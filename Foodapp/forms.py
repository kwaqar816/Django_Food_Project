from django.forms import fields, widgets
from Foodapp import models
from Foodapp.models import Food, UserProfile
from django import forms
from django.contrib.auth.models import User


class Foodform(forms.ModelForm):
    category = [('veg', 'vegitarian'), ('Non-veg', 'Non-vegetarian')]
    name = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'ni', 'class': 'c1'}))
    price = forms.FloatField(widget=forms.NumberInput())
    quantity = forms.IntegerField(widget=forms.TextInput())
    types = forms.CharField(widget=forms.TextInput())
    category = forms.ChoiceField(choices=category)
    image = forms.ImageField()

    class Meta:
        model = Food
        fields = '__all__'


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']


class UserProfileForm(forms.ModelForm):
    role = [('customersss', 'CUSTOMER'), ('adminsss', 'ADMIN')]
    Role = forms.ChoiceField(
        choices=role, initial='Customer', widget=forms.RadioSelect)

    class Meta:
        model = UserProfile
        fields = ['location', 'number']
