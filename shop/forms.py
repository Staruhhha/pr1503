import re
from django.core.exceptions import ValidationError
from django import forms
from shop.models import *

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = (
            'name',
            'representor_surname',
            'representor_name',
            'representor_patronymic',
            'representor_phone_number',
            'address'
        )
    def clean_representor_phone_number(self):
        representor_phone_number = self.cleaned_data['representor_phone_number']
        if re.match(r'\+7\(\d{3}\)\d{3}-\d{2}-\d{2}', representor_phone_number):
            return representor_phone_number
        raise ValidationError('Телефон должен быть прописан в формате +7(___)___-__-__')

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            'name',
            'description'
        )

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        min_length=2
    )
    email = forms.CharField(
        label='Адрес электронной почты',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label='Придумайте пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Подтвердите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        min_length=2
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class ContactForm(forms.Form):
    subject = forms.CharField(
        label='Заголовок письма',
        widget=forms.TextInput(
            attrs={'class': 'form-control',},
        ),
    )
    content = forms.CharField(
        label='Текст письма',
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': 11,}
        )
    )
