// Global Variables
let cartCount = parseInt(document.querySelector('[data-cart-count]')?.dataset.cartCount || 0);

// Document Ready
$(document).ready(function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Add to Cart AJAX
    $('.add-to-cart-form').on('submit', function(e) {
        e.preventDefault();
        
        let form = $(this);
        let button = form.find('button[type="submit"]');
        let originalText = button.html();
        
        // Show loading state
        button.prop('disabled', true).html('<span class="spinner-border spinner-border-sm"></span> Adding...');
        
        $.ajax({
            url: form.attr('action'),
            method: 'POST',
            data: form.serialize(),
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function(response) {
                if (response.success) {
                    // Update cart count
                    updateCartCount(response.cart_count);
                    
                    // Show success message
                    showToast('success', response.message);
                    
                    // Update cart total if on cart page
                    if (typeof updateCartTotal === 'function') {
                        updateCartTotal(response);
                    }
                }
            },
            error: function(xhr) {
                showToast('error', 'Failed to add item to cart');
            },
            complete: function() {
                // Restore button
                button.prop('disabled', false).html(originalText);
            }
        });
    });
    
    // Quantity update
    $('.quantity-input').on('change', function() {
        let input = $(this);
        let itemId = input.data('item-id');
        let quantity = parseInt(input.val()) || 1;
        
        if (quantity < 1) {
            input.val(1);
            quantity = 1;
        }
        
        updateCartItem(itemId, quantity);
    });
    
    $('.quantity-btn').on('click', function() {
        let btn = $(this);
        let input = btn.closest('.quantity-wrapper').find('.quantity-input');
        let itemId = input.data('item-id');
        let currentVal = parseInt(input.val()) || 1;
        
        if (btn.hasClass('plus')) {
            input.val(currentVal + 1);
        } else if (btn.hasClass('minus') && currentVal > 1) {
            input.val(currentVal - 1);
        }
        
        updateCartItem(itemId, parseInt(input.val()));
    });
    
    // Wishlist toggle
    $('.wishlist-btn').on('click', function(e) {
        e.preventDefault();
        
        let btn = $(this);
        let productId = btn.data('product-id');
        let icon = btn.find('i');
        
        $.ajax({
            url: `/products/wishlist/toggle/${productId}/`,
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function(response) {
                if (response.added) {
                    icon.removeClass('far').addClass('fas');
                    showToast('success', 'Added to wishlist');
                } else {
                    icon.removeClass('fas').addClass('far');
                    showToast('success', 'Removed from wishlist');
                }
            },
            error: function() {
                showToast('error', 'Failed to update wishlist');
            }
        });
    });
    
    // Auto-dismiss alerts
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);
    
    // Price range filter
    let priceRange = $('#priceRange');
    if (priceRange.length) {
        let minPrice = $('#minPrice');
        let maxPrice = $('#maxPrice');
        
        priceRange.on('input', function() {
            let value = $(this).val();
            maxPrice.val(value);
        });
    }
});

// Functions
function updateCartItem(itemId, quantity) {
    $.ajax({
        url: `/cart/update/${itemId}/`,
        method: 'POST',
        data: {
            quantity: quantity,
            csrfmiddlewaretoken: getCookie('csrftoken')
        },
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        },
        success: function(response) {
            if (response.success) {
                // Update item total
                $(`#item-total-${itemId}`).text('₹' + response.item_total);
                
                // Update cart total
                $('#cart-total').text('₹' + response.cart_total);
                
                // Update cart count
                updateCartCount(response.cart_count);
                
                // Show toast
                showToast('success', 'Cart updated');
            }
        },
        error: function() {
            showToast('error', 'Failed to update cart');
        }
    });
}

function updateCartCount(count) {
    let cartBadge = $('.navbar .fa-shopping-cart').siblings('.badge');
    
    if (count > 0) {
        if (cartBadge.length) {
            cartBadge.text(count);
        } else {
            $('.navbar .fa-shopping-cart').parent().append(
                `<span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">${count}</span>`
            );
        }
    } else {
        cartBadge.remove();
    }
}

function showToast(type, message) {
    let toastContainer = $('.toast-container');
    
    if (!toastContainer.length) {
        toastContainer = $('<div class="toast-container"></div>').appendTo('body');
    }
    
    let toastClass = 'custom-toast ';
    let icon = '';
    
    switch(type) {
        case 'success':
            toastClass += 'bg-success text-white';
            icon = '<i class="fas fa-check-circle"></i>';
            break;
        case 'error':
            toastClass += 'bg-danger text-white';
            icon = '<i class="fas fa-exclamation-circle"></i>';
            break;
        case 'warning':
            toastClass += 'bg-warning';
            icon = '<i class="fas fa-exclamation-triangle"></i>';
            break;
        default:
            toastClass += 'bg-info text-white';
            icon = '<i class="fas fa-info-circle"></i>';
    }
    
    let toast = $(`<div class="${toastClass}">${icon} ${message}</div>`);
    toastContainer.append(toast);
    
    setTimeout(function() {
        toast.fadeOut(function() {
            $(this).remove();
        });
    }, 3000);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Loading spinner
function showLoading() {
    $('.spinner-wrapper').addClass('show');
}

function hideLoading() {
    $('.spinner-wrapper').removeClass('show');
}

// Image gallery for product detail
function initImageGallery() {
    $('.thumbnail-img').on('click', function() {
        let src = $(this).data('large');
        $('#main-product-image').attr('src', src);
        
        $('.thumbnail-img').removeClass('active');
        $(this).addClass('active');
    });
}

// Checkout form validation
function validateCheckout() {
    let isValid = true;
    
    $('.required-field').each(function() {
        if (!$(this).val()) {
            $(this).addClass('is-invalid');
            isValid = false;
        } else {
            $(this).removeClass('is-invalid');
        }
    });
    
    return isValid;
}

// Export functions for use in other scripts
window.WearHub = {
    showToast: showToast,
    showLoading: showLoading,
    hideLoading: hideLoading,
    updateCartCount: updateCartCount
};