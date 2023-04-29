from django.shortcuts import render, redirect
from store.models import Product
from django.http import HttpResponse
from .models import Cart, CartItem
# Create your views here.

def _cart_id(request):
    session_key = request.session.session_key
    if not session_key:
        session_key = request.session.create()
    return session_key      

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()


    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity+= 1
        cart_item.save()
    
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=1,
        )
        cart_item.save()

    return redirect('cart')




def cart(request):
    return render(request, 'store/cart.html')