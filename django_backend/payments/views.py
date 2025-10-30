import json
import decimal
from decimal import Decimal
from typing import Dict, Any, List

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone

from .models import Payment, SellerWallet, Earning, PayoutRequest

# We expect store app to provide access to cart, order, and order items.
try:
    from store.models import Order, OrderItem, Product
except Exception:
    Order = None
    OrderItem = None
    Product = None

def _get_cart_items_from_session(request) -> List[Dict[str, Any]]:
    """
    Return a list of items from session cart with keys:
    id, name, price, quantity, seller_id
    """
    cart = request.session.get("cart", {})
    items = []
    for pid, item in cart.items():
        items.append({
            "id": str(pid),
            "name": item.get("name", f"Product {pid}"),
            "price": Decimal(str(item.get("price", "0"))),
            "quantity": int(item.get("qty", 1)),
            "seller_id": item.get("seller_id"),
        })
    return items

@login_required
def create_checkout_session(request):
    """Create a Stripe checkout session"""
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    items = _get_cart_items_from_session(request)
    if not items:
        return JsonResponse({"error": "Cart is empty"}, status=400)

    try:
        import stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY
    except Exception as e:
        return JsonResponse({"error": "Payment service not configured"}, status=500)

    line_items = []
    amount_total = Decimal("0")
    currency = "usd"
    
    try:
        for it in items:
            unit_amount = int((it["price"] * 100).quantize(Decimal("1")))
            line_items.append({
                "price_data": {
                    "currency": currency,
                    "product_data": {"name": it["name"]},
                    "unit_amount": unit_amount,
                },
                "quantity": it["quantity"],
            })
            amount_total += (it["price"] * it["quantity"])

        success_url = f"{settings.SITE_URL}{reverse('payments:success')}"
        cancel_url = f"{settings.SITE_URL}{reverse('payments:cancel')}"

        session = stripe.checkout.Session.create(
            mode="payment",
            line_items=line_items,
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={
                "user_id": str(request.user.id),
                "cart_json": json.dumps(items, default=str),
            },
        )

        Payment.objects.create(
            order_id="pending",
            stripe_session_id=session.id,
            amount=amount_total,
            currency=currency,
            status="created",
        )

        return JsonResponse({"id": session.id, "publishableKey": settings.STRIPE_PUBLISHABLE_KEY})
    
    except Exception as e:
        return JsonResponse({"error": f"Payment error: {str(e)}"}, status=500)

def checkout_success(request):
    """Handle successful checkout"""
    request.session["cart"] = {}
    return render(request, "payments/checkout_success.html")

def checkout_cancel(request):
    """Handle cancelled checkout"""
    return render(request, "payments/checkout_cancel.html")

@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe webhook events"""
    import stripe
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception as e:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        session_id = session["id"]
        try:
            payment = Payment.objects.get(stripe_session_id=session_id)
        except Payment.DoesNotExist:
            return HttpResponse(status=200)

        cart_items = json.loads(session.get("metadata", {}).get("cart_json", "[]"))
        user_id = session.get("metadata", {}).get("user_id")

        order_id = payment.order_id
        if Order is not None and order_id == "pending":
            order = Order.objects.create(user_id=user_id, total_amount=payment.amount, status="paid")
            order_id = str(order.pk)

        payment.status = "paid"
        payment.order_id = order_id
        payment.save()

        # Distribute earnings per item
        fee_percent = Decimal(str(getattr(settings, "PLATFORM_FEE_PERCENT", 10))) / Decimal("100")
        for it in cart_items:
            seller_id = it.get("seller_id")
            price = Decimal(str(it.get("price", "0")))
            qty = Decimal(str(it.get("quantity", 1)))
            gross = (price * qty).quantize(Decimal("0.01"))
            platform_fee = (gross * fee_percent).quantize(Decimal("0.01"))
            seller_amount = (gross - platform_fee).quantize(Decimal("0.01"))

            if seller_id:
                Earning.objects.create(
                    seller_id=seller_id,
                    order_id=order_id,
                    order_item_id=str(it.get("id")),
                    amount=seller_amount,
                    platform_fee=platform_fee,
                )
                wallet, _ = SellerWallet.objects.get_or_create(seller_id=seller_id)
                wallet.balance = (wallet.balance + seller_amount).quantize(Decimal("0.01"))
                wallet.total_earned = (wallet.total_earned + seller_amount).quantize(Decimal("0.01"))
                wallet.save()

    return HttpResponse(status=200)

@login_required
def seller_payouts(request):
    """View seller payouts and wallet"""
    if not request.user.is_seller:
        messages.error(request, 'Only sellers can access this page.')
        return redirect('accounts:dashboard')
    
    wallet, _ = SellerWallet.objects.get_or_create(seller=request.user)
    payouts = PayoutRequest.objects.filter(seller=request.user).order_by("-created_at")
    earnings = Earning.objects.filter(seller=request.user).order_by("-created_at")[:10]
    
    context = {
        'wallet': wallet,
        'payouts': payouts,
        'earnings': earnings,
    }
    return render(request, "payments/seller_payouts.html", context)

@login_required
def request_payout(request):
    """Request a payout"""
    if not request.user.is_seller:
        return HttpResponseForbidden("Only sellers can request payouts")
    
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")
    
    wallet, _ = SellerWallet.objects.get_or_create(seller=request.user)
    
    try:
        amount = Decimal(str(request.POST.get("amount", "0")))
    except decimal.InvalidOperation:
        messages.error(request, "Invalid amount")
        return redirect("payments:seller_payouts")
    
    if amount <= 0:
        messages.error(request, "Amount must be greater than 0")
        return redirect("payments:seller_payouts")
    
    if amount > wallet.balance:
        messages.error(request, "Insufficient balance")
        return redirect("payments:seller_payouts")
    
    PayoutRequest.objects.create(
        seller=request.user,
        amount=amount,
        status="pending",
        method="manual"
    )
    messages.success(request, f"Payout request of {amount} submitted successfully")
    return redirect("payments:seller_payouts")
