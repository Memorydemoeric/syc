from django.db import models


# Create your models here.
from common import rds
from customer.models import CustomerInfo


class ProductInfo(models.Model):
    pro_id = models.CharField(max_length=32, unique=True)
    pro_type = models.CharField(max_length=16, default='包')
    pro_count = models.IntegerField(default=0)
    pro_unit_cost = models.FloatField(default=0.0)
    pro_unit_price = models.FloatField(default=0.0)
    is_delete = models.BooleanField(default=0)

    class Meta:
        db_table = 'syc_storage_product_info'

    @property
    def product_total_cost(self):
        return self.pro_count * self.pro_unit_cost


class HalfFinishInfo(models.Model):
    half_id = models.CharField(max_length=32, unique=True)
    half_type = models.CharField(max_length=16, default='半成品')
    half_count = models.IntegerField(default=0)
    half_unit_cost = models.FloatField(default=0.0)
    half_unit_price = models.FloatField(default=0.0)
    is_delete = models.BooleanField(default=0)

    class Meta:
        db_table = 'syc_storage_half_finish'

    @property
    def half_total_cost(self):
        return self.half_count * self.half_unit_cost


class ProductRecord(models.Model):
    pro_id = models.CharField(max_length=32)
    pro_operate = models.CharField(max_length=8)  # M:调整 O:出库 I:入库 R:退货
    pro_old_count = models.IntegerField(default=0)
    pro_new_count = models.IntegerField(default=0)
    pro_change_count = models.IntegerField(default=0)
    pro_operate_time = models.DateTimeField(auto_created=True, auto_now_add=True)

    class Meta:
        db_table = 'syc_storage_product_record'

    @classmethod
    def product_modify(cls, pro_id, old_count, new_count, operate):
        change_count = new_count - old_count
        cls.objects.create(pro_id=pro_id, pro_operate=operate, pro_old_count=old_count,
                                     pro_new_count=new_count, pro_change_count=change_count)
        return None

    @classmethod
    def product_output_list(cls, pro_id, pro_change_count, pro_operate='O'):
        pro_old_count = ProductInfo.objects.get(pro_id=pro_id).pro_count
        pro_new_count = pro_old_count - pro_change_count
        out_element = cls(pro_id=pro_id, pro_change_count=pro_change_count, pro_old_count=pro_old_count, pro_new_count=pro_new_count, pro_operate=pro_operate)
        return out_element


class HalfFinishRecord(models.Model):
    half_id = models.CharField(max_length=32)
    half_operate = models.CharField(max_length=8)  # M:调整 O:出库 I:入库 R:退货
    half_old_count = models.IntegerField(default=0)
    half_new_count = models.IntegerField(default=0)
    half_change_count = models.IntegerField(default=0)
    half_operate_time = models.DateTimeField(auto_created=True, auto_now_add=True)

    class Meta:
        db_table = 'syc_storage_half_record'

    @classmethod
    def half_modify(cls, pro_id, old_count, new_count, operate):
        change_count = new_count - old_count
        cls.objects.create(half_id=pro_id, half_operate=operate, half_old_count=old_count,
                                     half_new_count=new_count, half_change_count=change_count)
        return None


class StorageOut(models.Model):
    pur_id = models.IntegerField(default=0, unique=True)
    storage_create_date = models.DateTimeField(auto_now_add=True)
    storage_price = models.FloatField(default=0.00)
    storage_actual_price = models.FloatField(default=0.00)
    pur_handler = models.CharField(max_length=256)
    pur_comment = models.CharField(max_length=32)
    cust_id = models.IntegerField(default=0)
    translation_expense = models.FloatField(default=0.00)
    translation_comment = models.CharField(max_length=256)
    rebate = models.IntegerField(default=0)
    is_enough = models.BooleanField(default=False)
    is_out = models.BooleanField(default=0)
    is_delete = models.BooleanField(default=0)
    payment_status = models.BooleanField(default=False)    # 付款状态: 0为未付款 1为已付款

    class Meta:
        db_table = 'syc_storage_out'

    @property
    def cust_info(self):
        if not hasattr(self, '_cust_info'):
            self._cust_info = CustomerInfo.objects.get(pk=self.cust_id)
        return self._cust_info

    @property
    def total_count(self):
        if not hasattr(self, '_total_count'):
            self._total_count = sum([i.storage_pro_count for i in StorageOutDetail.objects.filter(pur_id=self.pur_id).filter(is_delete=False)])
        return self._total_count

    @property
    def storage_out_detail(self):
        if not hasattr(self, '_storage_out_detail'):
            self._storage_out_detail = StorageOutDetail.objects.filter(pur_id=self.pur_id).order_by('pro_id')
        return self._storage_out_detail


class StorageOutDetail(models.Model):
    pro_id = models.CharField(max_length=32)
    storage_pro_count = models.IntegerField(default=0)
    storage_pro_actual_price = models.FloatField(default=0.00)
    storage_pro_price = models.FloatField(default=0.00)
    pur_id = models.IntegerField(default=0)
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'syc_storage_out_detail'

    @property
    def storage_unit_price(self):
        if not hasattr(self, '_storage_unit_price'):
            self._storage_unit_price = ProductInfo.objects.get(pro_id=self.pro_id).pro_unit_price
        return self._storage_unit_price


class StorageInProduct(models.Model):
    in_total_count = models.FloatField(default=0.00)
    in_date = models.DateField(auto_now=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'syc_storage_in_product'


class StorageInDetailProduct(models.Model):
    pro_id = models.CharField(max_length=32)
    in_count = models.FloatField(default=0.00)
    in_pur_id = models.IntegerField(default=0)

    class Meta:
        db_table = 'syc_storage_in_detail_product'


class StorageInHalf(models.Model):
    in_total_count = models.FloatField(default=0.00)
    in_date = models.DateField(auto_now=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'syc_storage_in_half'


class StorageInDetailHalf(models.Model):
    pro_id = models.CharField(max_length=32)
    in_count = models.FloatField(default=0.00)
    in_pur_id = models.IntegerField(default=0)

    class Meta:
        db_table = 'syc_storage_in_detail_half'
