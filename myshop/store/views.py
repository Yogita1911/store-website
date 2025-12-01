from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Product

# --- Traditional Django Views (MVT) ---

def product_list(request):
    """Displays all products and demonstrates cookie setting."""
    products = Product.objects.all()
    response = render(request, 'product_list.html', {'products': products})
    
    # COOKIE DEMONSTRATION:
    # Explicitly setting a non-session cookie. 
    # Check browser dev tools -> Application -> Cookies to see this.
    if 'visited_store_before' not in request.COOKIES:
        response.set_cookie('visited_store_before', 'true', max_age=3600) # Expires in 1 hour
        print("Setting first-visit cookie!")
        
    return response

def add_to_cart(request, product_id):
    """
    SESSION MANAGEMENT CORE:
    Adds items to a session-based cart dictionary.
    The cart looks like: {'product_id_1': quantity, 'product_id_2': quantity}
    """
    product = get_object_or_404(Product, id=product_id)
    
    # 1. Get existing cart from session, or create empty dict if none exists
    cart = request.session.get('cart', {})
    
    product_id_str = str(product_id) # Dictionary keys should be strings in JSON sessions

    # 2. Update quantity
    if product_id_str in cart:
        cart[product_id_str] = cart[product_id_str] + 1
    else:
        cart[product_id_str] = 1
        
    # 3. SAVE back to session (Crucial step!)
    request.session['cart'] = cart
    # Tell Django the session data changed (sometimes needed for dicts/lists)
    request.session.modified = True 
    
    messages.success(request, f"{product.name} added to cart.")
    return redirect('product_list')

def view_cart(request):
    """Retrives session cart data and meshes it with actual database objects."""
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        total = product.price * quantity
        total_price += total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': total
        })

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'cart.html', context)

def clear_cart(request):
    """Demonstrates clearing session data."""
    if 'cart' in request.session:
        del request.session['cart']
        messages.info(request, "Cart cleared.")
    return redirect('view_cart')

# --- DRF API Views (To be added next step) ---
# ... imports at top need: from rest_framework import generics
from rest_framework import generics
from .serializers import ProductSerializer

# --- DRF API Views ---

class ProductListAPI(generics.ListAPIView):
    """
    Shows JSON data representing the products.
    Useful for mobile apps or React/Vue frontends.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
