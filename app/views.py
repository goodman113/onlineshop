
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .models import *
from django.http import JsonResponse, HttpResponse
import json
from .form import SignupForm
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
    return render(request, 'index.html', {'category':categories, 'products':products, 'hotproduct':hotproducts, "order_details":order_details, 'soni':len(order_details), 'total_price':total_price})
def productDetailView(request, id):
    try:
        product = Products.objects.get(id=id)
    except Exception as e:
        print(e)
        return HttpResponse("<h1>Ushbu productimiz yo'q</h1>")
    return render(request,'product_detail.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        if request.user.is_authenticated:
            return redirect('home')
        user = authenticate(request=request,username=username, password=password)
        print(user)
        if user:
            login (request=request)# login (request=request, user=user)
            return redirect('home')
    return render(request, 'login.html')
def signup(request):
    form = SignupForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        form.save()
        print(data)
        user = authenticate(request=request, username=data['username'], password=data['password'])
        print(user)
        login(request=request, user=user)
        return redirect('home')
    return render(request, 'signup.html', context={'form':form})


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
    return render(request, 'checkout.html', {})