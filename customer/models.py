from django.db import models

# Create your models here.


class CustomerInfo(models.Model):
    cust_location = models.CharField(max_length=16)
    cust_name = models.CharField(max_length=16)
    cust_mobilephone = models.CharField(max_length=32)
    cust_address = models.CharField(max_length=128)
    cust_phone = models.CharField(max_length=16)
    cust_rebate = models.IntegerField(default=80.00)
    is_delete = models.BooleanField(default=0)

    class Meta:
        db_table = 'syc_customer_info'