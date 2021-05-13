import datetime

from purchase.models import Purchase
from report.models import CashFlow, CustomerRank, StatementOutputDetail
from storage.models import StorageOut, ProductInfo, StorageOutDetail


class FinalStatementOutputData(object):

    def __init__(self, create_date, origin_balance, income, total_actual_price, refund_price, translation_expense,
                 balance):
        self.create_date = create_date
        self.origin_balance = origin_balance
        self.income = income
        self.total_actual_price = total_actual_price
        self.refund_price = refund_price
        self.translation_expense = translation_expense
        self.balance = balance


def create_statement_output_data(cust_id, pur_id):
    statement_data = []
    flow_id = CashFlow.objects.filter(flow_type='O').get(pur_id=pur_id).id
    cash_flow_infos = CashFlow.objects.filter(cust_id=cust_id).filter(flow_type='O').filter(pk__lte=flow_id).order_by(
        '-id')[:5]
    for i in cash_flow_infos[::-1]:
        list_pur_id = i.pur_id
        statement_output_detail = StatementOutputDetail.objects.get(pur_id=list_pur_id)
        create_date = datetime.datetime.strftime(i.flow_date, '%m月%d日')
        origin_balance = statement_output_detail.origin_balance
        income = statement_output_detail.income
        balance = statement_output_detail.balance
        refund_price = statement_output_detail.ref_pur_price
        storage_info = StorageOut.objects.get(pur_id=list_pur_id)
        total_actual_price = storage_info.storage_actual_price
        translation_expense = storage_info.translation_expense
        statement_data.append(
            FinalStatementOutputData(create_date, origin_balance, income, total_actual_price, refund_price,
                                     translation_expense, balance))
    return statement_data


def create_statement_purchase_data(cust_id, pur_id):
    statement_data = []
    purchase_infos = Purchase.objects.filter(is_delete=False).filter(cust_id=cust_id).filter(pk__lte=pur_id).filter(
        pur_status__in=['0', '1', '2'])

    if len(purchase_infos) >= 5:  # 基本上不会发生
        origin_balance = CustomerRank.objects.get(cust_id=cust_id).balance

        for i in purchase_infos:

            create_date = datetime.datetime.strftime(i.pur_modify_date, '%m月%d日')

            if CashFlow.objects.filter(flow_type='I').filter(pur_id=i.id):
                income = CashFlow.objects.filter(flow_type='I').get(pur_id=i.id).cash_change
            else:
                income = 0
            total_actual_price = i.actual_price
            refund_price = 0
            translation_expense = i.predict_freight
            balance = origin_balance - i.actual_price
            statement_data.append(
                FinalStatementOutputData(create_date, origin_balance, income, total_actual_price, refund_price,
                                         translation_expense, balance))
            origin_balance = balance
        return statement_data
    else:
        cash_flow_infos = CashFlow.objects.filter(cust_id=cust_id).filter(flow_type='O').order_by('-id')[
                          :5 - len(purchase_infos)]
        balance = None

        for i in cash_flow_infos[::-1]:
            list_pur_id = i.pur_id
            statement_output_detail = StatementOutputDetail.objects.get(pur_id=list_pur_id)
            create_date = datetime.datetime.strftime(i.flow_date, '%m月%d日')
            origin_balance = statement_output_detail.origin_balance
            income = statement_output_detail.income
            balance = statement_output_detail.balance
            refund_price = statement_output_detail.ref_pur_price
            storage_info = StorageOut.objects.get(pur_id=list_pur_id)
            total_actual_price = storage_info.storage_actual_price
            translation_expense = storage_info.translation_expense
            statement_data.append(
                FinalStatementOutputData(create_date, origin_balance, income, total_actual_price, refund_price,
                                         translation_expense, balance))

        if balance:
            origin_balance = balance
        else:
            origin_balance = CustomerRank.objects.get(cust_id=cust_id).balance
        for i in purchase_infos:
            create_date = datetime.datetime.strftime(i.pur_modify_date, '%m月%d日')

            if StatementOutputDetail.objects.filter(pur_id=i.id):
                income = StatementOutputDetail.objects.get(pur_id=i.id).income
            else:
                income = 0
            total_actual_price = i.actual_price
            refund_price = 0
            translation_expense = i.predict_freight
            balance = origin_balance - i.actual_price - i.predict_freight + income
            statement_data.append(
                FinalStatementOutputData(create_date, origin_balance, income, total_actual_price, refund_price,
                                         translation_expense, balance))
            origin_balance = balance
        return statement_data


def search_product_statistics(start_date=None, end_date=None, order_by='0'):
    if end_date:
        try:
            end_date = datetime.datetime.strftime(
                datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days=1), '%Y-%m-%d')
        except Exception as e:
            print(e, '--------', type(e))
            end_date = None
    product_statistics = []
    product_ids = [i[0] for i in ProductInfo.objects.filter(is_delete=False).values_list('pro_id')]

    # 没有起始和结束时间
    if not (start_date or end_date):
        total_count = sum(i.storage_pro_count for i in StorageOutDetail.objects.filter(is_delete=False))
        if total_count:
            for pro_id in product_ids:
                pro_count = sum(
                    [i.storage_pro_count for i in
                     StorageOutDetail.objects.filter(is_delete=False).filter(pro_id=pro_id)])
                pro_percent = pro_count / total_count * 100
                product_statistics.append((pro_id, pro_count, pro_percent))

            # 排序
            if order_by == '0':
                product_statistics.sort(key=lambda x: x[0])
            elif order_by == '1':
                product_statistics.sort(key=lambda x: x[1])
            elif order_by == '2':
                product_statistics.sort(key=lambda x: -x[1])

            return product_statistics, total_count
        else:
            return [], 0

    # 有起始时间，无结束时间
    elif start_date and not end_date:
        print('起始...')
        print(type(start_date))
        storage_out_order_id = [i.pur_id for i in
                                StorageOut.objects.filter(is_delete=False).filter(storage_create_date__gte=start_date)]
        total_count = sum(i.storage_pro_count for i in
                          StorageOutDetail.objects.filter(pur_id__in=storage_out_order_id).filter(is_delete=False))

    # 无起始时间，有结束时间
    elif not start_date and end_date:
        storage_out_order_id = [i.pur_id for i in
                                StorageOut.objects.filter(is_delete=False).filter(storage_create_date__lte=end_date)]
        total_count = sum(i.storage_pro_count for i in
                          StorageOutDetail.objects.filter(pur_id__in=storage_out_order_id).filter(is_delete=False))

    # 有起始时间和结束时间
    else:
        storage_out_order_id = [i.pur_id for i in StorageOut.objects.filter(is_delete=False).filter(
            storage_create_date__gte=start_date).filter(storage_create_date__lte=end_date)]
        total_count = sum(i.storage_pro_count for i in
                          StorageOutDetail.objects.filter(pur_id__in=storage_out_order_id).filter(is_delete=False))

    if total_count:
        for pro_id in product_ids:
            pro_count = sum(
                [i.storage_pro_count for i in
                 StorageOutDetail.objects.filter(pur_id__in=storage_out_order_id).filter(is_delete=False).filter(
                     pro_id=pro_id)])
            pro_percent = pro_count / total_count * 100
            product_statistics.append((pro_id, pro_count, pro_percent))

        # 排序
        if order_by == '0':
            product_statistics.sort(key=lambda x: x[0])
        elif order_by == '1':
            product_statistics.sort(key=lambda x: x[1])
        elif order_by == '2':
            product_statistics.sort(key=lambda x: -x[1])

        return product_statistics, total_count
    else:
        return [], 0


# 设置默认搜索时间（当前时间减少一个月）
def change_date(t):
    t_temp = t.month
    if t_temp in (5, 7, 10, 12):
        t_last = t - datetime.timedelta(days=30)
    elif t_temp in (1, 2, 4, 6, 8, 9, 11):
        t_last = t - datetime.timedelta(days=31)
    else:
        t_last = t - datetime.timedelta(days=28)
    return t_last
