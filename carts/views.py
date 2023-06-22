from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product,Variation
from . models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
# Create your views here.

def _cart_id(req):
    cart = req.session.session_key
    if not cart:
        cart = req.session.create()
    return cart

def add_cart(req,product_id):
    product = Product.objects.get(id=product_id) #get the product detail
    product_variation = []
    if req.method == "POST":
        for item in req.POST:
            key = item
            value = req.POST[key]   
            try:
                variation = Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass
    try:
        cart = Cart.objects.get(cart_id = _cart_id(req)) #get the cart  using _cart_id presend in the session 
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(req)
        )
    cart.save()

    is_cart_item_exists = CartItem.objects.filter(product=product,cart=cart).exists()

    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product,cart=cart)
        # existing variations -> Database
        # current variation -> product_variation
        # item_id -> Databse
        ex_var_list = []
        id = []
        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)
        print(ex_var_list)

        if product_variation in ex_var_list:
            #increse the cart item quntity
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product,id=item_id)
            item.quantity += 1
            item.save()
        else:
            # craete new cart item
            item = CartItem.objects.create(product=product,quantity=1,cart=cart)
            if len(product_variation) > 0 :
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()    
    else:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        if len(product_variation) > 0 :
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()
    return redirect('cart')

def remove_cart(request,product_id,cart_item_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product,id=product_id)

    try:
        cart_item = CartItem.objects.get(product=product,cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request,product_id,cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product,id=product_id)
    cart_item = CartItem.objects.get(cart=cart,product=product,id=cart_item_id)
    cart_item.delete()
    return redirect('cart')
    

def cart(request,total=0,quantity=0,cart_items=None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for cartItem in cart_items:
            total += (cartItem.product.price * cartItem.quantity)
            quantity += cartItem.quantity
        tax = (5 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore
    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
    }
    return render(request, 'store/cart.html',context)