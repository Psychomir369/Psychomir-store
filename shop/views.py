from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib import messages
from django.db.models import Q
from payment.models import Order, OrderItem

def home(request):
    all_products = Product.objects.all()
    return render(request, 'index.html', {'products': all_products})

def about(request):
    return render(request, 'about.html')

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def category(request, cat):
    cat = cat.replace("-", " ")
    try:
        category = Category.objects.get(name=cat)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except:
        messages.success(request, "دسته بندی وجود ندارد!")
        return redirect("home")

def category_summary(request):
    all_cat = Category.objects.all()
    return render(request, 'category_summary.html', {'category': all_cat})

def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        if not searched:
            messages.success(request, "محصول مورد نظر شما یافت نشد!")
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched': searched})
    return render(request, 'search.html', {})

def user_orders(request):
    if request.user.is_authenticated:
        delivered_orders = Order.objects.filter(user=request.user, status='Delivered')
        other_orders = Order.objects.filter(user=request.user).exclude(status='Delivered')
        context = {
            'delivered': delivered_orders,
            'other': other_orders
        }
        return render(request, 'orders.html', context)
    else:
        messages.success(request, "دسترسی به این صفحه امکان پذیر نمی باشد!")
        return redirect('home')

def order_details(request, pk):
    if request.user.is_authenticated:
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order=pk)

        context = {
            'order': order,
            'items': items
        }
        return render(request, 'order_details.html', context)
    else:
        messages.success(request, "دسترسی به این صفحه امکان پذیر نمی باشد!")
        return redirect('home')