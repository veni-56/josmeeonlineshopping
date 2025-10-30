from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, UserProfile, Address, OTPVerification, SellerDocument


class OTPVerificationForm(forms.Form):
    """Form for OTP verification"""
    
    otp = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter 6-digit OTP',
            'inputmode': 'numeric',
            'maxlength': '6'
        })
    )
    
    def clean_otp(self):
        otp = self.cleaned_data.get('otp')
        if not otp.isdigit():
            raise forms.ValidationError('OTP must contain only digits.')
        return otp


class PhoneVerificationForm(forms.Form):
    """Form for phone number verification"""
    
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+1 (555) 123-4567',
            'type': 'tel'
        })
    )
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Basic phone validation - remove spaces and special characters
        cleaned_phone = ''.join(filter(str.isdigit, phone))
        if len(cleaned_phone) < 10:
            raise forms.ValidationError('Please enter a valid phone number.')
        return phone


class UserRegistrationForm(UserCreationForm):
    """Form for user registration"""
    
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email address'
    }))
    
    pan_number = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'PAN Card Number (e.g., AAAPA1234A)'
        })
    )
    
    gst_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'GST Number (e.g., 27AABCT1234H1Z0)'
        })
    )
    
    role = forms.ChoiceField(
        choices=[('buyer', 'Buyer'), ('seller', 'Seller')],
        widget=forms.RadioSelect,
        initial='buyer'
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role', 'phone', 'pan_number', 'gst_number']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number (optional)'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm password'})
    
    def clean_pan_number(self):
        pan = self.cleaned_data.get('pan_number')
        if pan and len(pan) != 10:
            raise forms.ValidationError('PAN number must be exactly 10 characters.')
        if pan and CustomUser.objects.filter(pan_number=pan).exists():
            raise forms.ValidationError('This PAN number is already registered.')
        return pan
    
    def clean_gst_number(self):
        gst = self.cleaned_data.get('gst_number')
        if gst and len(gst) != 15:
            raise forms.ValidationError('GST number must be exactly 15 characters.')
        if gst and CustomUser.objects.filter(gst_number=gst).exists():
            raise forms.ValidationError('This GST number is already registered.')
        return gst


class UserLoginForm(AuthenticationForm):
    """Form for user login"""
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))


class UserProfileForm(forms.ModelForm):
    """Form for editing user profile"""
    
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = UserProfile
        fields = ['bio', 'date_of_birth', 'gender']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['phone'].initial = self.instance.user.phone


class AddressForm(forms.ModelForm):
    """Form for adding/editing addresses"""
    
    class Meta:
        model = Address
        fields = ['full_name', 'phone', 'street_address', 'city', 'state', 'country', 'postal_code', 'is_default']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'street_address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SellerDocumentForm(forms.ModelForm):
    """Form for uploading seller documents"""
    
    class Meta:
        model = SellerDocument
        fields = ['document_type', 'document_file']
        widgets = {
            'document_type': forms.Select(attrs={'class': 'form-control'}),
            'document_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png'
            })
        }
