from django.db import models
import datetime

# Create your models here.
from common import rds
from common.my_math_func import my_round
from customer.models import CustomerInfo
from storage.models import ProductInfo, HalfFinishInfo


# 订单
class Purchase(models.Model):
    pur_price = models.FloatField(default=0.00)
    pur_create_date = models.DateTimeField(auto_now_add=True)
    pur_modify_date = models.DateField(default=datetime.datetime.now().strftime('%Y-%m-%d'))
    pur_finished_date = models.DateField(auto_now=True)
    pur_handle = models.CharField(max_length=256)
    pur_comment = models.CharField(max_length=32)
    cust_id = models.IntegerField(default=1)
    rebate = models.IntegerField(default=0)
    # 订单状态（0:已下单 1:生产中 2:出库结余 3:完成）
    pur_status = models.CharField(max_length=8, default='0')
    payment_status = models.BooleanField(default=0)
    predict_freight = models.IntegerField(default=0)
    is_enough = models.BooleanField(default=0)
    is_selected = models.BooleanField(default=0)
    is_finished = models.BooleanField(default=0)
    is_delete = models.BooleanField(default=0)

    @property
    def cust_info(self):
        if not hasattr(self, '_cust'):
            self._cust = CustomerInfo.objects.get(id=self.cust_id)
        return self._cust

    @property
    def purchase_detail(self):
        if not hasattr(self, '_purchase_detail'):
            self._purchase_detail = PurchaseDetail.objects.filter(pur_id=self.id).order_by('pro_id')
        return self._purchase_detail

    @property
    def count(self):
        if not hasattr(self, '_count'):
            self._count = sum([i.pur_pro_count for i in PurchaseDetail.objects.filter(pur_id=self.id)])
        return self._count

    def update_price(self):
        self.pur_price = sum(i.pur_pro_price for i in self.purchase_detail)
        self.save()

    @property
    def actual_price(self):
        if not hasattr(self, '_actual_price'):
            self._actual_price = my_round(self.pur_price * self.rebate / 100)
        return self._actual_price

    @classmethod
    def get_purchase_order_by_id(cls, id):
        try:
            purchase_order = cls.objects.get(pk=id)
        except ValueError:
            purchase_order = None
        return purchase_order

    class Meta:
        db_table = 'syc_purchase'


# 订单详情
class PurchaseDetail(models.Model):
    pro_id = models.CharField(max_length=32)
    pur_pro_count = models.IntegerField(default=0)
    pur_pro_price = models.FloatField(default=0.00)
    pur_id = models.IntegerField(default=0)

    @property
    def product_info(self):
        if not hasattr(self, '_product'):
            self._product = ProductInfo.objects.get(pro_id=self.pro_id)
        return self._product

    @property
    def pur_info(self):
        if not hasattr(self, '_pur_info'):
            self._pur_info = Purchase.objects.get(id=self.pur_id)
        return self._pur_info

    @classmethod
    def get_order_detail(cls, ord_id):
        data = cls.objects.filter(pur_id=ord_id)
        for i in data:
            rds.zadd('order_' + ord_id, i.pro_id, i.pur_pro_count)
        return sorted(data, key=lambda product: product.pro_id)

    @classmethod
    def update_order_detail(cls, data, ord_id, pro_id, pro_count):
        if data.filter(pro_id=pro_id):
            pro_info = data.filter(pro_id=pro_id).first()
            pro_info.pro_count = pro_count
        else:
            pro_info = cls(pro_id=pro_id, pur_pro_count=pro_count, pur_id=ord_id)
        pro_info.pur_pro_price = my_round(pro_count * ProductInfo.objects.get(
            pro_id=pro_id).pro_unit_price * Purchase.objects.get(
            pk=ord_id).rebate / 100)
        pro_info.save()
        return

    @property
    def storage_pro(self):
        return ProductInfo.objects.get(pro_id=self.pro_id)

    @property
    def storage_half(self):
        return HalfFinishInfo.objects.get(half_id=self.pro_id)

    @property
    def pur_total(self):
        return self.storage_pro.pro_count + self.storage_half.half_count - self.pur_pro_count

    @property
    def pro_surplus(self):
        return self.storage_pro.pro_count - self.pur_pro_count

    @classmethod
    def create_surplus_object(cls, ord_id, pro_id, pur_pro_count):
        surplus_object = cls(pur_id=int(ord_id), pro_id=pro_id, pur_pro_count=pur_pro_count,
                             pur_pro_price=pur_pro_count * ProductInfo.objects.get(
                                 pro_id=pro_id).pro_unit_price)
        return surplus_object

    class Meta:
        db_table = 'syc_pur_detail'


# 退货单
class RefundPurchase(models.Model):
    ref_cust_id = models.IntegerField(default=0)
    ref_create_time = models.DateTimeField(auto_created=True, auto_now_add=True)
    rebate = models.FloatField(default=0.00)
    is_delete = models.BooleanField(default=0)

    @property
    def refund_purchase_detail(self):
        if not hasattr(self, '_refund_purchase_detail'):
            self._refund_purchase_detail = RefundPurchaseDetail.objects.filter(ref_purchase_id=self.id)
        return self._refund_purchase_detail

    @property
    def total_count(self):
        if not hasattr(self, '_total_count'):
            self._total_count = sum(i.pur_pro_count for i in self.refund_purchase_detail)
        return self._total_count

    @property
    def total_price(self):
        if not hasattr(self, '_total_price'):
            self._total_count = sum([i.ref_pro_count * ProductInfo.objects.get(pro_id=i.ref_pro_id).pro_unit_price for i in self.refund_purchase_detail])
        return self._total_count

    @property
    def cust_info(self):
        if not hasattr(self, '_cust_info'):
            self._cust_info = CustomerInfo.objects.get(pk=self.ref_cust_id)
        return self._cust_info

    class Meta:
        db_table = 'syc_refund_purchase'


# 退货单详情
class RefundPurchaseDetail(models.Model):
    ref_pro_id = models.CharField(max_length=32)
    ref_pro_count = models.IntegerField(default=1)
    ref_purchase_id = models.IntegerField(default=0)
    is_delete = models.BooleanField(default=0)

    class Meta:
        db_table = 'syc_refund_purchase_detail'

    @property
    def pro_info(self):
        if not hasattr(self, '_pro_info'):
            self._pro_info = ProductInfo.objects.get(pro_id=self.ref_pro_id)
        return self._pro_info

    @property
    def pro_total_price(self):
        if not hasattr(self, '_pro_total_price'):
            self._pro_total_price = self._pro_info.pro_unit_price * self.ref_pro_count
        return self._pro_total_price
