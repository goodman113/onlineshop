
from calendar import leapdays
from unicodedata import name
from urllib import response
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,  logout
from .models import *
from django.http import JsonResponse, HttpResponse
import json
from .form import SignupForm
from django.contrib.auth.decorators import login_required
import requests
from functools import wraps


def homeView(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        category_id = data['cat_id']
        products = Products.objects.filter(category_id = category_id)
        data = []
        for i in products:
            data.append({
                'id': i.id,
                'name':i.name,
                'price':i.real_price(),
                'image':i.image.url
            })
        return JsonResponse({'data':data})
    if request.user.username:
        order, status = Orders.objects.get_or_create(customer=request.user, done_status=False)
        print(status)
        order_details = Order_details.objects.filter(order=order)
        total_price = sum([ i.real_price for i in order_details])
    else:
        order_details = []
        total_price = 0
    categories = Category.objects.all().order_by('id')
    hotproducts = Products.objects.all().order_by('-stock')
    products = Products.objects.filter(category=categories[0])
    data = []
    if request.user:
        wishlists = Wishlist.objects.filter(user=request.user)
        for i in wishlists:
            data.append(i.product.id)
    return render(request, 'index.html', {'category':categories, 'products':products, 'hotproduct':hotproducts, "order_details":order_details, 'soni':len(order_details), 'total_price':total_price, 'wishlist':data})
def productDetailView(request, id):
    try:
        product = Products.objects.get(id=id)
        likes = len(Wishlist.objects.filter(product=product, status=True))
        likestatus, status = Wishlist.objects.get_or_create(product=product, user=request.user)
    except Exception as e:
        print(e)
        return HttpResponse("<h1>Ushbu productimiz yo'q</h1>")
    return render(request, 'product_detail.html', {'product':product, 'likes':likes, 'likestatus':likestatus.status})

def login(request):
    error = ''
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        if request.user.is_authenticated:
            return redirect('home')
        user = authenticate(request=request,username=username, password=password)
        if user:
            login (request=request)
            return redirect('home')
        error = "In login and password you make mistake"
    return render(request, 'login.html', {'error':error})
def signup(request):
    form = SignupForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        form.save()
        user = authenticate(request=request, username=data['username'], password=data['password'])
        login(request=request, user=user)
        return redirect('home')
    return render(request, 'signup.html', context={'form':form})

# @login_required(login_url='/admin/')
def cartView(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data['product_id']
        order = Orders.objects.get(customer=request.user, done_status=False)
        order_details, status = Order_details.objects.get_or_create(order=order, product_id=product_id)
        if not (status):
            order_details.quantity=1
            order_details.save()
        return JsonResponse({'data':'ok'})
    # user = authenticate(request=request, username='admin2', password='muham1612mad')
    # login(request=request, user=user)
    order, status = Orders.objects.get_or_create(customer=request.user, done_status=False)
    print(status)
    order_details = Order_details.objects.filter(order=order)
    total_price = sum([ i.real_price for i in order_details])
    return render(request, 'cart.html', {'order_details':order_details, 'soni':len(order_details), 'total_price':total_price})

def quantChangeView(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data['order_det_id']
        quantity = data['quantity']
        order_det = Order_details.objects.get(id=id)
        order_det.quantity = int(quantity)
        order_det.save()
        return JsonResponse({'data':'ok'})

def cartDeleteView(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data['ord_det_id']
        Order_details.objects.get(id=id).delete()
        return JsonResponse({'data':'ok'})

def CheckoutView(request):
    if request.method == 'POST':
        print(request.POST)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        country_name = request.POST.get('country_name')
        viloyat = request.POST.get('viloyat')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        postal_code = request.POST.get('postal_code')
        order = Orders.objects.get(customer = request.user, done_status=False)
        order.first_name = first_name
        order.last_name = last_name
        order.email = email
        order.number = number
        order.viloyat = viloyat
        order.address1 = address1
        order.address2 = address2
        order.postal_code = postal_code
        order.done_status = True
        order.save()  
        token = "5283620123:AAFHxNxrFLGoswoBSzwAwIKOT9tsHWc9Xa8"
        method = 'sendMessage'
        text=  f"""
        davlati:{country_name}
        viloyat:{viloyat}
        phone:{number}
        address1 :{address1}
        address2 :{address2}
        email:{email}
        last_name: {last_name}
        first_name: {first_name}
        """
        order_details = Order_details.objects.filter(order=order)
        text+=f"Jami {len(order_details)} ta mahsulot zakaz berildi"
        sanoqchi = 1
        for i in order_details:
            text+="\n{sanoq}.{i.product.name} == {i.product.price}*{i.quantity} = {i.product.price*i.quantity}\n"
            sanoqchi+=1 
            i.price = i.product.price
            i.save()

        Jami = sum([i.product.price * i.quantity for i in order_details])
        text+=f"Jami: {Jami}"
        response = requests.post(
            url=f'https://api.telegram.org/bot{token}/{method}',
            data={'chat_id':-1001718176486, 'text':text}
        ).json()
        print(response)
        return redirect('home')


    order, status = Orders.objects.get_or_create(customer=request.user, done_status=False)
    print(status)
    order_details = Order_details.objects.filter(order=order)
    total_price = sum([ i.real_price for i in order_details])
    states = States.objects.all()
    country = Country.objects.all()
    return render(request, 'checkout.html', {'allsum':total_price, 'states':states, 'country':country})

def likeView(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data['product_id']
        wishlist, status = Wishlist.objects.get_or_create(product_id=product_id, user=request.user)
        wishlist.like = not (wishlist.product)
        wishlist.save()
        return JsonResponse({"like":wishlist.like})
