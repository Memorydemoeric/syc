from django.db import models

# Create your models here.
from customer.models import CustomerInfo
from storage.models import StorageOut


class CashFlow(models.Model):
    cust_id = models.IntegerField(default=0)
    pur_id = models.IntegerField(default=0)          # 如果为 退货 该项为0
    ref_pur_id = models.IntegerField(default=0)      # 如果为收款 发货 运费调整, 该项为0
    flow_type = models.CharField(max_length=32)      # I:收款 O:发货+运费 R:运费调整 B:退货 C:订单调整
    cash_change = models.FloatField(default=0.00)
    balance = models.FloatField(default=0.00)
    is_enough = models.BooleanField(default=False)
    flow_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'syc_report_cashflow'

    @property
    def start_flow(self):
        if not hasattr(self, '_start_flow'):
            self._start_flow = self.balance + self.cash_change
        return self._start_flow

    @property
    def storage_out_order(self):
        if not hasattr(self, '_storage_out_order'):
            self._storage_out_order = StorageOut.objects.get(pur_id=self.pur_id)
        return self._storage_out_order


class CustomerRank(models.Model):
    cust_id = models.IntegerField(default=0)
    pur_count = models.IntegerField(default=0)
    balance = models.FloatField(default=0.00)
    latest_pur_date = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'syc_report_customer_rank'

    @property
    def cust_info(self):
        if not hasattr(self, '_cust_info'):
            self._cust_info = CustomerInfo.objects.get(pk=self.cust_id)
        return self._cust_info


class StatementOutputDetail(models.Model):
    cust_id = models.IntegerField(default=0)
    origin_balance = models.FloatField(default=0.00)
    pur_id = models.IntegerField(default=0)
    pur_actual_price = models.FloatField(default=0.00)
    ref_pur_id = models.IntegerField(default=0)
    ref_pur_price = models.IntegerField(default=0)
    income = models.FloatField(default=0.00)
    balance = models.FloatField(default=0.00)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'syc_statement_output_detail'

    def update_balance(self):
        self.balance = self.origin_balance + self.income - self.pur_actual_price + self.ref_pur_price
        self.save()
