from django.db import models

# Create your models here.

class UserInfo(models.Model):
    user_name = models.CharField(max_length=16)
    telephone_number = models.CharField(max_length=32, default='')
    level = models.IntegerField(default=5)
    comment = models.CharField(max_length=256, default='')
    password = models.CharField(max_length=512, default='')
    load_in_token = models.CharField(max_length=512, default='')
    is_delete = models.BooleanField(default=0)

    class Meta:
        db_table = 'syc_user_info'