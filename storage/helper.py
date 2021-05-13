from common import rds
from common.my_math_func import my_round
from purchase.models import Purchase, PurchaseDetail
from storage.models import ProductInfo, StorageOut, StorageOutDetail, ProductRecord, HalfFinishInfo, \
    StorageInDetailProduct, StorageInProduct, StorageInDetailHalf, StorageInHalf


class OutDetail(object):
    def __init__(self, pro_id, pro_count, rebate):
        self.pro_id = pro_id
        self.pro_count = int(pro_count)
        self.rebate = rebate
        self.pro_ordinary_price = ProductInfo.objects.get(pro_id=pro_id).pro_unit_price * int(pro_count)
        self.pro_price = my_round(self.pro_ordinary_price * rebate / 100)


class AllStorageInfo(object):
    def __init__(self, pro_id, pro_count, half_count, ):
        self.pro_id = pro_id
        self.pro_count = pro_count
        self.half_count = half_count

    @property
    def total_count(self):
        if not hasattr(self, '_total_count'):
            self._total_count = self.pro_count + self.half_count
        return self._total_count


def create_storage_out_list(ord_id, pur_handler, translation_expense):
    purchase_info = Purchase.objects.get(id=int(ord_id))
    rebate = purchase_info.rebate
    pur_id = purchase_info.id
    storage_price = sum([int(i[1]) * ProductInfo.objects.get(pro_id=i[0].decode('utf-8')).pro_unit_price for i in
                         rds.zrange('storage_out_' + str(ord_id), 0, -1, withscores=True)])
    storage_actual_price = my_round(storage_price * purchase_info.rebate / 100)
    pur_handler = pur_handler
    pur_comment = purchase_info.pur_comment
    cust_id = purchase_info.cust_info.id
    is_out = True
    StorageOut.objects.create(pur_id=pur_id, storage_actual_price=storage_actual_price, storage_price=storage_price,
                              pur_handler=pur_handler, cust_id=cust_id, is_out=is_out, pur_comment=pur_comment,
                              translation_expense=translation_expense, is_enough=purchase_info.is_enough, rebate=rebate)
    storage_out_chache_elements = [(i[0].decode('utf-8'), i[1]) for i in
                                   rds.zrange('storage_out_' + ord_id, 0, -1, withscores=True)]
    storage_out_elements = [StorageOutDetail(pur_id=int(ord_id), pro_id=foo[0], storage_pro_count=int(foo[1]),
                                             storage_pro_price=foo[1] * ProductInfo.objects.get(
                                                 pro_id=foo[0]).pro_unit_price,
                                             storage_pro_actual_price=foo[1] * ProductInfo.objects.get(
                                                 pro_id=foo[0]).pro_unit_price * purchase_info.rebate / 100) for foo in
                            storage_out_chache_elements]
    StorageOutDetail.objects.bulk_create(storage_out_elements)
    storage_out_record_elements = [ProductRecord.product_output_list(pro_id=foo[0], pro_change_count=foo[1]) for foo in
                                   storage_out_chache_elements]
    ProductRecord.objects.bulk_create(storage_out_record_elements)
    return storage_out_chache_elements, storage_actual_price, cust_id


# 比较订单和出库单的不同
def purchase_compare(ord_id, pur_handler):
    for i in PurchaseDetail.objects.filter(pur_id=ord_id):
        rds.zincrby('storage_out_pur_' + ord_id, i.pro_id, i.pur_pro_count)
    purchase_info = Purchase.objects.get(pk=ord_id)
    purchase_info.pur_status = '3'
    purchase_info.is_selected = 0
    purchase_info.save()
    if rds.zrange('storage_out_pur_' + ord_id, 0, -1, withscores=True) != rds.zrange('storage_out_' + ord_id, 0, -1,
                                                                                     withscores=True):
        for i in rds.zrange('storage_out_' + ord_id, 0, -1, withscores=True):
            rds.zincrby('storage_out_pur_' + ord_id, i[0], -int(i[1]))
        Purchase.objects.create(pur_handle=pur_handler, cust_id=purchase_info.cust_id, pur_status=2,
                                rebate=purchase_info.rebate)
        detail_infos = [PurchaseDetail.create_surplus_object(ord_id=str(Purchase.objects.all().last().id),
                                                             pro_id=foo[0].decode('utf-8'), pur_pro_count=int(foo[1]))
                        for foo in rds.zrange('storage_out_pur_' + ord_id, 0, -1, withscores=True) if int(foo[1]) != 0]
        PurchaseDetail.objects.bulk_create(detail_infos)
        Purchase.objects.all().last().update_price()
        rds.delete('storage_out_pur_' + ord_id)


def storage_in_product_info_change(pro_id, in_count_change):
    product_info = ProductInfo.objects.get(pro_id=pro_id)
    old_product_count = product_info.pro_count
    product_count_change = in_count_change
    new_product_count = old_product_count + product_count_change
    product_info.pro_count += product_count_change
    product_info.save()
    return old_product_count, new_product_count, product_count_change


def storage_in_half_info_change(pro_id, in_count_change):
    half_info = HalfFinishInfo.objects.get(half_id=pro_id)
    old_half_count = half_info.half_count
    half_count_change = -in_count_change
    new_half_count = old_half_count + half_count_change
    half_info.half_count += half_count_change
    half_info.save()
    return old_half_count, new_half_count, half_count_change


def storage_in_detail_product_info_change(storage_in_id, pro_id, new_in_count):
    storage_in_detail_product_info = StorageInDetailProduct.objects.filter(in_pur_id=storage_in_id).get(
        pro_id=pro_id)
    storage_in_detail_product_info.in_count = new_in_count
    storage_in_detail_product_info.save()
    return None


def storage_in_product_info_order_change(storage_in_id, total_count_change):
    storage_in_product_info = StorageInProduct.objects.get(pk=storage_in_id)
    storage_in_product_info.in_total_count += total_count_change
    storage_in_product_info.save()
    return None


def storage_in_detail_half_info_change(storage_in_id, pro_id, new_in_count):
    storage_in_detail_half_info = StorageInDetailHalf.objects.filter(in_pur_id=storage_in_id).get(
        pro_id=pro_id)
    storage_in_detail_half_info.in_count = new_in_count
    storage_in_detail_half_info.save()
    return None


def storage_in_half_info_order_change(storage_in_id, total_count_change):
    storage_in_half_info = StorageInHalf.objects.get(pk=storage_in_id)
    storage_in_half_info.in_total_count += total_count_change
    storage_in_half_info.save()
    return None

