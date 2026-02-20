from django.shortcuts import render, redirect
from django.contrib import messages
from products.models import Product, Category
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:8]
    new_arrivals = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
        'categories': categories,
    }
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Send email
        send_mail(
            f'Contact Form: {subject}',
            f'From: {name} ({email})\n\n{message}',
            email,
            [settings.ADMIN_EMAIL],
            fail_silently=True,
        )
        
        messages.success(request, 'Thank you for contacting us. We will get back to you soon!')
        return redirect('core:contact')
    
    return render(request, 'core/contact.html')

def terms(request):
    return render(request, 'core/terms.html')