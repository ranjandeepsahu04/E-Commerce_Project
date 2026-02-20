# from django import forms
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from .models import CustomUser, UserProfile, Address

# class UserRegistrationForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     user_type = forms.ChoiceField(choices=CustomUser.USER_TYPES, widget=forms.RadioSelect)
#     phone_number = forms.CharField(max_length=15, required=True)
    
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'phone_number', 'user_type', 'password1', 'password2']
    
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.email = self.cleaned_data['email']
#         user.phone_number = self.cleaned_data['phone_number']
#         user.user_type = self.cleaned_data['user_type']
        
#         if commit:
#             user.save()
#             # Create profile
#             UserProfile.objects.create(user=user)
#         return user

# class DistributorRegistrationForm(UserRegistrationForm):
#     business_name = forms.CharField(max_length=255, required=True)
#     gst_number = forms.CharField(max_length=20, required=True)
#     pan_number = forms.CharField(max_length=20, required=True)
    
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         if commit:
#             user.is_approved = False  # Requires admin approval
#             user.save()
#             # Update profile with business details
#             profile = user.profile
#             profile.business_name = self.cleaned_data['business_name']
#             profile.gst_number = self.cleaned_data['gst_number']
#             profile.pan_number = self.cleaned_data['pan_number']
#             profile.save()
#         return user

# class UserLoginForm(AuthenticationForm):
#     username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

# class AddressForm(forms.ModelForm):
#     class Meta:
#         model = Address
#         exclude = ['user']




from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, UserProfile, Address

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        
        if commit:
            user.save()
            # Create profile for ALL users
            UserProfile.objects.create(user=user)
        return user

class ConsumerRegistrationForm(UserRegistrationForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'consumer'
        if commit:
            user.save()
            # Profile is already created in parent save() method
        return user

class DistributorRegistrationForm(UserRegistrationForm):
    business_name = forms.CharField(max_length=255, required=True)
    gst_number = forms.CharField(max_length=20, required=True)
    pan_number = forms.CharField(max_length=20, required=True)
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'distributor'
        user.is_approved = False  # Requires admin approval
        
        if commit:
            user.save()
            # Update the profile with business details
            # Profile already exists from parent save()
            profile = user.profile
            profile.business_name = self.cleaned_data['business_name']
            profile.gst_number = self.cleaned_data['gst_number']
            profile.pan_number = self.cleaned_data['pan_number']
            profile.save()
        return user

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user']
        widgets = {
            'address_type': forms.Select(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line1': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control'}),
            'landmark': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }