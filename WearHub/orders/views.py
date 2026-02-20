# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.core.mail import send_mail
# from django.conf import settings
# from django.utils import timezone
# from cart.models import Cart
# from .models import Order, OrderItem, Coupon
# from .forms import CheckoutForm

# @login_required
# def checkout(request):
#     cart = Cart.objects.filter(user=request.user).first()
#     if not cart or cart.get_total_items() == 0:
#         messages.error(request, 'Your cart is empty!')
#         return redirect('products:product_list')
    
#     if request.method == 'POST':
#         form = CheckoutForm(request.POST, user=request.user)
#         if form.is_valid():
#             # Create order
#             order = Order.objects.create(
#                 user=request.user,
#                 shipping_address=str(form.cleaned_data['shipping_address']),
#                 billing_address=str(form.cleaned_data['billing_address']),
#                 payment_method=form.cleaned_data['payment_method'],
#                 subtotal=cart.get_total(),
#                 total=cart.get_total()
#             )
            
#             # Apply coupon if valid
#             coupon_code = form.cleaned_data['coupon_code']
#             if coupon_code:
#                 try:
#                     coupon = Coupon.objects.get(code=coupon_code, is_active=True)
#                     if coupon.is_valid():
#                         discount = (coupon.discount_percent / 100) * order.subtotal
#                         if coupon.max_discount_amount and discount > coupon.max_discount_amount:
#                             discount = coupon.max_discount_amount
#                         order.discount = discount
#                         order.total = order.subtotal - discount
#                         coupon.used_count += 1
#                         coupon.save()
#                 except Coupon.DoesNotExist:
#                     messages.warning(request, 'Invalid coupon code!')
            
#             order.save()
            
#             # Create order items
#             for cart_item in cart.items.all():
#                 OrderItem.objects.create(
#                     order=order,
#                     product=cart_item.product,
#                     product_name=cart_item.product.name,
#                     quantity=cart_item.quantity,
#                     price=cart_item.product.get_discounted_price(),
#                     size=cart_item.size,
#                     color=cart_item.color
#                 )
            
#             # Clear cart
#             cart.items.all().delete()
            
#             # Send confirmation email
#             send_mail(
#                 f'Order Confirmation - {order.order_number}',
#                 f'Thank you for your order!\n\nOrder Number: {order.order_number}\nTotal: ₹{order.total}',
#                 settings.DEFAULT_FROM_EMAIL,
#                 [request.user.email],
#                 fail_silently=True,
#             )
            
#             messages.success(request, 'Order placed successfully!')
#             return redirect('orders:order_confirmation', order_id=order.id)
#     else:
#         form = CheckoutForm(user=request.user)
    
#     context = {
#         'form': form,
#         'cart': cart,
#     }
#     return render(request, 'orders/checkout.html', context)

# @login_required
# def order_confirmation(request, order_id):
#     order = get_object_or_404(Order, id=order_id, user=request.user)
#     return render(request, 'orders/confirmation.html', {'order': order})

# @login_required
# def order_history(request):
#     orders = Order.objects.filter(user=request.user).order_by('-created_at')
#     return render(request, 'orders/history.html', {'orders': orders})

# @login_required
# def order_detail(request, order_id):
#     order = get_object_or_404(Order, id=order_id, user=request.user)
#     return render(request, 'orders/detail.html', {'order': order})

# @login_required
# def cancel_order(request, order_id):
#     order = get_object_or_404(Order, id=order_id, user=request.user)
    
#     if order.status == 'pending':
#         order.status = 'cancelled'
#         order.save()
#         messages.success(request, 'Order cancelled successfully!')
#     else:
#         messages.error(request, 'Order cannot be cancelled!')
    
#     return redirect('orders:order_detail', order_id=order.id)





from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from cart.models import Cart
from accounts.models import Address
from .models import Order, OrderItem, Coupon
from .forms import CheckoutForm
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

@login_required
def checkout(request):
    # Get user's cart
    cart = Cart.objects.filter(user=request.user).first()
    
    # Check if cart exists and has items
    if not cart or cart.get_total_items() == 0:
        messages.error(request, 'Your cart is empty!')
        return redirect('products:product_list')
    
    # Calculate cart totals
    cart_items = cart.items.all()
    subtotal = sum(item.get_cost() for item in cart_items)
    tax = subtotal * Decimal('0.18')  # 18% GST
    shipping = Decimal('50') if subtotal < Decimal('1000') else Decimal('0')
    total = subtotal + tax + shipping
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Get form data
            cleaned_data = form.cleaned_data
            
            # Create shipping address string
            shipping_address = f"{cleaned_data['first_name']} {cleaned_data['last_name']}\n"
            shipping_address += f"{cleaned_data['address_line1']}\n"
            if cleaned_data['address_line2']:
                shipping_address += f"{cleaned_data['address_line2']}\n"
            shipping_address += f"{cleaned_data['city']}, {cleaned_data['state']} - {cleaned_data['pincode']}\n"
            shipping_address += cleaned_data['country']
            
            # Save address if checkbox is checked
            if cleaned_data.get('save_address'):
                Address.objects.create(
                    user=request.user,
                    full_name=f"{cleaned_data['first_name']} {cleaned_data['last_name']}",
                    phone=cleaned_data['phone'],
                    address_line1=cleaned_data['address_line1'],
                    address_line2=cleaned_data.get('address_line2', ''),
                    city=cleaned_data['city'],
                    state=cleaned_data['state'],
                    pincode=cleaned_data['pincode'],
                    country=cleaned_data['country'],
                    address_type='home'
                )
            
            # Create order
            order = Order.objects.create(
                user=request.user,
                shipping_address=shipping_address,
                billing_address=shipping_address,  # Using same address for billing
                payment_method=cleaned_data['payment_method'],
                subtotal=subtotal,
                shipping_charge=shipping,
                discount=Decimal('0'),
                total=total,
                status='confirmed'  # Auto-confirm order
            )
            
            # Apply coupon if provided
            coupon_code = cleaned_data.get('coupon_code')
            discount = Decimal('0')
            if coupon_code:
                try:
                    coupon = Coupon.objects.get(code=coupon_code, is_active=True)
                    if coupon.is_valid():
                        discount = (coupon.discount_percent / Decimal('100')) * subtotal
                        if coupon.max_discount_amount and discount > coupon.max_discount_amount:
                            discount = coupon.max_discount_amount
                        order.discount = discount
                        order.total = total - discount
                        coupon.used_count += 1
                        coupon.save()
                        messages.success(request, f'Coupon applied! You saved ₹{discount}')
                except Coupon.DoesNotExist:
                    messages.warning(request, 'Invalid coupon code!')
            
            order.save()
            
            # Create order items from cart items
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    product_name=cart_item.product.name,
                    quantity=cart_item.quantity,
                    price=cart_item.product.get_discounted_price(),
                    size=cart_item.size,
                    color=cart_item.color
                )
                
                # Reduce product stock
                product = cart_item.product
                product.stock -= cart_item.quantity
                product.save()
            
            # Clear the cart
            cart.items.all().delete()
            
            # Send order confirmation email
            try:
                subject = f'Order Confirmed! #{order.order_number}'
                
                # Email context
                context = {
                    'order': order,
                    'user': request.user,
                    'site_url': settings.SITE_URL,
                }
                
                # Try to send HTML email, fallback to plain text
                try:
                    html_message = render_to_string('emails/order_confirmation.html', context)
                    plain_message = strip_tags(html_message)
                    
                    email = EmailMultiAlternatives(
                        subject=subject,
                        body=plain_message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[request.user.email],
                    )
                    email.attach_alternative(html_message, "text/html")
                    email.send(fail_silently=False)
                except:
                    # Fallback to plain text
                    message = f'''Dear {request.user.username},

Your order has been confirmed successfully!

Order Number: {order.order_number}
Total Amount: ₹{order.total}
Payment Method: {order.get_payment_method_display()}

You can track your order here:
{settings.SITE_URL}/orders/detail/{order.id}/

Thank you for shopping with WearHub!

Best regards,
WearHub Team'''
                    
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [request.user.email],
                        fail_silently=True,
                    )
                
                logger.info(f"Order confirmation email sent to {request.user.email}")
                
            except Exception as e:
                logger.error(f"Failed to send order confirmation email: {e}")
            
            messages.success(request, f'Order placed successfully! Your order number is {order.order_number}')
            return redirect('orders:order_confirmation', order_id=order.id)
    else:
        # Pre-fill form with user data if available
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'phone': request.user.phone_number,
        }
        form = CheckoutForm(initial=initial_data)
    
    context = {
        'form': form,
        'cart': cart,
        'cart_items': cart_items,
        'totals': {
            'subtotal': subtotal,
            'tax': tax,
            'shipping': shipping,
            'total': total,
        }
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/confirmation.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        
        # Restore product stock
        for item in order.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()
        
        messages.success(request, 'Order cancelled successfully!')
    else:
        messages.error(request, 'Order cannot be cancelled!')
    
    return redirect('orders:order_detail', order_id=order.id)