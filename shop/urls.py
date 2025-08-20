from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('product/<int:pk>', views.product, name="product"),
    path('category/<str:cat>', views.category, name="category"),
    path('category/', views.category_summary, name="category_summary"),
    path('search/', views.search, name="search"),
    path('orders/', views.user_orders, name="orders"),
    path('order_details/<int:pk>', views.order_details, name="order_details"),
]