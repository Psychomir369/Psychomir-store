from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('login/signup/', views.signup_user, name="signup"),
    path('login/login_phone/', views.login_phone_user, name='login_phone'),
    path('verify_code/', views.verify_code, name='verify_code'),
    path('update_user/', views.update_user, name="update_user"),
    path('update_info/', views.update_info, name="update_info"),
    path('update_send/', views.update_send, name="update_send"),
    path('update_password/', views.update_password, name="update_password"),
]