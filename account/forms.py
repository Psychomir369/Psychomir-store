from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from shop.models import Profile

class SignupForm(UserCreationForm):
    first_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'نام'})
    )
    last_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'نام خانوادگی'})
    )
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'ایمیل'})
    )
    username = forms.CharField(
        label="",
        max_length=20,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'نام کاربری'})
    )
    phone = forms.CharField(
        label="",
        max_length=20,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'شماره تلفن'})
    )
    password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'name':'password',
            'type':'password',
            'placeholder':'رمز عبور'
        })
    )
    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'name':'password',
            'type':'password',
            'placeholder':'تأیید رمز عبور'
        })
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("این نام کاربری قبلاً ثبت شده است.")
        return username

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if Profile.objects.filter(phone=phone).exists():
            raise forms.ValidationError("این شماره تلفن قبلاً ثبت شده است.")
        return phone

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'phone', 'password1', 'password2')


class UpdateUserForm(UserChangeForm):
    password = None

    first_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'نام'}),
        required=False
    )
    last_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'نام خانوادگی'}),
        required=False
    )
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'ایمیل'}),
        required=False
    )
    username = forms.CharField(
        label="",
        max_length=20,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'نام کاربری'}),
        required=False
    )
    phone = forms.CharField(
        label="",
        max_length=20,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'شماره تلفن'}),
        required=False
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'phone')


class UpdatePasswordForm(SetPasswordForm):
    old_password = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'name':'password',
                'type':'password',
                'placeholder':'رمز عبور فعلی'
            }
        )
    )
    new_password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'name':'password',
                'type':'password',
                'placeholder':'رمز عبور جدید'
            }
        )
    )
    new_password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'name':'password',
                'type':'password',
                'placeholder':'تأیید رمز عبور جدید'
            }
        )
    )

    class Meta:
        model = User
        fields = ['old_password','new_password1','new_password2']


class UpdateUserInfo(forms.ModelForm):
    phone = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'شماره تلفن'}),
        required=False
    )
    address = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'آدرس'}),
        required=False
    )
    city = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'شهر'}),
        required=False
    )
    state = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'منطقه'}),
        required=False
    )
    zipcode = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'کد پستی'}),
        required=False
    )
    country = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'کشور'}),
        required=False
    )

    class Meta:
        model = Profile
        fields = ('phone','country','city','state','zipcode','address')