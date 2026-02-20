from .services import CartManager

def cart(request):
    """Cart context processor"""
    try:
        cart_manager = CartManager(request)
        summary = cart_manager.get_cart_summary()
        
        return {
            'cart_item_count': summary['item_count'],
            'cart_subtotal': summary['totals']['subtotal'],
            'cart_total': summary['totals']['total'],
        }
    except Exception as e:
        return {
            'cart_item_count': 0,
            'cart_subtotal': 0,
            'cart_total': 0,
        }