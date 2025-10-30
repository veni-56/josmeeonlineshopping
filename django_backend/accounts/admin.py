from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, UserProfile, Address, OTPVerification


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'is_verified', 'phone_verified', 'is_active', 'date_joined']
    list_filter = ['role', 'is_verified', 'phone_verified', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'avatar', 'is_verified', 'phone_verified')}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'email', 'phone')}),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        """Ensure superuser can always access admin"""
        form = super().get_form(request, obj, **kwargs)
        return form


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'date_of_birth']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['user']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user', 'city', 'country', 'is_default']
    list_filter = ['is_default', 'country', 'city']
    search_fields = ['full_name', 'user__username', 'city', 'country']
    readonly_fields = ['user', 'created_at']


@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ['phone', 'is_verified', 'is_expired', 'attempts', 'created_at']
    list_filter = ['is_verified', 'created_at']
    search_fields = ['phone']
    readonly_fields = ['phone', 'otp', 'created_at', 'expires_at']
    
    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True
    is_expired.short_description = 'Expired'
