from django.shortcuts import render, redirect
from shop.models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignupForm, UpdateUserForm, UpdatePasswordForm, UpdateUserInfo
import json
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
            messages.success(request, ("با موفقیت وارد شدید!"))
            return redirect("home")
        else:
            messages.success(request, ("مشکلی هنگام ورود شما رخ داد!"))
            return redirect("login")
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, ("با موفقیت خارج شدید!"))
    return redirect("home")

def signup_user(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                profile = Profile.objects.get(user=user)
                profile.phone = form.cleaned_data['phone']
                profile.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(request, username=username, password=password)
                login(request, user)
                messages.success(request, "ثبت نام با موفقیت انجام شد!")
                return redirect("update_info")
            except Exception as e:
                messages.error(request, f"خطا در ثبت نام: {str(e)}")
                return redirect("signup")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
            return render(request, 'signup.html', {'form': form})
    else:
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})

def login_phone_user(request):
    if request.method == "POST":
        phone = request.POST['phone']
        try:
            profile = Profile.objects.get(phone=phone)
            if profile:
                user = profile.user
                verification_code = generate_verification_code()
                request.session['verification_code'] = verification_code
                request.session['user_id'] = user.id
                request.session['phone'] = phone
                messages.success(request, 'کد تأیید برای شما ارسال شد.')
                return redirect('verify_code')
        except Profile.DoesNotExist:
            messages.error(request, "شما هنوز ثبت نام نکرده‌اید. ابتدا ثبت نام کنید.")
            return redirect('signup')
    return render(request, 'login_phone.html')

def verify_code(request):
    if request.method == 'POST':
        entered_code = request.POST['verification_code']
        stored_code = request.session.get('verification_code')
        if entered_code == stored_code:
            user_id = request.session.get('user_id')
            user = User.objects.get(id=user_id)
            login(request, user)
            current_user = Profile.objects.get(user__id=user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
            del request.session['verification_code']
            del request.session['user_id']
            del request.session['phone']
            messages.success(request, "با موفقیت وارد شدید!")
            return redirect("home")
        else:
            messages.error(request, "کد تأیید اشتباه است.")
            return redirect('verify_code')
    return render(request, 'verify_code.html')

def generate_verification_code():
    import random
    code = str(random.randint(100000, 999999))
    print(f"کد تأیید: {code}")
    return code

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        current_profile = Profile.objects.get(user__id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if request.method == 'POST':
            if user_form.is_valid():
                user = user_form.save()
                phone = user_form.cleaned_data.get('phone')
                current_profile.phone = phone
                current_profile.save()
                login(request, user)
                messages.success(request, 'اطلاعات شما با موفقیت ویرایش شد!')
                return redirect("home")
        user_form.initial['phone'] = current_profile.phone
        return render(request, 'update_user.html', {'user_form': user_form})
    else:
        messages.success(request, 'ابتدا باید وارد شوید!')
        return redirect("home")

def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UpdateUserInfo(request.POST or None, instance=current_user)
        if form.is_valid():
            form.save()
            messages.success(request, 'اطلاعات کاربری شما با موفقیت ذخیره شد!')
            return redirect("home")
        return render(request, 'update_info.html', {'form': form})
    else:
        messages.success(request, 'ابتدا باید وارد شوید!')
        return redirect("home")

def update_send(request):
    if request.user.is_authenticated:
        shipping_user, created = ShippingAddress.objects.get_or_create(
            user=request.user
        )
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        if request.method == 'POST' and shipping_form.is_valid():
            shipping_form.save()
            messages.success(request, 'اطلاعات ارسال شما با موفقیت ذخیره شد!')
            return redirect("home")
        
        return render(request, 'update_send.html', {'shipping_form': shipping_form})
    else:
        messages.success(request, 'ابتدا باید وارد شوید!')
        return redirect("home")

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = UpdatePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'رمز عبور با موفقیت ویرایش شد!')
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, 'مشکلی هنگام ویرایش رمز شما رخ داد!')
                    return redirect('update_password')
        else:
            form = UpdatePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.success(request, 'ابتدا باید وارد شوید!')
        return redirect("home")