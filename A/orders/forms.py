from django import forms
from .models import Address


class ApplyCouponForm(forms.Form):
    """
    form for add coupon
    """

    coupon = forms.CharField(label="کد تخفیف", required=False,
                             widget=forms.TextInput(attrs={'class': 'class-alert alert col-md-2'}))


class AddressForm(forms.Form):
    address = forms.CharField(label="آدرس", max_length=500)
