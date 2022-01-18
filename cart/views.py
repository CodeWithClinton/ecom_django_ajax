from django.shortcuts import render
from .models import Product, Cart, Cartitems
from django.http import JsonResponse
import json

# Create your views here.
def store(request):
    if request.user.is_authenticated:
        customer = request.user
        cart, created = Cart.objects.get_or_create(owner=customer, completed = False)
        cartitems = cart.cartitems_set.all()
    else:
        cart = []
        cartitems = []
        cart = {'cartquantity': 0}

    products = Product.objects.all()
    context = {'products': products, 'cart': cart, 'cartitems': cartitems}
    return render(request, 'cart/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        cart, created = Cart.objects.get_or_create(owner=customer, completed = False)
        cartitems = cart.cartitems_set.all()
    else:
        cart = []
        cartitems = []
        cart = {'cartquantity': 0}
    context = {'cart': cart, 'cartitems': cartitems}
    return render(request, 'cart/cart.html', context)

def updateCart(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']
    if request.user.is_authenticated:
        customer = request.user
        product = Product.objects.get(product_id= product_id)
        cart, created = Cart.objects.get_or_create(owner=customer, completed=False)
        cartitems, created = Cartitems.objects.get_or_create(product=product, cart=cart)

        if action == 'add':
            cartitems.quantity += 1
        cartitems.save()

        msg = {
            'quantity': cart.cartquantity
        }

    return JsonResponse(msg, safe=False)

def updateQuantity(request):
    data = json.loads(request.body)
    inputval = int(data['in_val'])
    product_id = data['p_id']
    if request.user.is_authenticated:
        customer = request.user
        product = Product.objects.get(product_id= product_id)
        cart, created = Cart.objects.get_or_create(owner=customer, completed=False)
        cartitems, created = Cartitems.objects.get_or_create(product=product, cart=cart)

        cartitems.quantity = inputval
        cartitems.save()

        msg = {
            'subtotal':cartitems.subtotal,
            'grandtotal': cart.grandtotal,
            'quantity': cart.cartquantity
        }

    return JsonResponse(msg, safe=False)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        cart, created = Cart.objects.get_or_create(owner=customer, completed = False)
        cartitems = cart.cartitems_set.all()
    else:
        cart = []
        cartitems = []
        cart = {'cartquantity': 0}
    context = {'cart': cart, 'cartitems': cartitems}
    return render(request, 'cart/checkout.html', context)

def payment(request):
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user
        cart, created = Cart.objects.get_or_create(owner=customer, completed=False)
        total = float(data['cart_total'])
        
        if total == cart.grandtotal:
            cart.completed = True
            cart.save()
        
        
        
    return JsonResponse('It is working', safe=False)