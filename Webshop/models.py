from django.db import models
from django.conf import settings
import stripe
from django.contrib.auth.models import AbstractUser

# Create your models here.

CATEGORY_CHOICES = (
    ('Outer wear', 'Outer wear'),
    ('Active wear', 'Active wear'),
    ('Swimwear', 'Swimwear'),
    ('Casual Wear', 'Casual Wear'),
    ('Bottoms', 'Bottoms'),
    ('Shirt and blouses', 'Shirt and blouses'),
    ('Sport Wear', 'Sport Wear'),
    ('Sleep wear', 'Sleep wear'),
    ('Shoes', 'Shoes'),
)

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=30)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title



class Product(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=100, null=True)
    price = models.FloatField()
    description = models.TextField()
    stock = models.IntegerField()
    imageurl = models.URLField()
    status = models.BooleanField(default=True)
    date_created = models.DateField(default=True)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=5, default='S')

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(auto_now=True, null=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"

    def get_products(self):
        return self.product.all()



class CartOrder(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    order_items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now=True)
    is_ordered = models.BooleanField(default=False)

    def get_cart_items(self):
        return self.order_items.all()

    def __str__(self):
        return self.owner.user.username


