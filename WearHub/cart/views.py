
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Cart, CartItem
from products.models import Product
from .services import CartManager, cart_item_generator

def view_cart(request):
    """View cart contents"""
    cart_manager = CartManager(request)
    summary = cart_manager.get_cart_summary()
    
    # Demonstrate generator usage
    generated_items = list(cart_item_generator(cart_manager.cart))
    
    context = {
        'cart_items': summary['items'],
        'total_items': summary['item_count'],
        'totals': summary['totals'],
        'generated_items': generated_items,
        'cart': cart_manager.cart,
    }
    return render(request, 'cart/cart.html', context)

@require_POST
def add_to_cart(request):
    """Add item to cart"""
    try:
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        cart_manager = CartManager(request)
        result = cart_manager.add_item(product_id, quantity)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            summary = cart_manager.get_cart_summary()
            return JsonResponse({
                'success': True,
                'message': 'Item added to cart successfully!',
                'cart_count': summary['item_count'],
                'cart_total': summary['totals']['total']
            })
        
        messages.success(request, 'Item added to cart successfully!')
        return redirect('cart:view')
        
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
        
        messages.error(request, str(e))
        return redirect(request.META.get('HTTP_REFERER', 'products:product_list'))

@require_POST
@require_POST
def update_cart(request, item_id):  # item_id will be integer
    try:
        quantity = int(request.POST.get('quantity', 1))
        cart_manager = CartManager(request)
        result = cart_manager.update_quantity(item_id, quantity)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            summary = cart_manager.get_cart_summary()
            item = result.get('item')
            
            return JsonResponse({
                'success': True,
                'item_total': str(item.get_cost()) if item else '0',
                'item_id': str(item_id),
                'cart_count': summary['item_count'],
                'cart_subtotal': str(summary['totals']['subtotal']),
                'cart_tax': str(summary['totals']['tax']),
                'cart_shipping': str(summary['totals']['shipping']),
                'cart_total': str(summary['totals']['total']),
                'deleted': result.get('deleted', False)
            })
        
        messages.success(request, 'Cart updated successfully!')
        return redirect('cart:view_cart')
        
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
        
        messages.error(request, str(e))
        return redirect('cart:view_cart')

@require_POST
def remove_from_cart(request, item_id):  # item_id will be integer
    try:
        cart_manager = CartManager(request)
        cart_manager.remove_item(item_id)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            summary = cart_manager.get_cart_summary()
            return JsonResponse({
                'success': True,
                'message': 'Item removed from cart',
                'item_id': str(item_id),
                'cart_count': summary['item_count'],
                'cart_subtotal': str(summary['totals']['subtotal']),
                'cart_tax': str(summary['totals']['tax']),
                'cart_shipping': str(summary['totals']['shipping']),
                'cart_total': str(summary['totals']['total'])
            })
        
        messages.success(request, 'Item removed from cart!')
        return redirect('cart:view_cart')
        
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
        
        messages.error(request, str(e))
        return redirect('cart:view_cart')

@require_POST
def clear_cart(request):
    """Clear all items from cart"""
    try:
        cart_manager = CartManager(request)
        cart_manager.clear_cart()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Cart cleared successfully'
            })
        
        messages.success(request, 'Cart cleared successfully!')
        return redirect('cart:view')
        
    except Exception as e:
        messages.error(request, str(e))
        return redirect('cart:view')