def cart_processor(request):
    """
    Makes cart count available globally in all templates.
    """
    cart = request.session.get('cart', {})
    count = sum(cart.values())
    return {'cart_count': count}