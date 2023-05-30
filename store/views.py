from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from orders.models import OrderProduct
from store.forms import ReviewForm
from .models import Product, ProductGallery, ReviewRating
from carts.models import  CartItem
from carts.views import _cart_id
from category.models import Category
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug !=None:
        categories = get_object_or_404(Category, category_slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).order_by('id')
        paginator = Paginator(products, 4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()
    else:    
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 4)
        page = request.GET.get('page')
    
        paged_products = paginator.get_page(page)
        products_count = products.count()
    context = {
       'products':paged_products,
       'products_count': products_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__category_slug=category_slug, product_slug=product_slug )
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()

    except Exception as e:
        raise e
    if request.user.is_authenticated:
        try:
            orderedproduct = OrderProduct.objects.filter(user=request.user, product__id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderedproduct = None
    else:
        orderedproduct = None
    # get the reviews
    reviews = ReviewRating.objects.filter(product__id=single_product.id, status=True) 

    # get the product gallery.
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)
    context  ={
        'single_product': single_product,
        'in_cart':in_cart,
       'orderedproduct':orderedproduct,
       'reviews':reviews,
       'product_gallery':product_gallery,
    }

    return render(request, 'store/product_detail.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))

        products_count = products.count()    

    context = {
        'products': products,
        'products_count':products_count,
        'keyword': keyword,
    }         
    return render(request, 'store/store.html', context)


def submit_review(request, product_id=None):
    if request.method == 'POST':
        url = request.META.get('HTTP_REFERER')
        
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Review updated successfully')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.product_id = product_id
                data.user_id = request.user.id
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.ip = request.META.get('REMOTE_ADDR')
                data.save()
                messages.success(request, 'Review for this product added successfully')
                return redirect(url)
