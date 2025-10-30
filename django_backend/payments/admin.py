from django.contrib import admin
from django.utils import timezone
from .models import Payment, SellerWallet, Earning, PayoutRequest

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order_id", "amount", "currency", "status", "created_at")
    list_filter = ("status", "currency", "created_at")
    search_fields = ("order_id", "stripe_session_id")
    readonly_fields = ("stripe_session_id", "created_at", "updated_at")
    ordering = ['-created_at']

@admin.register(SellerWallet)
class SellerWalletAdmin(admin.ModelAdmin):
    list_display = ("seller", "balance", "total_earned", "total_withdrawn", "updated_at")
    search_fields = ("seller__username", "seller__email")
    readonly_fields = ("seller", "updated_at")

@admin.register(Earning)
class EarningAdmin(admin.ModelAdmin):
    list_display = ("seller", "order_id", "amount", "platform_fee", "created_at")
    list_filter = ("created_at", "seller")
    search_fields = ("seller__username", "order_id", "order_item_id")
    readonly_fields = ("seller", "order_id", "order_item_id", "created_at")
    ordering = ['-created_at']

@admin.register(PayoutRequest)
class PayoutRequestAdmin(admin.ModelAdmin):
    list_display = ("seller", "amount", "status", "method", "created_at", "processed_at")
    list_filter = ("status", "method", "created_at")
    search_fields = ("seller__username", "seller__email")
    actions = ["mark_paid", "approve", "reject"]
    readonly_fields = ("seller", "created_at")
    ordering = ['-created_at']

    def mark_paid(self, request, queryset):
        """Mark selected payouts as paid"""
        count = 0
        for payout in queryset.filter(status__in=["approved", "pending"]):
            payout.status = "paid"
            payout.processed_at = timezone.now()
            payout.save()
            
            # Adjust wallet
            wallet, _ = SellerWallet.objects.get_or_create(seller=payout.seller)
            wallet.balance = max(wallet.balance - payout.amount, 0)
            wallet.total_withdrawn = wallet.total_withdrawn + payout.amount
            wallet.save()
            count += 1
        
        self.message_user(request, f"{count} payout(s) marked as paid")
    mark_paid.short_description = "Mark selected payouts as paid"

    def approve(self, request, queryset):
        """Approve selected payouts"""
        count = queryset.filter(status="pending").update(status="approved")
        self.message_user(request, f"{count} payout(s) approved")
    approve.short_description = "Approve selected payouts"

    def reject(self, request, queryset):
        """Reject selected payouts"""
        count = queryset.filter(status="pending").update(status="rejected")
        self.message_user(request, f"{count} payout(s) rejected")
    reject.short_description = "Reject selected payouts"
