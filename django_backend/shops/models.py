from django.db import models
from django.utils.text import slugify
from accounts.models import CustomUser


class Shop(models.Model):
    """Seller shop model"""
    
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='shop')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='shops/logos/', blank=True, null=True)
    banner = models.ImageField(upload_to='shops/banners/', blank=True, null=True)
    
    # Contact information
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    
    pan_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    gst_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def total_products(self):
        return self.products.count()
    
    @property
    def total_sales(self):
        from payments.models import Earning
        return Earning.objects.filter(shop=self).aggregate(
            total=models.Sum('amount')
        )['total'] or 0


class SellerDocument(models.Model):
    """Model to store seller supporting documents"""
    
    DOCUMENT_TYPES = (
        ('pan_certificate', 'PAN Certificate'),
        ('gst_certificate', 'GST Certificate'),
        ('business_license', 'Business License'),
        ('bank_statement', 'Bank Statement'),
        ('other', 'Other'),
    )
    
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    document_file = models.FileField(upload_to='seller_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.shop.name} - {self.get_document_type_display()}"
