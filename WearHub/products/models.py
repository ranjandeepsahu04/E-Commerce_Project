from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from decimal import Decimal

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('men', "Men's Wear"),
        ('women', "Women's Wear"),
        ('kids', "Kids' Wear"),
    ]
    
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.get_name_display()

class Product(models.Model):
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    ]
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=1)
    brand = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=50, blank=True)
    sizes = models.CharField(max_length=50, blank=True, help_text="Comma separated sizes")
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        
        # Ensure slug is unique
        original_slug = self.slug
        counter = 1
        while Product.objects.filter(slug=self.slug).exclude(id=self.id).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1
        
        super().save(*args, **kwargs)

    def get_discounted_price(self):
        if self.discount_price and self.discount_price < self.price:
            return self.discount_price
        return self.price
    
    def is_in_stock(self):
        return self.stock > 0

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_main = models.BooleanField(default=False)
    alt_text = models.CharField(max_length=255, blank=True)
    
    class Meta:
        ordering = ['-is_main', 'id']
    
    def __str__(self):
        return f"Image for {self.product.name}"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['product', 'user']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.rating}★"

# class Wishlist(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='wishlist_items'
#     )
#     product = models.ForeignKey(
#         Product,
#         on_delete=models.CASCADE,
#         related_name='wishlisted_by'
#     )
#     added_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ['user', 'product']

#     def __str__(self):
#         return f"{self.user.username} → {self.product.name}"
    


# class Product(models.Model):
#     # ... your existing fields ...
    
#     def save(self, *args, **kwargs):
#         # Auto-generate slug if not provided
#         if not self.slug:
#             self.slug = slugify(self.name)
        
#         # Ensure slug is unique
#         original_slug = self.slug
#         queryset = Product.objects.filter(slug=self.slug)
#         if queryset.exists() and queryset.first().id != self.id:
#             # Add a number to make it unique
#             counter = 1
#             while queryset.filter(slug=self.slug).exists():
#                 self.slug = f"{original_slug}-{counter}"
#                 counter += 1
        
#         super().save(*args, **kwargs)
