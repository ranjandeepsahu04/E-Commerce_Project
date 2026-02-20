
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import UserRegistrationForm, DistributorRegistrationForm, UserLoginForm, AddressForm
from .models import CustomUser, Address, UserProfile
import uuid
import logging
from orders.models import Order
from .forms import UserLoginForm

logger = logging.getLogger(__name__)

def register_choice(request):
    return render(request, 'accounts/register_choice.html')

def register_consumer(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Send welcome email
            try:
                subject = f'Welcome to WearHub, {user.username}!'
                
                # Email context
                context = {
                    'user': user,
                    'site_url': settings.SITE_URL,
                }
                
                # Try to render HTML email, fallback to plain text if template doesn't exist
                try:
                    html_message = render_to_string('emails/welcome_email.html', context)
                    plain_message = strip_tags(html_message)
                    
                    # Create email with HTML content
                    email = EmailMultiAlternatives(
                        subject=subject,
                        body=plain_message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[user.email],
                    )
                    email.attach_alternative(html_message, "text/html")
                    email.send(fail_silently=False)
                except:
                    # Fallback to simple text email if template doesn't exist
                    send_mail(
                        subject,
                        f'Hi {user.username},\n\nThank you for registering with WearHub. Your account has been created successfully.\n\nStart shopping now: {settings.SITE_URL}\n\nHappy Shopping!\nWearHub Team',
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=True,
                    )
                
                logger.info(f"Welcome email sent to {user.email}")
                messages.success(request, 'Registration successful! Check your email for confirmation.')
                
            except Exception as e:
                logger.error(f"Failed to send welcome email: {e}")
                messages.success(request, 'Registration successful!')
            
            login(request, user)
            return redirect('core:home')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register_consumer.html', {'form': form})

def register_distributor(request):
    if request.method == 'POST':
        form = DistributorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Send acknowledgment to distributor
            try:
                subject = 'Your Distributor Application - WearHub'
                message = f'''Dear {user.username},

Thank you for applying to become a distributor at WearHub!

Your application has been submitted successfully and is pending approval. 
We will review your details and notify you once your account is approved.

Business Name: {user.profile.business_name}
GST Number: {user.profile.gst_number}
PAN Number: {user.profile.pan_number}

You will receive another email once your account is approved.

Thank you for partnering with WearHub!

Best regards,
WearHub Team'''
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                logger.error(f"Failed to send distributor email: {e}")
            
            # Notify admin
            try:
                admin_subject = f'New Distributor Registration: {user.username}'
                admin_message = f'''New distributor registered:

Username: {user.username}
Email: {user.email}
Phone: {user.phone_number}
Business: {user.profile.business_name}
GST: {user.profile.gst_number}
PAN: {user.profile.pan_number}

Approve at: {settings.SITE_URL}/admin/accounts/customuser/'''
                
                send_mail(
                    admin_subject,
                    admin_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.ADMIN_EMAIL],
                    fail_silently=True,
                )
            except Exception as e:
                logger.error(f"Failed to send admin notification: {e}")
            
            messages.info(request, 'Registration submitted for approval. You will be notified once approved.')
            return redirect('accounts:login')
    else:
        form = DistributorRegistrationForm()
    return render(request, 'accounts/register_distributor.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('core:home')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('core:home')

@login_required
def profile_view(request):
    addresses = Address.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    context={
        'addresses': addresses,
        'orders': orders,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Address added successfully!')
            return redirect('accounts:profile')
    else:
        form = AddressForm()
    return render(request, 'accounts/add_address.html', {'form': form})


@login_required
def edit_profile(request):
    """Edit user profile"""
    if request.method == 'POST':
        # Update user basic info
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.phone_number = request.POST.get('phone_number', '')
        user.save()
        
        # Update profile
        profile = user.profile
        profile.address_line1 = request.POST.get('address_line1', '')
        profile.address_line2 = request.POST.get('address_line2', '')
        profile.city = request.POST.get('city', '')
        profile.state = request.POST.get('state', '')
        profile.pincode = request.POST.get('pincode', '')
        profile.country = request.POST.get('country', 'India')
        
        # Handle profile picture
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')
    
    # GET request - display form with current data
    return render(request, 'accounts/edit_profile.html')


@login_required
def edit_address(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated successfully!')
            return redirect('accounts:profile')
    else:
        form = AddressForm(instance=address)
    
    return render(request, 'accounts/edit_address.html', {'form': form, 'address': address})

@login_required
def delete_address(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    address.delete()
    messages.success(request, 'Address deleted!')
    return redirect('accounts:profile')

# Signal for sending approval email
@receiver(post_save, sender=CustomUser)
def send_approval_email(sender, instance, created, **kwargs):
    """Send email when distributor is approved"""
    # Only send email if this is an update (not creation) and user is a distributor and just got approved
    if not created and instance.user_type == 'distributor' and instance.is_approved:
        try:
            subject = 'Your Distributor Account has been Approved!'
            message = f'''Dear {instance.username},

Congratulations! Your distributor account has been approved.

You can now log in and start adding products to WearHub.

Login here: {settings.SITE_URL}/accounts/login/

Business Name: {instance.profile.business_name}

What you can do now:
✓ Add and manage your products
✓ Track orders and sales
✓ Manage inventory
✓ Access distributor dashboard

Thank you for joining WearHub!

Best regards,
WearHub Team'''
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                fail_silently=False,
            )
            print(f"✅ Approval email sent to {instance.email}")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")