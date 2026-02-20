# from django import forms
# from .models import Order, Coupon

# class CheckoutForm(forms.Form):
#     shipping_address = forms.ModelChoiceField(
#         queryset=None,
#         empty_label=None,
#         widget=forms.RadioSelect,
#         required=True
#     )
#     billing_address = forms.ModelChoiceField(
#         queryset=None,
#         empty_label=None,
#         widget=forms.RadioSelect,
#         required=True
#     )
#     payment_method = forms.ChoiceField(
#         choices=Order.PAYMENT_CHOICES,
#         widget=forms.RadioSelect
#     )
#     coupon_code = forms.CharField(max_length=50, required=False)
#     notes = forms.CharField(widget=forms.Textarea, required=False)
    
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user')
#         super().__init__(*args, **kwargs)
#         self.fields['shipping_address'].queryset = user.addresses.all()
#         self.fields['billing_address'].queryset = user.addresses.all()


from django import forms
from .models import Order, Coupon

class CheckoutForm(forms.Form):
    # Shipping address fields
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address_line1 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address_line2 = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    state = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    pincode = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.ChoiceField(choices=[
        ('', 'Select Country'),
        ('India', 'India'),
        ('USA', 'United States'),
        ('UK', 'United Kingdom'),
    ], widget=forms.Select(attrs={'class': 'form-control'}))
    
    save_address = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    
    # Payment method
    payment_method = forms.ChoiceField(
        choices=Order.PAYMENT_CHOICES,
        widget=forms.RadioSelect,
        initial='cod'
    )
    
    # Coupon
    coupon_code = forms.CharField(required=False, max_length=50, 
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter coupon code'}))