from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    phone_number = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to='users_avatars', blank=True)


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to='categories_images')

    def count_product(self):
        return Product.objects.filter(category=self).count()

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='products_images')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.title


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.title}'