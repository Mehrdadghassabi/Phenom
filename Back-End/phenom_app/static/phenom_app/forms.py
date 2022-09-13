from django import forms

class ContactUs(forms.Form):
    name = forms.CharField(label='name', max_length=100, required=True)
    email = forms.EmailField(label='email', max_length=150, required=True)
    phone = forms.CharField(label='phone', max_length=15, required=False)
    site = forms.CharField(label='site', max_length=30, required=False)
    message = forms.CharField(label='message', max_length=300, required=True)