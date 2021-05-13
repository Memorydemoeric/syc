from urllib.parse import quote

from common.file_operation import create_statement_finish_directory
from common.my_math_func import my_round
from report.helper import create_statement_output_data, search_product_statistics, change_date
from storage.helper import storage_in_product_info_change, storage_in_half_info_change, \
    storage_in_detail_product_info_change, storage_in_product_info_order_change, storage_in_detail_half_info_change, \
    storage_in_half_info_order_change
from syc import settings
from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import render, redirect

import datetime
# Create your views here.
from common import rds
from common.excel_operation import create_statement
from customer.models import CustomerInfo
from purchase.models import RefundPurchase, RefundPurchaseDetail, Purchase, PurchaseDetail
from report.models import CustomerRank, CashFlow, StatementOutputDetail
from storage.models import StorageOut, StorageOutDetail, ProductInfo, ProductRecord, StorageInProduct, StorageInHalf, \
    StorageInDetailProduct, StorageInDetailHalf, HalfFinishInfo, HalfFinishRecord
from user.models import UserInfo


def report_manage(request):
    data = {
        'title': '报表管理'
    }
    return render(request, 'report_manage.html', data)


def report_list_order(request):
    date_end = datetime.date.today()
    date_start = change_date(date_end)
    if request.method == 'GET':
        date_data = StorageOut.objects.filter(storage_create_date__gte=date_start).order_by('-storage_create_date')
        addition_count = sum([i.total_count for i in date_data])
        addition_price = sum([i.storage_actual_price for i in date_data])
        data = {
            'title': '历史订单查询',
            'storage_out': date_data,
            'date_start': date_start.isoformat(),
            'date_end': date_end.isoformat(),
            'addition_count': addition_count,
            'addition_price': addition_price,
        }
        return render(request, 'report_list_order.html', data)
    else:
        date_start = request.POST.get('date_start')
        date_end = request.POST.get('date_end')
        cust_condition = request.POST.get('cust_condition')
        if date_start:
            std_date_start = datetime.datetime.strptime(date_start, '%Y-%m-%d')
            date_data = StorageOut.objects.filter(storage_create_date__gte=std_date_start)
            if date_end:
                new_date_end = datetime.datetime.strptime(date_end, '%Y-%m-%d') + datetime.timedelta(days=1)
                date_data = date_data.filter(storage_create_date__lt=new_date_end)
        elif date_end:
            new_date_end = datetime.datetime.strptime(date_end, '%Y-%m-%d') + datetime.timedelta(days=1)
            date_data = StorageOut.objects.filter(storage_create_date__lt=new_date_end)
        else:
            date_data = StorageOut.objects.all()
        if cust_condition:
            date_data = [i for i in date_data if cust_condition in i.cust_info.cust_location + i.cust_info.cust_name]
            date_data = sorted(date_data, key=lambda x: x.storage_create_date, reverse=True)
        else:
            date_data = date_data.order_by('-storage_create_date')
        addition_count = sum([i.total_count for i in date_data])
        addition_price = sum([i.storage_actual_price for i in date_data])
        data = {
            'title': '历史订单查询',
            'storage_out': date_data,
            'location': cust_condition,
            'date_start': date_start,
            'date_end': date_end,
            'addition_count': addition_count,
            'addition_price': addition_price,
        }
        return render(request, 'report_list_order.html', data)


def report_storage_out_detail(request):
    order_id = int(request.GET.get('order_id'))
    if Purchase.objects.filter(pk=order_id):
        purchase_info = Purchase.objects.get(pk=order_id)
    if purchase_info.pur_status == '3':
        storage_out = StorageOut.objects.get(pur_id=order_id)
        storage_out_detail = StorageOutDetail.objects.filter(pur_id=order_id).filter(is_delete=False).order_by('pro_id')
        data = {
            'title': '历史订单详情',
            'storage_out': storage_out,
            'storage_out_detail': storage_out_detail,
        }

        return render(request, 'report_storage_out_detail.html', data)
    elif purchase_info.pur_status in ['0', '1', '2']:
        purchase_detail = PurchaseDetail.objects.filter(pur_id=order_id).order_by('pro_id')
        data = {
            'title': '历史订单详情',
            'purchase_info': purchase_info,
            'purchase_detail': purchase_detail,
        }
        return render(request, 'report_purchase_detail.html', data)


def statement(request):
    data = {
        'title': '对账单'
    }
    if not CustomerRank.objects.all():
        for i in CustomerInfo.objects.filter(is_delete=False):
            CustomerRank.objects.create(cust_id=i.id)
    thirty_days_before = datetime.datetime.now().date() - datetime.timedelta(days=30)
    cust_info = CustomerRank.objects.filter(is_delete=False)
    cust_rank_info = cust_info.filter(latest_pur_date__gt=thirty_days_before).order_by('-latest_pur_date')[0:12]
    data['cust_rank_info'] = cust_rank_info
    data['cust_info'] = cust_info
    return render(request, 'statement.html', data)


def statement_select_location(request):
    data = {}
    location = request.POST.get('location')
    all_cust_info = CustomerInfo.objects.all()
    cust_info = all_cust_info.filter(cust_location__contains=location)
    if cust_info:
        cust_info_list = [{'id': i.id, 'cust_name': i.cust_name} for i in cust_info]
    else:
        cust_info_list = [{'id': i.id, 'cust_name': i.cust_name} for i in all_cust_info]
    data['code'] = '888'
    data['cust_info'] = cust_info_list
    return JsonResponse(data)


def statement_detail(request):
    data = {
        'title': '对账单明细'
    }
    cust_id = request.GET.get('cust_id')
    if cust_id and CustomerRank.objects.filter(is_delete=False).filter(cust_id=int(cust_id)):
        cust_info = CustomerRank.objects.get(cust_id=int(cust_id))
        statement_detail = CashFlow.objects.filter(cust_id=int(cust_id)).order_by('-flow_date')
        data['cust_info'] = cust_info
        data['statement_detail'] = statement_detail
    return render(request, 'report_statement_detail.html', data)


def translation_expense_edit(request):
    data = {}
    old_translation_expense = request.POST.get('old_translation_expense')
    new_translation_expense = request.POST.get('new_translation_expense')
    pur_id = request.POST.get('pur_id')
    if StorageOut.objects.filter(pur_id=int(pur_id)):
        storage_out_info = StorageOut.objects.get(pur_id=int(pur_id))
        storage_out_info.translation_expense = float(new_translation_expense)
        storage_out_info.save()
        cust_id = storage_out_info.cust_id

        customer_rank_info = CustomerRank.objects.get(cust_id=cust_id)
        old_balance = customer_rank_info.balance
        cash_change = float(new_translation_expense) - float(old_translation_expense)
        new_balance = old_balance - cash_change
        customer_rank_info.balance = new_balance
        customer_rank_info.save()

        reference_cash_flow = CashFlow.objects.filter(flow_type='O').get(pur_id=int(pur_id))
        reference_cash_flow.cash_change += cash_change
        reference_cash_flow.balance -= cash_change
        reference_cash_flow.save()

        cash_flow_infos = CashFlow.objects.filter(cust_id=cust_id).filter(flow_type__in=['I', 'O', 'C']).filter(
            pk__gt=reference_cash_flow.id)
        for i in cash_flow_infos:
            storage_out_info = StorageOut.objects.get(pur_id=i.pur_id)
            i.balance -= cash_change
            if i.balance >= storage_out_info.translation_expense + storage_out_info.storage_actual_price:
                storage_out_info.is_enough = True
                i.is_enough = True
            else:
                storage_out_info.is_enough = False
                i.is_enough = False
            i.save()
            storage_out_info.save()

        statement_output_info = StatementOutputDetail.objects.get(pur_id=int(pur_id))
        statement_output_info.pur_actual_price += cash_change
        statement_output_info.update_balance()
        for i in StatementOutputDetail.objects.filter(id__gt=statement_output_info.id):
            i.origin_balance -= cash_change
            i.update_balance()
    else:
        purchase_info = Purchase.objects.get(id=int(pur_id))
        purchase_info.predict_freight = float(new_translation_expense)
        purchase_info.save()

    data['code'] = '888'
    return JsonResponse(data)


def report_refund_detail(request):
    data = {
        'title': '退货明细'
    }
    refund_id = request.GET.get('refund_id')
    if refund_id and RefundPurchase.objects.filter(pk=int(refund_id)):
        refund_info = RefundPurchase.objects.get(pk=int(refund_id))
        cust_info = refund_info.cust_info
        refund_detail_info = refund_info.refund_purchase_detail
        total_actual_price = my_round(refund_info.total_price * cust_info.cust_rebate / 100)
        data['cust_info'] = cust_info
        data['refund_detail_info'] = refund_detail_info
        data['refund_info'] = refund_info
        data['total_actual_price'] = total_actual_price
    return render(request, 'report_refund_detail.html', data)


def translation_comment_edit(request):
    pur_id = request.POST.get('pur_id')
    comment_containt = request.POST.get('comment_containt')
    if pur_id and StorageOut.objects.filter(pur_id=int(pur_id)):
        storage_out_info = StorageOut.objects.get(pur_id=pur_id)
        storage_out_info.translation_comment = comment_containt
        storage_out_info.save()
    elif pur_id and Purchase.objects.filter(id=int(pur_id)):
        purchase_info = Purchase.objects.get(id=int(pur_id))
        purchase_info.pur_comment = comment_containt
        purchase_info.save()
    return JsonResponse({'code': '888'})


def edit_report_detail(request):
    data = {
        'title': '历史订单修改'
    }
    pur_id = request.GET.get('pur_id')
    if pur_id and StorageOut.objects.filter(pur_id=int(pur_id)):
        storage_out_order_info = StorageOut.objects.get(pur_id=int(pur_id))
        storage_out_detail = StorageOutDetail.objects.filter(pur_id=int(pur_id)).filter(is_delete=False).order_by(
            'pro_id')
        data['storage_out_order_info'] = storage_out_order_info
        data['storage_out_detail'] = storage_out_detail
        if rds.smembers('statement_ord_' + pur_id + '_detail_set'):
            rds.delete('statement_ord_' + pur_id + '_detail_set')
            rds.delete('statement_edit_ord_' + pur_id + '_detail')
            rds.delete('statement_edit_ord_' + pur_id + '_pro_list')
        for i in storage_out_detail:
            rds.sadd('statement_ord_' + pur_id + 'old_detail_set', i.pro_id)
            rds.sadd('statement_ord_' + pur_id + '_detail_set', i.pro_id)
            rds.zadd('statement_edit_ord_' + pur_id + '_detail', i.pro_id, i.storage_pro_count)
    return render(request, 'report_edit_storage_out_detail.html', data)


def edit_report_detail_modify(request):
    data = {}
    pur_id = request.POST.get('pur_id')
    pro_id = request.POST.get('pro_id')
    pro_count = request.POST.get('pro_count')
    if pur_id and pro_id and pro_count:
        if ProductInfo.objects.filter(pro_id=int(pro_id)):
            product_info = ProductInfo.objects.get(pro_id=int(pro_id))
            if pro_id in [i.decode('utf-8') for i in rds.smembers('statement_ord_' + pur_id + '_detail_set')]:
                old_pro_count = rds.zscore('statement_edit_ord_' + pur_id + '_detail', pro_id)
                count_change = int(pro_count) - int(old_pro_count)
                data['count_change'] = count_change
                data['code'] = '999'
            else:
                data['code'] = '888'
            data['storage_unit_price'] = product_info.pro_unit_price
            data['storage_pro_price'] = product_info.pro_unit_price * int(pro_count)
            data['cust_rebate'] = Purchase.objects.get(pk=int(pur_id)).rebate
            rds.zadd('statement_edit_ord_' + pur_id + '_detail', pro_id, int(pro_count))
            rds.sadd('statement_ord_' + pur_id + '_detail_set', pro_id)
            rds.zadd('statement_edit_ord_' + pur_id + '_pro_list', pro_id, int(pro_count))
        else:
            data['code'] = '000'
    else:
        data['code'] = '000'
    return JsonResponse(data)


def edit_report_detail_delete(request):
    data = {}
    pur_id = request.POST.get('pur_id')
    pro_id = request.POST.get('pro_id')
    rds.zadd('statement_edit_ord_' + pur_id + '_detail', pro_id, 0)
    rds.zadd('statement_edit_ord_' + pur_id + '_pro_list', pro_id, 0)
    rds.sadd('statement_ord_' + pur_id + '_detail_set', pro_id)
    pur_info = StorageOut.objects.get(pur_id=int(pur_id))
    cust_rebate = pur_info.rebate
    data['code'] = '888'
    data['rebate'] = cust_rebate
    return JsonResponse(data)


def edit_report_detail_submit(request):
    data = {}
    # storage_out 订单信息
    pur_id = request.POST.get('pur_id')
    storage_price = request.POST.get('storage_price')
    storage_actual_price = request.POST.get('storage_actual_price')

    storage_product_info = ProductInfo.objects.all()
    pur_info = StorageOut.objects.get(pur_id=int(pur_id))
    cust_info = pur_info.cust_info
    cust_rank_info = CustomerRank.objects.get(cust_id=cust_info.id)
    storage_out_detail_infos = StorageOutDetail.objects.filter(pur_id=int(pur_id)).filter(is_delete=False)
    cash_change = pur_info.storage_actual_price - float(storage_actual_price)
    balance = cust_rank_info.balance + cash_change

    # storage_out_detail 订单信息
    edit_storage_out_detail = rds.zrange('statement_edit_ord_' + pur_id + '_pro_list', 0, -1, withscores=True)
    old_storage_out_detail = rds.smembers('statement_ord_' + pur_id + 'old_detail_set')
    for i in edit_storage_out_detail:
        pro_id = i[0].decode('utf-8')
        pro_count = int(i[1])
        old_pro_count = 0
        change_count = pro_count - old_pro_count
        storage_pro_price = storage_product_info.get(pro_id=pro_id).pro_unit_price * pro_count

        # 是否需要记录每个产品的实际价格
        storage_pro_actual_price = storage_product_info.get(
            pro_id=pro_id).pro_unit_price * pro_count * Purchase.objects.get(pk=int(pur_id)).rebate / 100

        old_storage_count = storage_product_info.get(pro_id=pro_id).pro_count
        if i[0] in old_storage_out_detail:
            old_pro_count = storage_out_detail_infos.get(pro_id=pro_id).storage_pro_count
            # 查找修改 产品编号 产品数量 合计零售价 实际价格
            change_count = pro_count - old_pro_count
            if int(i[1]) == 0:  # 删除

                # 删除出库记录信息
                detail_info = storage_out_detail_infos.get(pro_id=pro_id)
                detail_info.is_delete = True
                detail_info.save()

            else:  # 修改
                detail_info = storage_out_detail_infos.get(pro_id=pro_id)
                detail_info.storage_pro_count = pro_count
                detail_info.storage_pro_price = storage_pro_price
                detail_info.storage_pro_actual_price = storage_pro_actual_price
                detail_info.save()

        # 添加 产品编号 产品数量 金额 实际价格
        else:  # 添加
            StorageOutDetail.objects.create(pro_id=pro_id, storage_pro_count=pro_count,
                                            storage_pro_price=storage_pro_price,
                                            storage_pro_actual_price=storage_pro_actual_price, pur_id=int(pur_id))

            # 库存记录添加
        ProductRecord.objects.create(pro_id=pro_id, pro_operate='M', pro_old_count=old_storage_count,
                                     pro_new_count=old_storage_count - change_count, pro_change_count=-change_count)

        # 修改库存
        product_info = storage_product_info.get(pro_id=pro_id)
        product_info.pro_count -= change_count
        product_info.save()

    cust_rank_info.balance = balance
    cust_rank_info.save()
    # cash_flow 订单信息 订单id 客户id 类型=C 变化值 最终余额
    CashFlow.objects.create(cust_id=cust_info.id, pur_id=int(pur_id), flow_type='C', cash_change=cash_change,
                            balance=balance)
    pur_info.storage_actual_price = float(storage_actual_price)
    pur_info.storage_price = float(storage_price)
    pur_info.save()

    statement_output_detail = StatementOutputDetail.objects.get(pur_id=int(pur_id))
    statement_output_detail.pur_actual_price -= cash_change
    statement_output_detail.update_balance()
    for i in StatementOutputDetail.objects.filter(id__gt=statement_output_detail.id).filter(cust_id=cust_info.id):
        i.origin_balance -= cash_change
        i.update_balance()

    rds.delete('statement_ord_' + pur_id + 'old_detail_set')
    rds.delete('statement_ord_' + pur_id + '_detail_set')
    rds.delete('statement_edit_ord_' + pur_id + '_detail')

    data['code'] = '888'
    return JsonResponse(data)


def statement_output(request):
    cust_id = request.GET.get('cust_id')
    pur_id = request.GET.get('pur_id')
    cust_info = CustomerInfo.objects.get(pk=int(cust_id))
    storage_out_info = StorageOut.objects.get(pur_id=int(pur_id))
    path = create_statement_finish_directory()
    total_count = storage_out_info.total_count
    total_price = storage_out_info.storage_price
    total_actual_price = storage_out_info.storage_actual_price
    statement_data = create_statement_output_data(int(cust_id), int(pur_id))
    file_path, file_name = create_statement(cust_info=cust_info, storage_out_info=storage_out_info, path=path,
                                            total_count=total_count,
                                            total_price=total_price, total_actual_price=total_actual_price,
                                            statement_data=statement_data)
    file = open(file_path, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=' + quote(file_name) + '.xlsx'
    return response


def report_change_income(request):
    data = {}
    print('通过验证...')
    pur_id = request.POST.get('pur_id')
    new_income = request.POST.get('new_income')
    cash_flow_info = CashFlow.objects.filter(flow_type='I').get(pur_id=int(pur_id))
    modify_cash_flow_date = cash_flow_info.flow_date

    old_income = cash_flow_info.cash_change
    old_balance = cash_flow_info.balance
    cash_change = float(new_income) - float(old_income)
    cash_flow_info.cash_change += cash_change
    cash_flow_info.save()

    statement_output_detail = StatementOutputDetail.objects.get(pur_id=int(pur_id))
    statement_output_detail.income += cash_change
    statement_output_detail.update_balance()
    for i in StatementOutputDetail.objects.filter(id__gt=statement_output_detail.id).filter(
            cust_id=statement_output_detail.cust_id):
        i.origin_balance += cash_change
        i.update_balance()

    all_cash_flow = CashFlow.objects.filter(flow_date__gte=modify_cash_flow_date).order_by('flow_date')
    for i in all_cash_flow:
        i.balance += cash_change
        if StorageOut.objects.filter(pur_id=i.pur_id):
            storage_out_info = StorageOut.objects.get(pur_id=i.pur_id)
            if float(
                    new_income) + i.balance >= storage_out_info.storage_actual_price + storage_out_info.translation_expense:
                is_enough = True
            else:
                is_enough = False
            storage_out_info.is_enough = is_enough
            storage_out_info.save()
        else:
            print('id:', i.id)
            print('pur_id:', i.pur_id)
            purchase_info = Purchase.objects.get(id=i.pur_id)
            if float(new_income) + i.balance >= purchase_info.predict_freight + purchase_info.actual_price:
                is_enough = True
            else:
                is_enough = False
            purchase_info.is_enough = is_enough
            purchase_info.save()
        i.is_enough = is_enough
        i.save()

    cust_id = cash_flow_info.cust_id
    cust_rank_info = CustomerRank.objects.get(cust_id=cust_id)
    cust_rank_info.balance = all_cash_flow.last().balance
    cust_rank_info.save()
    data['code'] = '888'
    data['cust_id'] = cust_id
    return JsonResponse(data)


def storage_in_product(request):
    data = {
        'title': '成品入库信息'
    }
    start_time = request.GET.get('start_time', None)
    end_time = request.GET.get('end_time', None)
    if start_time and end_time:
        storage_in_infos = StorageInProduct.objects.filter(in_date__gte=start_time).filter(
            in_date__lte=end_time).filter(is_delete=False).all().order_by('-in_date')
    elif start_time and not end_time:
        storage_in_infos = StorageInProduct.objects.filter(in_date__gte=start_time).filter(
            is_delete=False).all().order_by('-in_date')
    elif not start_time and end_time:
        storage_in_infos = StorageInProduct.objects.filter(in_date__lte=end_time).filter(
            is_delete=False).all().order_by('-in_date')
    else:
        storage_in_infos = StorageInProduct.objects.filter(is_delete=False).all().order_by('-in_date')
    data['storage_in_infos'] = storage_in_infos
    data['start_time'] = start_time
    data['end_time'] = end_time
    return render(request, 'storage_in_product.html', data)


def storage_in_half(request):
    data = {
        'title': '半成品入库信息'
    }
    start_time = request.GET.get('start_time', None)
    end_time = request.GET.get('end_time', None)
    if start_time and end_time:
        storage_in_infos = StorageInHalf.objects.filter(in_date__gte=start_time).filter(in_date__lte=end_time).filter(
            is_delete=False).all().order_by('-in_date')
    elif start_time and not end_time:
        storage_in_infos = StorageInHalf.objects.filter(in_date__gte=start_time).filter(is_delete=False).all().order_by(
            '-in_date')
    elif not start_time and end_time:
        storage_in_infos = StorageInHalf.objects.filter(in_date__lte=end_time).filter(is_delete=False).all().order_by(
            '-in_date')
    else:
        storage_in_infos = StorageInHalf.objects.filter(is_delete=False).all().order_by('-in_date')
    data['storage_in_infos'] = storage_in_infos
    data['start_time'] = start_time
    data['end_time'] = end_time
    return render(request, 'storage_in_half.html', data)


def storage_in_product_detail(request):
    data = {
        'title': '成品入库详情'
    }
    storage_in_id = request.GET.get('storage_in_id')
    rds.delete('storage_in_product_edit_' + storage_in_id)
    rds.delete('storage_in_product_set')
    if storage_in_id.isdigit():
        if StorageInProduct.objects.filter(pk=int(storage_in_id)):
            storage_in_info = StorageInProduct.objects.get(pk=int(storage_in_id))
            data['storage_in_info'] = storage_in_info
        storage_in_product_infos = StorageInDetailProduct.objects.filter(in_pur_id=int(storage_in_id))
        data['storage_in_detail'] = storage_in_product_infos.order_by('pro_id')
        data['storage_in_type'] = 'product'
    return render(request, 'storage_in_detail.html', data)


def storage_in_half_detail(request):
    data = {
        'title': '半成品入库详情'
    }
    storage_in_id = request.GET.get('storage_in_id')
    rds.delete('storage_in_half_edit_' + storage_in_id)
    rds.delete('storage_in_half_set')
    if storage_in_id.isdigit():
        if StorageInHalf.objects.filter(pk=int(storage_in_id)):
            storage_in_info = StorageInHalf.objects.get(pk=int(storage_in_id))
            data['storage_in_info'] = storage_in_info
        storage_in_half_infos = StorageInDetailHalf.objects.filter(in_pur_id=int(storage_in_id)).order_by('pro_id')
        data['storage_in_detail'] = storage_in_half_infos
        data['storage_in_type'] = 'half'
    return render(request, 'storage_in_detail.html', data)


def storage_in_recover(request):
    data = {}
    storage_in_id = request.POST.get('storage_in_id')
    select_type = request.POST.get('select_type')

    # 成品入库撤销操作
    if select_type == 'product' and storage_in_id.isdigit():
        if StorageInProduct.objects.filter(pk=int(storage_in_id)):
            storage_in_info = StorageInProduct.objects.get(pk=int(storage_in_id))
            if storage_in_info:
                storage_in_detail = StorageInDetailProduct.objects.filter(in_pur_id=int(storage_in_id))
                storage_pro_infos = ProductInfo.objects.all()
                storage_half_infos = HalfFinishInfo.objects.all()
                for foo in storage_in_detail:
                    storage_pro_info = storage_pro_infos.get(pro_id=foo.pro_id)
                    storage_half_info = storage_half_infos.get(half_id=foo.pro_id)
                    ProductRecord.objects.create(pro_id=foo.pro_id, pro_operate='M',
                                                 pro_old_count=storage_pro_info.pro_count,
                                                 pro_new_count=storage_pro_info.pro_count - foo.in_count,
                                                 pro_change_count=(-foo.in_count))
                    HalfFinishRecord.objects.create(half_id=foo.pro_id, half_operate='M',
                                                    half_old_count=storage_half_info.half_count,
                                                    half_new_count=storage_half_info.half_count + foo.in_count,
                                                    half_change_count=foo.in_count)
                    storage_pro_info.pro_count -= foo.in_count
                    storage_pro_info.save()
                    storage_half_info.half_count += foo.in_count
                    storage_half_info.save()
                    storage_in_info.is_delete = True
                    storage_in_info.save()
                data['code'] = '888'

    # 半成品入库撤销操作
    elif select_type == 'half' and storage_in_id.isdigit():
        if StorageInHalf.objects.filter(pk=int(storage_in_id)):
            storage_in_info = StorageInHalf.objects.get(pk=int(storage_in_id))
            if storage_in_info:
                storage_in_detail = StorageInDetailHalf.objects.filter(in_pur_id=int(storage_in_id))
                storage_half_infos = HalfFinishInfo.objects.all()
                for foo in storage_in_detail:
                    storage_half_info = storage_half_infos.get(half_id=foo.pro_id)
                    HalfFinishRecord.objects.create(half_id=foo.pro_id, half_operate='M',
                                                    half_old_count=storage_half_info.half_count,
                                                    half_new_count=storage_half_info.half_count - foo.in_count,
                                                    half_change_count=(-foo.in_count))
                    storage_half_info.half_count -= foo.in_count
                    storage_half_info.save()
                    storage_in_info.is_delete = True
                    storage_in_info.save()
                data['code'] = '888'
    else:
        data['code'] = '000'

    return JsonResponse(data)


def storage_in_edit(request):
    data = {}
    pro_id = request.POST.get('pro_id')
    pro_count = request.POST.get('pro_count')
    storage_in_id = request.POST.get('storage_in_id')
    storage_in_type = request.POST.get('storage_in_type')
    rds.zadd('storage_in_' + storage_in_type + '_edit_' + storage_in_id, pro_id, pro_count)
    rds.sadd('storage_in_' + storage_in_type + '_set', pro_id)
    data['code'] = '888'
    return JsonResponse(data)


def storage_in_confirm(request):
    data = {}
    storage_in_type = request.POST.get('storage_in_type')
    storage_in_id = request.POST.get('storage_in_id')
    if request.POST.get('confirm') == 'ok' and storage_in_id.isdigit():

        # 查找原始入库数量
        storage_in_pro_id_list = [foo.decode('utf-8') for foo in rds.smembers('storage_in_' + storage_in_type + '_set')]
        if storage_in_type == 'product':
            storage_in_infos = StorageInDetailProduct.objects.filter(in_pur_id=int(storage_in_id)).filter(
                pro_id__in=storage_in_pro_id_list)
        elif storage_in_type == 'half':
            storage_in_infos = StorageInDetailHalf.objects.filter(in_pur_id=int(storage_in_id)).filter(
                pro_id__in=storage_in_pro_id_list)

        storage_in_change = {i.decode('utf-8'): [storage_in_infos.get(pro_id=i.decode('utf-8')).in_count, int(j)] for
                             i, j in rds.zrange('storage_in_' + storage_in_type + '_edit_' + storage_in_id, 0, -1,
                                                withscores=True)}
        data['storage_in_change_'] = storage_in_change
        data['code'] = '888'
    return JsonResponse(data)


def storage_in_submit(request):
    data = {}
    # 确认后进行数据库操作 分为 product 和 half 两种
    # 相关数据库 ProductInfo/HalfFinishInfo ProductRecord/HalfFinishRecord
    # StorageInProductDetail/StorageInHalfDetail StorageInProduct/StorageInHalf
    submit_status = request.POST.get('submit')
    storage_in_type = request.POST.get('storage_in_type')
    storage_in_id = request.POST.get('storage_in_id')

    # 成品入库数量修改
    if storage_in_id.isdigit() and storage_in_type == 'product' and submit_status == 'ok':
        product_change_list = [(foo[0].decode('utf-8'), foo[1]) for foo in
                               rds.zrange('storage_in_' + storage_in_type + '_edit_' + storage_in_id, 0, -1,
                                          withscores=True)]
        product_id_set = [foo.decode('utf-8') for foo in rds.smembers('storage_in_' + storage_in_type + '_set')]
        print('product_id_set:', product_id_set)
        storage_in_change_infos = StorageInDetailProduct.objects.filter(in_pur_id=int(storage_in_id)).filter(
            pro_id__in=product_id_set)
        total_count_change = 0
        for i in product_change_list:
            old_in_count = storage_in_change_infos.get(pro_id=i[0]).in_count
            new_in_count = i[1]
            in_count_change = new_in_count - old_in_count
            total_count_change += in_count_change

            old_product_count, new_product_count, product_count_change = storage_in_product_info_change(pro_id=i[0],
                                                                                                        in_count_change=in_count_change)
            old_half_count, new_half_count, half_count_change = storage_in_half_info_change(pro_id=i[0],
                                                                                            in_count_change=in_count_change)
            HalfFinishRecord.objects.create(half_id=i[0], half_operate='M', half_old_count=old_half_count,
                                            half_new_count=new_half_count, half_change_count=half_count_change)
            ProductRecord.objects.create(pro_id=i[0], pro_operate='M', pro_old_count=old_product_count,
                                         pro_new_count=new_product_count, pro_change_count=product_count_change)
            storage_in_detail_product_info_change(storage_in_id=int(storage_in_id), pro_id=i[0],
                                                  new_in_count=new_in_count)

            storage_in_product_info_order_change(storage_in_id=int(storage_in_id),
                                                 total_count_change=total_count_change)

        rds.delete('storage_in_' + storage_in_type + '_edit_' + storage_in_id)
        rds.delete('storage_in_' + storage_in_type + '_set')
        data['code'] = '888'
    # 半成品入库数量修改
    elif storage_in_id.isdigit() and storage_in_type == 'half' and submit_status == 'ok':
        product_change_list = [(foo[0].decode('utf-8'), foo[1]) for foo in
                               rds.zrange('storage_in_' + storage_in_type + '_edit_' + storage_in_id, 0, -1,
                                          withscores=True)]
        product_id_set = [foo.decode('utf-8') for foo in rds.smembers('storage_in_' + storage_in_type + '_set')]
        storage_in_change_infos = StorageInDetailHalf.objects.filter(in_pur_id=int(storage_in_id)).filter(
            pro_id__in=product_id_set)
        total_count_change = 0
        for i in product_change_list:
            old_in_count = storage_in_change_infos.get(pro_id=i[0]).in_count
            new_in_count = i[1]
            in_count_change = old_in_count - new_in_count
            total_count_change -= in_count_change

            old_half_count, new_half_count, half_count_change = storage_in_half_info_change(pro_id=i[0],
                                                                                            in_count_change=in_count_change)

            HalfFinishRecord.objects.create(half_id=i[0], half_operate='M', half_old_count=old_half_count,
                                            half_new_count=new_half_count, half_change_count=half_count_change)

            storage_in_detail_half_info_change(storage_in_id=int(storage_in_id), pro_id=i[0], new_in_count=new_in_count)

            storage_in_half_info_order_change(storage_in_id=int(storage_in_id), total_count_change=total_count_change)

        rds.delete('storage_in_' + storage_in_type + '_edit_' + storage_in_id)
        rds.delete('storage_in_' + storage_in_type + '_set')
        data['code'] = '888'
    return JsonResponse(data)


def change_handler(request):
    data = {}
    user_id = request.POST.get('user_id')
    pur_id = request.POST.get('pur_id')
    if user_id.isdigit() and pur_id.isdigit():
        if StorageOut.objects.filter(pur_id=int(pur_id)):
            storage_out_info = StorageOut.objects.get(pur_id=int(pur_id))
            storage_out_info.pur_handler = UserInfo.objects.get(id=int(user_id)).user_name
            storage_out_info.save()
            data['code'] = '888'
    return JsonResponse(data)


def product_statistics(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    order_by = request.GET.get('order_by', '0')
    data = {}
    if not (start_date or end_date):
        print('start1:', start_date)
        print('end1', end_date)
        data['title'] = '产品统计'
        data['product_statistics'], data['total_count'] = search_product_statistics(start_date=start_date,
                                                                                    end_date=end_date,
                                                                                    order_by=order_by)
        data['order_by'] = order_by
        return render(request, 'product_statistics.html', data)
    else:
        print('start2:', start_date)
        print('end2', end_date)
        data['title'] = '产品统计'
        data['product_statistics'], data['total_count'] = search_product_statistics(start_date=start_date,
                                                                                    end_date=end_date,
                                                                                    order_by=order_by)
        data['start_date'] = start_date
        data['end_date'] = end_date
        data['order_by'] = order_by
        return render(request, 'product_statistics.html', data)
