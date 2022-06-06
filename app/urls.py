from django.urls import path
from .views import *
urlpatterns = [
    path('', homeView, name='home'),
    path('login.html/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('product/<int:id>', productDetailView, name='prdetail'),
    path('cart/', cartView, name='cart'),
    path('quantitychange/',quantChangeView, name='quanntychange'),
    path('cart-delete/', cartDeleteView, name='quanntychange'),
    path('checkout', CheckoutView, name='checkout'),
    path('like', likeView,  name='like')
]