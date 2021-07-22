from django.db.models.aggregates import Count
from django.forms.forms import Form
from django.http import request
from django.shortcuts import redirect, render
from . import forms
from django.http import JsonResponse
from .models import Food, UserProfile,  Cart, OrderSummery1, Orders
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum, Count
import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import size
from django_pandas.io import read_frame
import seaborn as sns
# Create your views here.


def index(req):
    count = Cart.objects.filter(currentuser=req.user).count()
    return render(req, 'Foodapp/index.html', {'count': count})


def addFood(req):
    form = forms.Foodform()
    print("/////", form)
    if req.method == "POST":
        form = forms.Foodform(req.POST, req.FILES)
        if form.is_valid():
            print("//////", form)
            form.save(commit=True)
    #count = Cart.objects.filter(currentuser=req.user).count()
    return render(req, 'Foodapp/addfood.html', {'form': form})


def menu(request):
    food = Food.objects.all()
    cartid = Cart.objects.filter(currentuser=request.user).values_list('fid')
    print('CART ID ', cartid)
    cartdata = []
    for i in cartid:
        cartdata.append(i[0])
    print('#$#$#$#$#$#$', cartdata)
    count = Cart.objects.filter(currentuser=request.user).count()
    return render(request, 'Foodapp/menu.html', {'food': food, 'cartdata': cartdata, 'count': count})


def Deletefood(req, id):
    food = Food.objects.filter(id=id)
    food.delete()
    #count = Cart.objects.filter(currentuser=req.user).count()
    return redirect('/showfood')


# @permission_required('Foodapp.chage_food', login_url='/loginUser')
def Updatefood(req, id):
    food = Food.objects.get(id=id)
    print(food)
    form = forms.Foodform()
    print('####', form)

    if req.method == "POST":
        form = forms.Foodform(req.POST, req.FILES, instance=food)
        if form.is_valid():
            print("/////", form)
            form.save(commit=True)
            return redirect('/showfood')
    count = Cart.objects.filter(currentuser=req.user).count()
    return render(req, 'Foodapp/updatefood.html', {'food': food, 'count': count})


def CreateUser(req):
    form = forms.UserForm()
    form1 = forms.UserProfileForm()
    if req.method == 'POST':
        form = forms.UserForm(req.POST)
        form1 = forms.UserProfileForm(req.POST)
        role = req.POST['Role']
        print(role)
        if form.is_valid() and form1.is_valid():
            user = form.save(commit=True)
            Userprofile = form1.save(commit=False)
            user.set_password(user.password)
            user.save()
            Userprofile.user = user
            Userprofile.save()
            if role == 'customersss':
                print('printing customer', role)
                cust = Group.objects.get(name='Customer')
                user.groups.add(cust)
            elif role == 'adminsss':
                print('printing admin', role)
                admin = Group.objects.get(name='admin')
                user.groups.add(admin)
            return redirect('/login')
    count = Cart.objects.filter(currentuser=req.user).count()
    return render(req, 'Foodapp/register.html', {'form': form, 'form1': form1, 'count': count})


def showUsers(req):
    data = UserProfile.objects.all()
    count = Cart.objects.filter(currentuser=req.user).count()
    return render(req, 'Foodapp/customer.html', {'data': data, 'count': count})


def logins(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request. POST['username']
        password = request. POST['password']
        user = authenticate(username=username, password=password)
        print(username, user)

        if user != None:
            print(user)
            login(request, user)
            return redirect('/index')

        else:
            msg = 'username or password is worng'
            print('hello')
            return render(request, 'Foodapp/login.html', {'form': form, 'msg': msg})
    #count = Cart.objects.filter(currentuser=request.user).count()
    return render(request, 'Foodapp/login.html', {'form': form})


def logouts(req):
    print('logout...........')
    logout(req)
    return render(req, 'Foodapp/index.html')


def userprofile(req):
    currentuser = req.user
    data1 = UserProfile.objects.get(user=currentuser)
    # User is built in model class auth application
    data2 = User.objects.get(username=currentuser)
    qset = Group.objects.get(user=currentuser)
    role = qset.name
    count = Cart.objects.filter(currentuser=req.user).count()
    return render(req, 'Foodapp/profile.html', {'data1': data1, 'data2': data2, 'role': role, 'count': count})


def updatecart(request):
    quantity = request.POST.get('q')
    price = request.POST.get('p')
    print('PRICE/////////', price)

    cartid = request.POST.get('id')
    amount = int(quantity)*float(price)
    print('AMOUNT######', amount)
    Cart.objects.filter(id=cartid).update(itemquantity=quantity, total=amount)
    bill = Cart.objects.aggregate(Sum('total'))
    print(bill)
    totalam = bill['total__sum']
    count = Cart.objects.filter(currentuser=request.user).count()
    return JsonResponse({'status': 'true', 'bill': totalam, 'amount': amount, 'count': count})


def editProfile(req):
    print('inside editprofile')
    currentUser = req.user
    print('/////////////', currentUser)
    data1 = UserProfile.objects.get(user=currentUser)
    data2 = User.objects.get(username=currentUser)
    #profile = forms.UserProfileForm(data1)
    #form = forms.UserForm(data2)

    if req.method == "POST":
        profile = forms.UserProfileForm(req.POST, instance=data1)
        form = forms.UserForm(req.POST, instance=data2)
        if form.is_valid() and profile.is_valid():
            user = form.save(commit=True)
            profile = profile.save(commit=False)
            profile.user = user
            profile.save()
            form.save()
            return redirect('/showfood')
    count = Cart.objects.filter(currentuser=req.user).count()
    return render(req, 'Foodapp/index.html', {'count': count})


def addcart(req):
    print('ADD TO CAR ????????????????????????', req.GET)
    fid = req.GET['foodid']
    print(fid)
    #price = req.GET.get('price')
    # print(price)
    foodobj = Food.objects.get(id=fid)
    price = foodobj.price
    cuser = req.user
    Cart(currentuser=cuser, fid=foodobj, total=price).save()
    print(price, foodobj, cuser)
    print(req)
    count = Cart.objects.filter(currentuser=req.user).count()
    return render(req, 'Foodapp/menu.html', {'count': count})


def showCart(req):
    user = req.user
    data = Cart.objects.filter(currentuser=user)
    print(data)
    # global totalam
    # totalam = 0
    count = Cart.objects.filter(currentuser=req.user).count()
    return render(req, 'Foodapp/cart.html', {'cart': data, 'count': count})


def deleteCart(req, id):
    Cartobj = Cart.objects.get(id=id)
    print('/////////////////////////////////', Cartobj)
    Cartobj.delete()
    count = Cart.objects.filter(currentuser=req.user).count()
    return redirect('/cart', {'count': count})


def addorders(req):
    try:
        amount = req.POST.get('totalbill')
        print('AMOUNT  ', amount)
        user = req.user
        ordsumobject = OrderSummery1.objects.create(
            totalamount=amount, customer=user)
        ordsumobject.save()
        cart = list(Cart.objects.filter(currentuser=user))
        print(cart)
        for c in cart:
            ordobj = Orders(ordersobj=ordsumobject, food=c.fid,
                            total=c.total, foodQuant=c.itemquantity)
            print('##############', ordobj)
            ordobj.save()
            c.delete()
        count = Cart.objects.filter(currentuser=req.user).count()
        return render(req, 'Foodapp/index.html', {'success': 'order has been placed', 'count': count})
    except Exception as e:
        return render(req, 'Foodapp/cart.html', {'msg': 'some error'+str(e)})


def showOrders(req):
    osobj = OrderSummery1.objects.filter(customer=req.user)
    oslist = list(osobj)
    print('OS LIST PRINTING')
    print(oslist)
    data = []
    for i in oslist:
        print('///////////////////', i)
        print(i.totalamount)
        q = Orders.objects.filter(ordersobj=i)
        for ordersobj in list(q):
            data.append(ordersobj)
    print(data)
    print('HELLO WORLD')
    count = Cart.objects.filter(currentuser=req.user).count()

    return render(req, 'Foodapp/myorder.html', {'data': oslist, 'data1': data, 'count': count})


def showallorders(req):
    data = OrderSummery1.objects.all()
    count = Cart.objects.filter(currentuser=req.user).count()

    return render(req, 'Foodapp/allorder.html', {'data': data, 'count': count})

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////


def graph(req):
    fcount = Food.objects.all().count()
    ccount = User.objects.all(). count()
    ocount = OrderSummery1.objects.all().count()
    amount = list(OrderSummery1.objects.values_list('totalamount'))
    totalamount = 0
    for i in amount:
        totalamount += i[0]
    print(fcount, ccount, ocount, totalamount)
    return render(req, 'Foodapp/graph.html', {'fcount': fcount, 'ccount': ccount, 'ocount': ocount, 'total': totalamount})


def cgraph(req):
    data1 = OrderSummery1.objects.all()
    data = read_frame(data1)
    print(data, type(data))
    cust = data.groupby('customer')['id'].count()
    print(cust, type(cust))
    plt.plot(cust.index, cust.values)
    plt.show()
    return render(req, 'Foodapp/graph.html')


def categorygraph(req):
    data1 = Food.objects.values('category').annotate(Count('category'))
    print(data1)
    data = read_frame(data1)
    print(data)
    plt.pie(data.loc[:, 'category_count'], labels=data.loc[:, 'category'])
    plt.show()
    return render(req, 'Foodapp/graph.html',)


def ordergraph(req):
    data1 = OrderSummery1.objects.values('date', 'totalamount')
    print(data1)
    data = read_frame(data1)
    print(data.dtypes)
    data['date'] = pd.to_datetime(data['date'], infer_datetime_format=True)
    data['month'] = pd.DatetimeIndex(data['date']).month
    df = data.groupby('month')['totalamount'].sum()
    print(df)
    sns.boxplot(df.index.values)
    months = ['April', 'May']
    # graph=sns.countplot('month',data=)
    plt.show()


def ccountgraph(req):
    data1 = OrderSummery1.objects.values(
        'customer').annotate(Count('customer'))
    print(data1)
    df = read_frame(data1)
    print(df)
    sns.ccountplot(x='customer', data=df)
    plt.show()

    return render(req, 'Foodapp/graph.html')
