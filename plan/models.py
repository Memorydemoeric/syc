import datetime

from django.db import models

# Create your models here.
from storage.models import ProductInfo, HalfFinishInfo


class PlanList(models.Model):
    plan_create_time = models.DateTimeField(auto_now_add=True, auto_created=True)

    class Meta:
        db_table = 'syc_plan'


class PlanDetail(models.Model):
    plan_id = models.CharField(max_length=16)
    plan_pro_id = models.CharField(max_length=16)
    plan_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'syc_plan_detail'

    @property
    def plan(self):
        if not hasattr(self, '_plan'):
            self._plan = PlanList.objects.get(pk=self.plan_id)
        return self._plan

    @property
    def product(self):
        if not hasattr(self, '_product'):
            self._product = ProductInfo.objects.get(pro_id=self.plan_pro_id)
        return self._product

    @property
    def half_finished(self):
        if not hasattr(self, '_half_finished'):
            self._half_finished = HalfFinishInfo.objects.get(half_id=self.plan_pro_id)
        return self._half_finished


