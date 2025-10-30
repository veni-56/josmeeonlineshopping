from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import seller_required
from .models import Shop, SellerDocument
from .forms import ShopCreateForm, ShopUpdateForm, SellerDocumentForm


@login_required
@seller_required
def create_shop_view(request):
    """Create a new shop (sellers only)"""
    # Check if seller already has a shop
    if hasattr(request.user, 'shop'):
        messages.info(request, 'You already have a shop.')
        return redirect('shops:shop_detail', slug=request.user.shop.slug)
    
    if request.method == 'POST':
        form = ShopCreateForm(request.POST, request.FILES)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.owner = request.user
            shop.save()
            messages.success(request, f'Shop "{shop.name}" created successfully!')
            return redirect('dashboard:seller_dashboard')
    else:
        form = ShopCreateForm()
    
    return render(request, 'shops/shop_form.html', {'form': form, 'action': 'Create'})


@login_required
@seller_required
def update_shop_view(request):
    """Update shop details"""
    shop = get_object_or_404(Shop, owner=request.user)
    
    if request.method == 'POST':
        form = ShopUpdateForm(request.POST, request.FILES, instance=shop)
        if form.is_valid():
            form.save()
            messages.success(request, 'Shop updated successfully!')
            return redirect('dashboard:seller_dashboard')
    else:
        form = ShopUpdateForm(instance=shop)
    
    return render(request, 'shops/shop_form.html', {'form': form, 'action': 'Update', 'shop': shop})


@login_required
@seller_required
def upload_document_view(request):
    """Upload seller documents"""
    shop = get_object_or_404(Shop, owner=request.user)
    
    if request.method == 'POST':
        form = SellerDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.shop = shop
            document.save()
            messages.success(request, 'Document uploaded successfully!')
            return redirect('shops:manage_documents')
    else:
        form = SellerDocumentForm()
    
    documents = shop.documents.all()
    context = {
        'form': form,
        'shop': shop,
        'documents': documents,
    }
    return render(request, 'shops/upload_document.html', context)


@login_required
@seller_required
def manage_documents_view(request):
    """Manage seller documents"""
    shop = get_object_or_404(Shop, owner=request.user)
    documents = shop.documents.all()
    
    context = {
        'shop': shop,
        'documents': documents,
    }
    return render(request, 'shops/manage_documents.html', context)


@login_required
@seller_required
def delete_document_view(request, document_id):
    """Delete a seller document"""
    shop = get_object_or_404(Shop, owner=request.user)
    document = get_object_or_404(SellerDocument, id=document_id, shop=shop)
    
    if request.method == 'POST':
        document.delete()
        messages.success(request, 'Document deleted successfully!')
    
    return redirect('shops:manage_documents')


def shop_detail_view(request, slug):
    """Public shop detail page"""
    shop = get_object_or_404(Shop, slug=slug, is_active=True)
    products = shop.products.filter(is_active=True)[:12]
    
    context = {
        'shop': shop,
        'products': products,
    }
    return render(request, 'shops/shop_detail.html', context)


def shop_list_view(request):
    """List all active shops"""
    shops = Shop.objects.filter(is_active=True, is_verified=True)
    return render(request, 'shops/shop_list.html', {'shops': shops})
