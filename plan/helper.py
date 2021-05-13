from common import rds
from purchase.models import Purchase
from storage.models import ProductInfo, HalfFinishInfo


class CreatePlanDetail(object):

    def __init__(self, pro_id, pro_count):
        self.pro_id = pro_id.decode('utf-8')
        self.pro_count = pro_count

    @property
    def product(self):
        if not hasattr(self, '_product'):
            self._product = ProductInfo.objects.get(pro_id=self.pro_id)
        return self._product

    @property
    def half_finished(self):
        if not hasattr(self, '_half_finished'):
            self._half_finished = HalfFinishInfo.objects.get(half_id=self.pro_id)
        return self._half_finished

    @property
    def new_product(self):
        if not hasattr(self, '_new_product'):
            self._new_product = self.pro_count - self.product.pro_count
            if self._new_product < 0:
                return 0
        return self._new_product

    @property
    def new_half_finished(self):
        if not hasattr(self, '_new_half_finished'):
            self._new_half_finished = self.pro_count - self.product.pro_count - self.half_finished.half_count
            if self._new_half_finished <= 0:
                return 0
        return self._new_half_finished

    @property
    def percent_complete(self):
        if not hasattr(self, '_percent_complete'):
            self._percent_complete = round(self.product.pro_count / self.pro_count * 100, 2)
            if self._percent_complete >= 100:
                return 100
        return self._percent_complete

    @property
    def is_complete(self):
        if not hasattr(self, '_is_complete'):
            self._is_complete = (ProductInfo.objects.get(pro_id=self.pro_id).pro_count <= self.pro_count)
        return self._is_complete

    @property
    def half_count(self):
        if not hasattr(self, '_half_count'):
            self._half_count = self.half_finished.half_count
        return self._half_count


def purchase_detail_for_customer(detail_infos, pro_id):
    purchase_for_customer = ''
    for i in detail_infos:
        if i.purchase_detail.filter(pro_id=pro_id):
            cust_info = i.cust_info.cust_location + i.cust_info.cust_name
            purchase_detail = i.purchase_detail.get(pro_id=pro_id).pur_pro_count
            purchase_for_customer += cust_info + '*' + str(purchase_detail) + '  '
    return purchase_for_customer


def create_excel_data():
    origin_data = rds.zrange('plan_detail', 0, -1, withscores=True)
    origin_data_sorted = sorted(origin_data, key=lambda i: i[0])
    detail_infos = Purchase.objects.filter(is_delete=False).filter(is_selected=True).filter(pur_status__in=['0', '1', '2'])
    data = []
    for i in origin_data_sorted:
        purchase_for_customer = purchase_detail_for_customer(detail_infos, i[0].decode('utf-8'))
        plan_detail = CreatePlanDetail(i[0], i[1])
        if plan_detail.is_complete:
            data.append((i[0], i[1], plan_detail.new_half_finished, plan_detail.new_product, purchase_for_customer))
    return data
