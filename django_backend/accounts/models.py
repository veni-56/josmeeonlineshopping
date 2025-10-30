from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
import random
import string
from django.utils import timezone
from datetime import timedelta


class CustomUser(AbstractUser):
    """Custom user model with role-based access"""
    
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('admin', 'Admin'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    pan_number = models.CharField(max_length=10, blank=True, null=True, unique=True)
    gst_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_buyer(self):
        return self.role == 'buyer'
    
    @property
    def is_seller(self):
        return self.role == 'seller'
    
    @property
    def is_admin_user(self):
        return self.role == 'admin' or self.is_superuser


class OTPVerification(models.Model):
    """Model to store OTP for phone verification"""
    
    phone = models.CharField(max_length=20)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"OTP for {self.phone}"
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def is_valid(self):
        return not self.is_expired() and not self.is_verified and self.attempts < 5
    
    @staticmethod
    def generate_otp():
        """Generate a 6-digit OTP"""
        return ''.join(random.choices(string.digits, k=6))
    
    @staticmethod
    def create_otp(phone):
        """Create a new OTP for the given phone number"""
        otp_code = OTPVerification.generate_otp()
        expires_at = timezone.now() + timedelta(minutes=10)
        otp = OTPVerification.objects.create(
            phone=phone,
            otp=otp_code,
            expires_at=expires_at
        )
        return otp


class UserProfile(models.Model):
    """Extended user profile information"""
    
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    
    def __str__(self):
        return f"Profile of {self.user.username}"


class Address(models.Model):
    """User shipping addresses"""
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Addresses'
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.city}, {self.country}"
    
    def save(self, *args, **kwargs):
        # Ensure only one default address per user
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)


class SellerDocument(models.Model):
    """Model to store seller documents (PAN, GST, etc.)"""
    
    DOCUMENT_TYPES = (
        ('pan', 'PAN Card'),
        ('gst', 'GST Certificate'),
        ('business_license', 'Business License'),
        ('other', 'Other'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending Verification'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='seller_documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    document_file = models.FileField(upload_to='seller_documents/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        unique_together = ('user', 'document_type')
    
    def __str__(self):
        return f"{self.user.username} - {self.get_document_type_display()}"
