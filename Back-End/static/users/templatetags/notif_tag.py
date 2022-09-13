from django import template
from users.models import Notification

register = template.Library()

@register.filter(name='notifs')
def get_notifs(user):
    return Notification.objects.filter(user=user).order_by('-date')

@register.filter(name='notifCount')
def get_notif_count(user):
    return Notification.objects.filter(user=user).count()

