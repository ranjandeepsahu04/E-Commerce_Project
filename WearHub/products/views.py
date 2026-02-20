from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
from .models import Product, Category, Review, ProductImage
from .forms import ProductForm, ProductImageForm, ReviewForm
from cart.models import Cart, CartItem

def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # Search
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__icontains=query)
        )
    
    # Filter by price
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Sorting
    sort = request.GET.get('sort', '-created_at')
    products = products.order_by(sort)
    
    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': category_slug,
        'query': query,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    reviews = product.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Related products
    related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product.id)[:4]
    
    # # Check if in wishlist
    # in_wishlist = False
    # if request.user.is_authenticated:
    #     in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
    
    context = {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'related_products': related_products,
        'in_wishlist': in_wishlist,
    }
    return render(request, 'products/product_detail.html', context)

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if user already reviewed
    if Review.objects.filter(product=product, user=request.user).exists():
        messages.error(request, 'You have already reviewed this product.')
        return redirect('products:product_detail', slug=product.slug)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('products:product_detail', slug=product.slug)
    else:
        form = ReviewForm()
    
    return render(request, 'products/add_review.html', {'form': form, 'product': product})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    if created:
        messages.success(request, 'Added to wishlist!')
    else:
        messages.info(request, 'Already in wishlist!')
    
    return redirect(request.META.get('HTTP_REFERER', 'products:product_detail'))

@login_required
def remove_from_wishlist(request, product_id):
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    messages.success(request, 'Removed from wishlist!')
    return redirect('products:wishlist')

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'products/wishlist.html', {'wishlist_items': wishlist_items})

# Distributor Views
@login_required
def distributor_dashboard(request):
    if request.user.user_type != 'distributor':
        messages.error(request, 'Access denied.')
        return redirect('core:home')
    
    products = Product.objects.filter(added_by=request.user)
    return render(request, 'products/distributor/dashboard.html', {'products': products})

@login_required
def add_product(request):
    if request.user.user_type != 'distributor':
        messages.error(request, 'Only distributors can add products.')
        return redirect('core:home')
    
    if not request.user.is_approved:
        messages.warning(request, 'Your account is pending approval.')
        return redirect('core:home')
    
    if request.method == 'POST':
        form = ProductForm(request.POST)
        files = request.FILES.getlist('images')
        
        if form.is_valid():
            product = form.save(commit=False)
            product.added_by = request.user
            product.save()
            
            # Save images
            for i, img in enumerate(files):
                ProductImage.objects.create(
                    product=product,
                    image=img,
                    is_main=(i == 0),  # First image as main
                    alt_text=product.name
                )
            
            messages.success(request, 'Product added successfully!')
            return redirect('products:distributor_dashboard')
    else:
        form = ProductForm()
    
    return render(request, 'products/distributor/add_product.html', {'form': form})

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, added_by=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated!')
            return redirect('products:distributor_dashboard')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'products/distributor/edit_product.html', {'form': form, 'product': product})

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, added_by=request.user)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect('products:distributor_dashboard')