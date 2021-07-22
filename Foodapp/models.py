from django.conf.urls.static import static
from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.deletion import CASCADE
from django.forms.widgets import NumberInput
import datetime

# Create your models here.


class Food(models.Model):
    category = [('veg', 'vegitarian'), ('Non-veg', 'Non-vegitarian')]
    name = models.CharField(max_length=50)
    price = models.FloatField()
    quantity = models.IntegerField()
    types = models.CharField(max_length=30)
    category = models.CharField(choices=category, max_length=30)
    image = models.ImageField(upload_to='media', default='')

    class Meta:
        db_table = 'foodDB'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=50)
    number = models.CharField(max_length=10)

    class Meta:
        db_table = 'UserProfile'


customer, created = Group.objects.get_or_create(
    name='Customer')  # name=Customer is shown into browser
admin, createds = Group.objects.get_or_create(name='admin')
# line number 30 and 31 is used to create groups in our admin panel of django in browser
#print(customer, admin, created, createds)


class Cart(models.Model):
    currentuser = models.ForeignKey(User, on_delete=models.CASCADE)
    itemquantity = models.IntegerField(default=1)
    fid = models.ForeignKey(Food, on_delete=models.CASCADE)
    total = models.FloatField()

    class Meta:
        db_table = 'cart'


class OrderSummery1(models.Model):
    dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    statusChoices = [('Pending', 'Pending'), ('Delivered',
                                              'Delivered'), ('Cancel', 'Cancel')]
    date = models.CharField(default=str(dt), blank=True, max_length=25)
    totalamount = models.FloatField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=19, choices=statusChoices, default='Pending')

    class Meta:
        db_table = "ordersummery"


class Orders(models.Model):
    ordersobj = models.ForeignKey(OrderSummery1, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    total = models.IntegerField()
    foodQuant = models.IntegerField()

    class Meta:
        db_table = 'Orders'
