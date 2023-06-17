from django.shortcuts import render,get_object_or_404
from .models import Product
from category.models import Category
# Create your views here.

def store(request,category_slug=None):
    categories = None
    Products = None

    if category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug)
        Products = Product.objects.filter(category=categories,is_available=True)
        Products_count = Products.count()
    else:
        Products = Product.objects.all().filter(is_available=True)
        Products_count = Products.count()

    
    context = {
        'Products':Products,
        'Products_count':Products_count
    }

    return render(request, 'store/store.html',context)

def product_detail(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
    except Exception as e:
        raise e
    context = {
        'single_product':single_product,
    }

    return render(request,'store/product_detail.html',context)