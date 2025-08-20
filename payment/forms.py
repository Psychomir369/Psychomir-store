from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام و نام خانوادگی'}),
        required=True,
    )
    shipping_email = forms.CharField(
        label="",  
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'}), 
        required=True,  
    )
    shipping_phone = forms.CharField(
        label="",  
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره تلفن'}),  
        required=True,  
    )
    shipping_address = forms.CharField(
        label="",  
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'آدرس'}),  
        required=True,  
    )
    shipping_city = forms.CharField(
        label="",  
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شهر'}),  
        required=True, 
    )
    shipping_state = forms.CharField(
        label="",  
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'منطقه'}), 
        required=False, 
    )
    shipping_zipcode = forms.CharField(
        label="",  
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کد پستی'}), 
        required=True, 
    )

    class Meta:
        model = ShippingAddress
        fields = [
            'shipping_full_name', 'shipping_email', 'shipping_phone',
            'shipping_city', 'shipping_state', 'shipping_zipcode', 'shipping_address',
        ]
        exclude = ['user',]