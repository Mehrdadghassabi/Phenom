from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm) :
    email = forms.EmailField()

    class Meta :
        model = User
        fields = [  'first_name' , 'username' , 'email' , 'password1' , 'password2' ]


class UserUpdateFrom(forms.ModelForm) :
    email = forms.EmailField()
    class Meta :
        model = User
        fields = ['username', 'email', 'first_name' ]