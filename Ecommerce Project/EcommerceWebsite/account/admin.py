from django.contrib import admin

from . models import User,Product,Category,Cart,User_Details,Order,OrderItem
# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(User_Details)
admin.site.register(Order)
admin.site.register(OrderItem)