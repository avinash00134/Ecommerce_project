from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from . models import User,Product,Order

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"class":"form-control"}))

    class Meta:
        model = User
        fields = {'first_name','last_name','username','email','password1','password2','is_customer','is_seller','mobilenumber'}

class AddProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['user','available','created','updated']

class EditOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['user','created','updated']
