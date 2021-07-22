from django.contrib import admin
from .models import Food, UserProfile, Cart, OrderSummery1, Orders
# Register your models here.
admin.site.register(Food)
admin.site.register(UserProfile)
admin.site.register(Cart)
admin.site.register(OrderSummery1)
admin.site.register(Orders)
