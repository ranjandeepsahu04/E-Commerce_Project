from django.core.exceptions import ValidationError
from django.db import transaction
from products.models import Product
from .models import Cart, CartItem
import copy
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

def cart_item_generator(cart):
    """
    Generator function for cart items - demonstrates generator concept
    """
    items = cart.items.select_related('product').all()
    for item in items:
        yield {
            'id': str(item.id),
            'product_id': str(item.product.id),
            'product_name': item.product.name,
            'quantity': item.quantity,
            'price': float(item.product.get_discounted_price()),
            'total': float(item.get_cost())
        }

class CartManager:
    """
    OOP Service Class for Cart Management
    Demonstrates OOP design patterns, static methods, and exception handling
    """
    
    def __init__(self, request):
        self.request = request
        self.cart = self._get_or_create_cart()
    
    def _get_or_create_cart(self):
        """Get existing cart or create new one"""
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
        else:
            session_id = self.request.session.session_key
            if not session_id:
                self.request.session.create()
                session_id = self.request.session.session_key
            cart, created = Cart.objects.get_or_create(session_id=session_id)
        return cart
    
    def add_item(self, product_id, quantity=1, variant_id=None):
        """
        Add item to cart with deep copy demonstration
        """
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            
            # Convert quantity to Decimal for price calculation
            quantity = Decimal(str(quantity))  # Convert to Decimal

            # Deep copy demonstration for cart item
            item_data = {
                'product': product,
                'quantity': quantity,
                'price_at_time': float(product.get_discounted_price())
            }
            
            # Create a deep copy for logging/audit
            import copy
            item_audit_copy = copy.deepcopy(item_data)
            logger.info(f"Adding to cart - Original: {item_data}, Copy: {item_audit_copy}")
            
            # Check stock
            if product.stock < quantity:
                raise ValidationError(f"Only {product.stock} items available in stock")
            
            # Get or create cart item
            cart_item, created = CartItem.objects.get_or_create(
                cart=self.cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            # Shallow copy demonstration
            shallow_copy = dict(item_data)  # Shallow copy
            logger.info(f"Shallow copy created: {shallow_copy}")
            
            return {'success': True, 'item': cart_item, 'created': created}
            
        except Product.DoesNotExist:
            logger.error(f"Product {product_id} not found")
            raise ValidationError("Product not found")
        except Exception as e:
            logger.exception("Error adding item to cart")
            raise
    
    @staticmethod
    def calculate_totals(cart_items):
        """
        Static method to calculate cart totals
        """
        subtotal = sum(item.get_cost() for item in cart_items)
        tax = subtotal * Decimal('0.18')  # 18% GST
        shipping = Decimal('50') if subtotal < Decimal('1000') else Decimal('0')
        total = subtotal + tax + shipping
        
        return {
            'subtotal': round(subtotal, 2),
            'tax': round(tax, 2),
            'shipping': shipping,
            'total': round(total, 2)
        }
    
    def update_quantity(self, item_id, quantity):
        """Update item quantity with validation"""
        try:
            cart_item = CartItem.objects.get(id=item_id, cart=self.cart)
            
            if quantity <= 0:
                cart_item.delete()
                return {'success': True, 'deleted': True}
            
            if cart_item.product.stock < quantity:
                raise ValidationError(f"Only {cart_item.product.stock} items available")
            
            cart_item.quantity = quantity
            cart_item.save()
            
            return {'success': True, 'item': cart_item}
            
        except CartItem.DoesNotExist:
            raise ValidationError("Cart item not found")
    
    def remove_item(self, item_id):
        """Remove item from cart"""
        try:
            cart_item = CartItem.objects.get(id=item_id, cart=self.cart)
            cart_item.delete()
            return {'success': True}
        except CartItem.DoesNotExist:
            raise ValidationError("Cart item not found")
    
    def clear_cart(self):
        """Clear all items from cart"""
        self.cart.items.all().delete()
        return {'success': True}
    
    def get_cart_summary(self):
        """Get complete cart summary"""
        items = self.cart.items.select_related('product').all()
        totals = self.calculate_totals(items)
        
        return {
            'items': items,
            'item_count': sum(item.quantity for item in items),
            'totals': totals
        }
    
    def merge_carts(self, session_cart):
        """
        Merge session cart with user cart after login
        Demonstrates exception handling and transaction
        """
        try:
            with transaction.atomic():
                for item in session_cart.items.all():
                    try:
                        cart_item = CartItem.objects.get(
                            cart=self.cart,
                            product=item.product
                        )
                        cart_item.quantity += item.quantity
                        cart_item.save()
                    except CartItem.DoesNotExist:
                        item.cart = self.cart
                        item.save()
                
                # Delete session cart
                session_cart.delete()
                
        except Exception as e:
            logger.exception("Error merging carts")
            raise ValidationError("Failed to merge carts")

class CartIterator:
    """
    Iterator class for cart items - demonstrates iterator protocol
    """
    def __init__(self, cart_items):
        self.cart_items = list(cart_items)
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index < len(self.cart_items):
            item = self.cart_items[self.index]
            self.index += 1
            return item
        raise StopIteration