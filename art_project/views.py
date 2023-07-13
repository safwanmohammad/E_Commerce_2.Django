from django.shortcuts import get_object_or_404, render
from store.models import Product
from store.models import ReviewRating
from category.models import Category
from django.core.paginator import Paginator
def home(request):
    products = Product.objects.all().filter(is_available=True).order_by('-created_date')
    category = Category.objects.all()
    print(category)
    
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id,status=True)
    context = {
        'products':products,
        'reviews':reviews,
        'category':category,
    }
    return render(request,'home.html',context)