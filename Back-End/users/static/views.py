from django.shortcuts import render , redirect
from django.contrib import messages
from .forms import UserRegisterForm , UserUpdateFrom
from django.utils.translation import activate

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core import mail
from django.utils.html import strip_tags
from django.http import HttpResponse
from .models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse , JsonResponse
from django.shortcuts import redirect
import os.path , json
from zeep import Client
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy



activate('fa')


with open(os.path.dirname(__file__) + '/../config.json') as config_file:
    config_data = json.load(config_file)

MERCHANT = config_data['MERCHANT']
zarinpal_web_gate = config_data['zarinpal_web_gate']
client = Client(zarinpal_web_gate)
# amount = config_data['amount-1month']  # Toman / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional

plan = None

def register(request) :
    form = UserRegisterForm(request.POST or None)
    username=None
    if request.method == 'POST' :
        if form.is_valid() :
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)

            mail_subject = 'فعالسازی حساب فنوم'
            html_message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            plain_message = strip_tags(html_message)
            to_email = form.cleaned_data.get('email')
            from_email='app.phenom@gmail.com'
            mail.send_mail(mail_subject, plain_message, from_email, [to_email], html_message=html_message)

            username = form.cleaned_data.get('username')
            messages.success(request , f'ثبت نام شما با موفقیت انجام شد !')
            messages.success(request , f' ایمیلی حاوی لینک فعال سازی به آدرس ایمیل شما ارسال شد . جهت ثبت نام نهایی ایمیل خود را چک کنید .')
            return redirect('login')


    return render(request , 'users/register.html' , {'form':form , 'username':username})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return render(request , 'users/account-activated.html')
    else:
        return HttpResponse('<h2 style="direction:rtl;text-align:center;">لینک فعالسازی نامعتبر می باشد!</h2>')


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'users/user-panel/change-pass.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        message_text = 'رمز عبور شما با موفقیت تغییر یافت'
        messages.success(self.request, message_text)
        notif = Notification(user=self.request.user, message=message_text, page='profile')
        notif.save()
        return super().form_valid(form)

def change_pass(request) :
    form = UserRegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            return redirect('profile')

    return render(request, 'users/user-panel/change-pass.html', {'form': form})


@login_required
def send_request(request, plan_id):
    # print(request.user.username)
    global plan
    plans = {
        1: config_data['plans']['plan1'],
        2: config_data['plans']['plan2'],
        3: config_data['plans']['plan3'],
        4: config_data['plans']['plan4']
    }
    plan = plan_id
    try:
        amount = plans[plan_id]["amount"]
    except:
        # TODO: Render a noice HTML
        return HttpResponse('there is no such plan')

    callback_URL = ''.join(['http://', get_current_site(request).domain, "/verify"])
    result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, callback_URL)
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))

@login_required
def verify(request):
    global plan
    plans = {
        1: config_data['plans']['plan1'],
        2: config_data['plans']['plan2'],
        3: config_data['plans']['plan3'],
        4: config_data['plans']['plan4']
    }
    paid_amount = plans[plan]["amount"]
    license_days = plans[plan]["days"]
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], paid_amount)
        if result.Status == 100:
            # license_days = plan * 30
            purchase_id = add_license(request.user, license_days, paid_amount)
            context = {
                'purchase_id' : purchase_id,
                'payment_id' : result.RefID
            }
            return successful_payment(request,context=context)
            # return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID) + "\nPurchase ID: " + str(purchase_id) )
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return redirect("unsuccessful-payment")
            # return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return redirect("unsuccessful-payment")
        # return HttpResponse('Transaction failed or canceled by user')


def successful_payment(request , context = None) :
    return render(request, 'users/payment/successful-payment.html', context)

@csrf_exempt
def validateLicense(request) :

    if request.method == 'POST':
        r = json.loads(request.body)
        lic_key = r['license']
        email = r['email']
        hardware_id = r['hardware_id']
        license = License.objects.filter(license_key=lic_key).first()
        if license and email == license.user.email :
            exp_date = license.expiration_date
            hw_id = license.hw_id
            if timezone.now() <  exp_date :
                okResponse = JsonResponse({"isValid": True , "expiration_date":str(exp_date)})
                if not hw_id :
                    license.hw_id = hardware_id
                    license.save()
                    return okResponse
                elif (hw_id == hardware_id) :
                    return okResponse

        return JsonResponse({"isValid": False})

    return HttpResponse("Invalid request")

@login_required
def dashboard(request) :
    active_licenses = License.objects.filter(user=request.user).filter(expiration_date__gt=timezone.now())
    context = {"licenses":active_licenses}
    return render(request , 'users/user-panel/dashboard.html' , context)


@login_required
def purchased_licenses(request) :
    purchases = Purchase.objects.filter(user=request.user)
    context = {"purchases": purchases}
    return render(request, 'users/user-panel/purchased-licenses.html' , context)

@login_required
def profile(request) :
    if request.method=='POST' :
        u_form = UserUpdateFrom(request.POST , instance=request.user)
        if u_form.is_valid() :
            u_form.save()
            message_text = f'پروفایل شما با موفقیت آپدیت شد'
            messages.success(request, message_text )
            notif = Notification(user=request.user, message=message_text, page='profile')
            notif.save()

            return redirect('profile')
    else :
        u_form = UserUpdateFrom(instance=request.user)

    context = {"u_form" : u_form , "username":request.user.username
        , "email":request.user.email ,"full_name":request.user.first_name}

    return render(request , 'users/user-panel/profile.html' , context)

@login_required
def buy_license(request) :
    return render(request , 'users/user-panel/buy-license.html')

@login_required
def mark_as_read(request) :
    Notification.objects.all().delete()
    return redirect(request.GET['current'])

