from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='App'),
    path('user_page', views.user, name='user_page'),
    path('user_signup', views.SignupPage, name='user_signup'),
    path('user_login', views.login,name='user_login'),
    path('search_view', views.search_view,name='search_view'),
    path('add_to_cart',views.add_to_cart_view,name='add_to_cart'),
    path('cart_view',views.cart_view,name='cart_view'),
    path('remove_from_cart',views.remove_from_cart_view,name='remove_from_cart')
]