from django import template
from django.utils.http import urlencode

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """
    Return encoded URL parameters with the specified parameters added/replaced.
    
    This tag preserves all existing GET parameters while adding/changing the specified ones.
    
    Usage in your template (which you already have):
        <a href="?{% url_replace page=products.next_page_number %}">Next</a>
        <a href="?{% url_replace category=category.slug %}">Category Filter</a>
        <a href="{% url 'products:product_list' %}?{% url_replace category='' %}">All Products</a>
    """
    # Get the current request's GET parameters
    query = context['request'].GET.copy()
    
    # Update or add new parameters
    for key, value in kwargs.items():
        if value is None or value == '':
            # If value is empty, remove the parameter
            if key in query:
                del query[key]
        else:
            # Otherwise set the parameter
            query[key] = str(value)
    
    # Return the encoded query string
    return query.urlencode()


@register.filter
def get_range(value):
    """
    Return a range of numbers from 1 to value.
    
    Usage:
        {% for i in 5|get_range %}
            {{ i }}
        {% endfor %}
    """
    try:
        return range(1, int(value) + 1)
    except (ValueError, TypeError):
        return range(0)


@register.filter
def multiply(value, arg):
    """
    Multiply two numbers.
    
    Usage:
        {{ price|multiply:quantity }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def currency(value):
    """
    Format a number as Indian Rupees.
    
    Usage:
        {{ product.price|currency }}
    """
    try:
        return f"₹{float(value):,.2f}"
    except (ValueError, TypeError):
        return "₹0.00"


@register.filter
def discount_percentage(original, discounted):
    """
    Calculate discount percentage.
    
    Usage:
        {{ product.price|discount_percentage:product.discount_price }}
    """
    try:
        if original and discounted and float(original) > 0:
            discount = ((float(original) - float(discounted)) / float(original)) * 100
            return f"{int(discount)}% off"
        return ""
    except (ValueError, TypeError, ZeroDivisionError):
        return ""


@register.filter
def stars(rating):
    """
    Convert rating number to star HTML.
    
    Usage:
        {{ product.avg_rating|stars }}
    """
    try:
        rating = float(rating)
        full_stars = int(rating)
        half_star = 1 if rating - full_stars >= 0.5 else 0
        empty_stars = 5 - full_stars - half_star
        
        stars_html = '★' * full_stars
        if half_star:
            stars_html += '½'
        stars_html += '☆' * empty_stars
        
        return stars_html
    except (ValueError, TypeError):
        return "☆☆☆☆☆"


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    """
    Alternative to url_replace that takes the request explicitly.
    
    Usage:
        {% query_transform request page=5 %}
    """
    request = context.get('request')
    if not request:
        return ''
    
    updated = request.GET.copy()
    for key, value in kwargs.items():
        if value is not None:
            updated[key] = str(value)
        else:
            updated.pop(key, None)
    
    return updated.urlencode()


@register.filter
def add_class(value, css_class):
    """
    Add a CSS class to a form field.
    
    Usage:
        {{ form.field|add_class:"form-control" }}
    """
    try:
        return value.as_widget(attrs={"class": css_class})
    except:
        return value


@register.filter
def get_item(dictionary, key):
    """
    Get an item from a dictionary using a key.
    
    Usage:
        {{ mydict|get_item:key }}
    """
    return dictionary.get(key)


@register.filter
def subtract(value, arg):
    """
    Subtract arg from value.
    
    Usage:
        {{ total|subtract:discount }}
    """
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def divide(value, arg):
    """
    Divide value by arg.
    
    Usage:
        {{ total|divide:count }}
    """
    try:
        if float(arg) != 0:
            return float(value) / float(arg)
        return 0
    except (ValueError, TypeError):
        return 0