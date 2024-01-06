from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from product.models import User


class UserLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

