import datetime
from django.shortcuts import redirect, render

from carts.models import CartItem
from orders.forms import OrderForm
from orders.models import Order

# Create your views here.
def place_order(request):
    current_user = request.user

    # first check if the cart_count is greater than zero
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    total = 0
    grand_total = 0
    tax = 0
    quantity = 0
    for cart_item in cart_items:
        total += (cart_item.quantity * cart_item.product.price)
        quantity += cart_item.quantity
    tax = (0.2 * total)
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)    
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']   
            data.state = form.cleaned_data['state']                                                                        
            data.city = form.cleaned_data['city']                                                                        
            data.order_note = form.cleaned_data['order_note']                                                                        
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            yr = int(datetime.datetime.today().strftime('%Y'))
            dt = int(datetime.datetime.today().strftime('%d'))
            mt = int(datetime.datetime.today().strftime('%m'))   
            d = datetime.date(yr,mt,dt)         
            current_date = d.strftime("%Y%m%d") 

            order_number = current_date + str(data.id)
            data.order_number = order_number                    
            data.save()
            return redirect('checkout')
        else:
            return redirect('checkout')