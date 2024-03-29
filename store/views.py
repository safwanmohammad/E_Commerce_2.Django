from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,ReviewRating,productGallery,VariationPrice,Variation
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Q
from .forms import  ReviewForm
from django.contrib import messages
from orders.models import OrderProduct
# Create your views here.

def store(request,category_slug=None):
    categories = None
    Products = None

    if category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug)
        Products = Product.objects.filter(category=categories,is_available=True)
        paginator = Paginator(Products,4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        Products_count = Products.count()
    else:
        Products = Product.objects.all().filter(is_available=True).order_by('-product_name')
        paginator = Paginator(Products,8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        Products_count = Products.count()

    
    context = {
        'categories':categories,
        'Products':paged_products,
        'Products_count':Products_count,
    }

    return render(request, 'store/store.html',context)

def product_detail(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product =single_product).exists()
    except Exception as e:
        raise e
    if request.user.is_authenticated:
        try:
            order_product = OrderProduct.objects.filter(user=request.user,product_id =single_product.id).exists()
        except OrderProduct.DoesNotExist:
            order_product =None
    else:
        order_product =None

    # get the review
    reviews = ReviewRating.objects.filter(product_id=single_product.id,status=True)

    # get the product gallary
    product_gallary = productGallery.objects.filter(product_id=single_product.id)
    product_price = VariationPrice.objects.all().filter(product_id=single_product.id,)
    # adding price list to the template
    variation_prices = VariationPrice.objects.filter(product_id=single_product.id,is_active=True)
    var_prices = []
    for variation_price in variation_prices:
        variation_category = variation_price.variation_category
        var_price = variation_price.var_price
        var_prices.append(var_price)
        var_prices.sort()
        print(var_prices)
        print(f"Variation Category: {variation_category}")
        print(f"Variation Price: {var_price}")
        print()
    
    context = {
        # 'variation_category':variation_category,
        'var_prices':var_prices,
        'variation_prices':variation_prices,
        'single_product':single_product,
        'in_cart': in_cart,
        'order_product':order_product,  
        'reviews':reviews,
        'product_gallary':product_gallary,
        'product_price':product_price,
    }

    return render(request,'store/product_detail.html',context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            Products = Product.objects.order_by('-created_date').filter(Q(description__icontains = keyword) | Q(product_name__icontains = keyword))
            Products_count = Products.count()
    context = {
        'Products': Products,
        'Products_count':Products_count,
    }
    return render(request, 'store/store.html',context)

def submit_review(request,product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method =="POST":
        try:
            reviews =ReviewRating.objects.get(user__id=request.user.id,product__id=product_id)
            form = ReviewForm(request.POST,instance=reviews)
            form.save()
            messages.success(request,'Thank you! Your review has been updated')
            return redirect(url)
        except:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request,'Thank you! Your review has been submited')
                return redirect(url)
