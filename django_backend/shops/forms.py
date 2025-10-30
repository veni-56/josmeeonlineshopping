from django import forms
from .models import Shop, SellerDocument


class ShopCreateForm(forms.ModelForm):
    """Form for creating a new shop"""
    
    class Meta:
        model = Shop
        fields = ['name', 'description', 'logo', 'banner', 'email', 'phone', 'address', 'pan_number', 'gst_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shop name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your shop'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'banner': forms.FileInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Shop email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shop phone'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Shop address'}),
            'pan_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PAN Number (e.g., AAAPA1234A)'}),
            'gst_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'GST Number (e.g., 27AABCT1234H1Z0)'}),
        }


class ShopUpdateForm(forms.ModelForm):
    """Form for updating shop details"""
    
    class Meta:
        model = Shop
        fields = ['name', 'description', 'logo', 'banner', 'email', 'phone', 'address', 'pan_number', 'gst_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'banner': forms.FileInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'pan_number': forms.TextInput(attrs={'class': 'form-control'}),
            'gst_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SellerDocumentForm(forms.ModelForm):
    """Form for uploading seller documents"""
    
    class Meta:
        model = SellerDocument
        fields = ['document_type', 'document_file']
        widgets = {
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'document_file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.jpg,.jpeg,.png,.doc,.docx'}),
        }
