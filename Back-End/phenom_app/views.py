from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactUs
from django.utils.translation import activate
from django.core import mail

activate('fa')

def home(request) :
    return render(request , 'phenom_app/home.html')

def doc(request):
    return render(request , 'phenom_app/doc-page.html')

def tech_info(request):
    return render(request , 'phenom_app/tech-info.html')

def download_view(request):
    return render(request , 'phenom_app/downloadpage.html')

def contact_us(request):

    if request.method == 'POST':

        form = ContactUs(request.POST)

        if form.is_valid():
            
            _email = form.cleaned_data.get('email')
            _message = form.cleaned_data.get('message')
            _name = form.cleaned_data.get('name')
            _site = form.cleaned_data.get('site')
            _phone = form.cleaned_data.get('phone')
            
            whole_data  = f"email: {_email}\n"
            whole_data += f"name: {_name}\n"
            whole_data += f"message: {_message}\n"
            whole_data += f"web site: {_site}\n"
            whole_data += f"phone number: {_phone}\n"
            from_email='app.phenom@gmail.com'
            
            mail.send_mail("Contact Us Stuff", whole_data, from_email, [from_email])
            
            # messages.success(request, 'پیام با موفقیت ارسال شد :)')
            return render(request, 'phenom_app/message-recorded.html')
            # return redirect("contact-us")

    else:
        form = ContactUs()

    return render(request, 'phenom_app/contact-us.html', {'form': form})