from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from django.http import HttpResponse
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def _cart_id(request):
    session_key = request.session.session_key
    if not session_key:
        session_key = request.session.create()
    return session_key      

def add_to_cart(request, product_id):

    product_variation = []
    product = Product.objects.get(id=product_id)

    if request.method == "POST":
      
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
                print(product_variation)
                
            except:
                pass
               

    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    if cart_item_exists:
        cart_item = CartItem.objects.filter(cart=cart, product=product)
        # existing variations :comes from database
        # current variation : comes from product variation
        # item id : comes from database
        ex_var_list = []
        id = []
        
        for item in cart_item:
            existing_variation = item.variation.all()
            ex_var_list.append(list(existing_variation))
            print("existing variation list", ex_var_list)
            id.append(item.id)
            print("item id is", id)
    
        if product_variation in ex_var_list:
            # increase the cart item quantity
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
    
        else:
            item = CartItem.objects.create(product=product, quantity=1, cart=cart )             
            if len(product_variation) > 0:
                item.variation.clear()
                item.variation.add(*product_variation)
            item.save()
    else:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )  
        if len(product_variation) >0:   
            cart_item.variation.clear()
            cart_item.variation.add(*product_variation)
        cart_item.save()    


    return redirect('cart')

def remove_from_cart(request, product_id,cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass        
    return redirect('cart')    
  

def delete_cart_item(request, product_id, cart_item_id):   
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)     
    cart_item.delete() 
    return redirect('cart')



def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = 0.02 * total
        grand_total = total + tax    
    except ObjectDoesNotExist:
        pass
    context = {
        'grand_total': grand_total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'total':total,
    }        
    return render(request, 'store/cart.html', context)