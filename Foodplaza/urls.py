"""Foodplaza URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import logout
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Foodapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('addfood/', views.addFood),
    path('showfood/', views.menu),
    path('deletefood/<int:id>', views.Deletefood),
    path('updatefood/<int:id>', views.Updatefood),
    path('signup', views.CreateUser),
    path('showuser', views.showUsers),
    path('login/', views.logins),
    path('index/', views.index),
    path('logout/', views.logouts),
    path('', views.index),
    path('profile/', views.userprofile),
    path('updatecust/', views.editProfile),
    path('addtocart/', views.addcart),
    path('cart', views.showCart),
    path('updatecart/', views.updatecart),
    path('deletecart/<int:id>', views.deleteCart),
    path('addorders/', views.addorders),
    path('showalluser/', views.showallorders),
    path('showorders/', views.showOrders),
    path('graph/', views.graph),
    path('customergraph/', views.cgraph),
    path('categorygraph/', views.categorygraph),
    path('ordergraph/', views.ordergraph),
    path('ccountgraph/', views.ccountgraph)


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
