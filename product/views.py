from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib import auth
from django.views.generic import CreateView
from pyexpat.errors import messages

from product.forms import UserLoginForm, UserRegisterForm
from product.models import Product, Category, User, Basket


# Create your views here.

class IndexView(View):
    def get(self, request):
        category_id = request.GET.get('category_id', None)
        if category_id is not None:
            products = Product.objects.filter(category_id=category_id).order_by('-id')[:12]
        else:
            products = Product.objects.all().order_by('-id')[:12]
        category = Category.objects.all()
        context = {
            'title': 'Главная',
            'products': products,
            'category': category,
        }
        return render(request, 'product/index.html', context=context)


class ProductsView(View):
    def get(self, request):
        category_id = request.GET.get('category_id', None)
        brand = request.GET.get('brand', None)
        if category_id is not None:
            category = Category.objects.get(id=category_id)
            products = Product.objects.filter(category=category).order_by('-id')
        elif brand is not None:
            products = Product.objects.filter(brand=brand).order_by('-id')
        else:
            products = Product.objects.all().order_by('-id')
        category = Category.objects.all()
        context = {
            'title': 'Продукты',
            'products': products,
            'categoryes': category,
        }
        return render(request, 'product/products.html', context=context)


class LoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'product/login.html'
    success_url = reverse_lazy('index')

# class LoginView(View):
#     def get(self, request):
#         form = UserLoginForm()
#         context = {
#             'title': 'Авторизация',
#             'form': form,
#         }
#         return render(request, 'product/login.html', context=context)
#
#     def post(self, request):
#         form = UserLoginForm(data=request.POST)
#         print(form)
#         if form.is_valid():
#
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#         context = {
#             'title': 'Авторизация',
#             'form': form,
#         }
#         return render(request, 'product/login.html', context=context)


class LogoutView(View):
    """
    View for handling logout requests.

    This view logs out the user from the current session and redirects
    to the index page.
    """

    def get(self, request):
        auth.logout(request)
        return HttpResponseRedirect(reverse('index'))


class RegisterUserView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'product/register.html'
    success_url = reverse_lazy('product:login')

    def get_context_data(self, **kwargs):
        context = super(RegisterUserView, self).get_context_data()
        context['title'] = 'Регистрация'
        return context


# class RegisterUserView(View):
#
#     def get(self, request):
#         form = UserRegisterForm()
#         context = {
#             'title': 'Регистрация',
#             'form': form
#         }
#         return render(request, 'product/register.html', context=context)
#
#     def post(self, request):
#         form = UserRegisterForm(data=request.POST)
#         print(form)
#         if form.is_valid():
#             form.save()
#             # messages.success(request, 'Вы зарегистрировались. Теперь вы можете войти.')
#             return HttpResponseRedirect(reverse('product:login'))
#         context = {
#             'title': 'Регистрация',
#             'form': form
#         }
#         return render(request, 'product/register.html', context=context)


class ProfileView(View):
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        basket = Basket.objects.filter(user=user).order_by('-created_timestamp')
        context = {
            'title': 'Профиль',
            'user': user,
            'basket': basket,
        }
        return render(request, 'product/profile.html', context=context)


class BasketAdd(View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        basket = Basket.objects.filter(user=request.user, product=product)
        if not basket.exists():
            Basket.objects.create(user=request.user, product=product, quantity=1)
        else:
            basket = basket.first()
            basket.quantity += 1
            basket.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
