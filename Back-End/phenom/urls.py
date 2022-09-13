
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path , include
from django.views.generic.base import TemplateView
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register , name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html') , name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='phenom_app/home.html') , name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password-reset/password-reset.html',
        subject_template_name='users/password-reset/password_reset_subject.txt',
        html_email_template_name='users/password-reset/password_reset_email.html'
    ), name='password-reset') ,

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password-reset/password-reset.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password-reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),


    path('profile/change-pass/',  user_views.CustomPasswordChangeView.as_view(), name='change-pass'),
    #path('logout/' , name='logout'),
    path('activate/<uidb64>/<token>/',user_views.activate, name='activate'),
    path('', include('phenom_app.urls')),
    
    path("payment-request/<int:plan_id>/", user_views.send_request, name='payment-request'),
    path("unsuccessful-payment/", TemplateView.as_view(template_name='users/payment/unsuccessful-payment.html'), name='unsuccessful-payment'),
    path("successful-payment/", user_views.successful_payment , name='successful-payment'),
    path("verify/", user_views.verify , name='verify'),
    path("validate-license/", user_views.validateLicense , name='validate'),
    path('dashboard/', user_views.dashboard ,name='dashboard'),
    path('purchased-licenses/', user_views.purchased_licenses ,name='purchased-licenses'),
    path('profile/', user_views.profile ,name='profile'),
    path('buy-license/', user_views.buy_license ,name='buy-license'),
    path('mark-as-read/', user_views.mark_as_read ,name='mark_as_read'),

]
