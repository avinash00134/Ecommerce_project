from django.db import models
from django.contrib.auth.models import AbstractUser,User
from taggit.managers import TaggableManager

class User(AbstractUser):
    is_customer = models.BooleanField('Is customer', default=False)
    is_seller = models.BooleanField('Is seller', default=False)
    mobilenumber = models.CharField(null=True,max_length=10)

class Category(models.Model):
    category_name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager()
    
    class Meta:
        verbose_name_plural = "Product"

    def __str__(self):
        return self.name

class Cart(models.Model):
    sample = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    quantity = models.IntegerField()
    total = models.FloatField()


class User_Details(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=120)
    lname = models.CharField(max_length=120)
    address = models.CharField(max_length=200)
    mobilenumber = models.IntegerField()
    email = models.EmailField(max_length=120)
    country = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    pincode = models.IntegerField()
    status = models.CharField(max_length=100)


class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    mobilenumber = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pincode = models.IntegerField()
    order_note = models.TextField(max_length=200, blank=True)
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_number

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class SearchQuery(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    query = models.CharField(max_length=220)
    timestamp = models.DateTimeField(auto_now_add=True)