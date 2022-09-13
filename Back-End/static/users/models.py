from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime , timedelta
import uuid , pytz
from persiantools.jdatetime import JalaliDateTime

def jalali_str(gr_datetime) :
    return JalaliDateTime.to_jalali(gr_datetime.astimezone(timezone.get_current_timezone())).strftime("%H:%M:%S - %Y/%m/%d")


class User(AbstractUser) :
    pass

class Purchase(models.Model) :

    purchase_id = models.CharField(primary_key=True , default=uuid.uuid4().hex[:20] , max_length=20, editable=False)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(default=timezone.now)
    license_days = models.IntegerField(default=30)
    paid_amount = models.IntegerField()


    @property
    def purchase_date_jalali(self):
        return jalali_str(self.purchase_date)



class License(models.Model) :
    license_key = models.CharField(max_length=50)
    hw_id = models.CharField(max_length=100 , default='')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    start_date =  models.DateTimeField(default=timezone.now)
    expiration_date = models.DateTimeField()
    purchase_id = models.CharField(primary_key=True , default=uuid.uuid4().hex[:20] , max_length=20, editable=False)

    @property
    def expiration_date_jalali(self):
        return jalali_str(self.expiration_date)

class Notification (models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    message = models.CharField(max_length=400 )
    date = models.DateTimeField(default=timezone.now)
    page = models.CharField(max_length=400 , default="")

def add_license(user , license_days , paid_amount ) :

    p_id = uuid.uuid4().hex[:6].upper()
    while Purchase.objects.filter(purchase_id=p_id).exists():
        p_id = uuid.uuid4().hex[:6].upper()

    pur = Purchase(purchase_id = p_id , user=user, paid_amount=paid_amount, license_days=license_days)
    pur.save()
    license = License(license_key=uuid.uuid4().hex[:20].upper() , user=user , expiration_date=timezone.now() + timedelta(days=license_days)
                      , purchase_id = p_id)
    license.save()
    jalali_date = jalali_str(timezone.now())
    message = "خرید اشتراک %s روزه در تاریخ %s" % (license_days, jalali_date)
    notif = Notification(user=user, message=message, page='purchased-licenses')
    notif.save()

    return p_id


User._meta.get_field('email')._unique = True

