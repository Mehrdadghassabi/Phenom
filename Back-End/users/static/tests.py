from django.test import TestCase
from .models import User , buy_license
from datetime import datetime , timedelta

class PaymentUnitTest(TestCase) :
    def setUp(self) :
        self.user = User.objects.create(username="test1")
        self.user.save()
        buy_license(self.user , 3 , 125000)
#    def test_has_paid(self):
#        self.assertTrue(self.user.has_paid() )



