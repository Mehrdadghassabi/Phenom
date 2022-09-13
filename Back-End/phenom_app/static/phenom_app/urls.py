from django.urls import path
from . import views

urlpatterns = [
    path('', views.home , name='home'),
    path('doc/', views.doc, name='doc'),
    path('tech-info/', views.tech_info, name='tech-info'),
    path('contact-us/', views.contact_us, name="contact-us"),
    path('download-phenom/', views.download_view ,name='download'),
]