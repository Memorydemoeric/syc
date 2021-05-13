import datetime
from urllib.parse import quote

from django.db.models import Q

from common.excel_operation import excel_to_pro, create_purchase_statement
from common.my_math_func import my_round
from purchase.helper import OrderDetail
from report.helper import create_statement_purchase_data
from report.models import CustomerRank, CashFlow, StatementOutputDetail
from django.http import JsonResponse, HttpResponse, FileResponse
from django.shortcuts import render, redirect
from common import rds

# Create your views here.
from common.file_operation import upload_purchase_file, create_statement_purchase_directory
from customer.models import CustomerInfo
from purchase.forms import PurchaseForm
from purchase.models import Purchase, PurchaseDetail, RefundPurchase, RefundPurchaseDetail
from storage.models import ProductInfo, HalfFinishInfo, ProductRecord, StorageOut
from user.models import UserInfo


def pur_manage(request):
    data = {
        'title': '销售管理'
    }
    return render(request, 'purchase_manage.html', data)


def show_purchase_order(request):
    data = {'title': '创建订单'}
    if request.method == 'GET':
        cust_info = CustomerInfo.objects.all()
        data['cust_info'] = cust_info
        data['user_info'] = UserInfo.objects.filter(is_delete=False).filter(~Q(id=1))
        data['pur_orders'] = Purchase.objects.filter(is_delete=False).filter(pur_status__in=['0', '1', '2'])
        data['now'] = datetime.datetime.date(datetime.datetime.now()).strftime('%Y-%m-%d')
        return render(request, 'create_purchase_order.html', data)
    else:
        location = request.POST.get('location')
        if location and CustomerInfo.objects.filter(cust_location__contains=location):
            cust_info = CustomerInfo.objects.filter(cust_location__contains=location)
        else:
            cust_info = CustomerInfo.objects.all()
        data['cust_info'] = [{'id': cust.id, 'name': cust.cust_name} for cust in cust_info]
        return JsonResponse(data)


def create_purchase_order(request):
    form = PurchaseForm(request.POST)
    if form.is_valid():
        form.save()
    else:
        print(form.errors)
    return redirect('/purchase/show_pur/')


def delete_purchase_order(request):
    id = request.POST.get('id').split('_')[-1]
    purchase_order = Purchase.get_purchase_order_by_id(id=id)
    if purchase_order:
        purchase_order.is_delete = True
        purchase_order.save()
    data = {'code': 'ok'}
    return JsonResponse(data)


def edit_purchase_order(request):
    data = {'title': '订单编辑'}
    ord_id = request.GET.get('ord_id')
    if Purchase.objects.filter(pk=int(ord_id)):
        pur_info = Purchase.objects.get(pk=int(ord_id))
        if not pur_info.rebate:
            pur_info.rebate = pur_info.cust_info.cust_rebate
            pur_info.save()
    rds.delete('order_' + str(ord_id))
    for i in PurchaseDetail.objects.filter(pur_id=int(ord_id)):
        rds.zincrby('order_' + str(ord_id), i.pro_id, i.pur_pro_count)
    data['order'] = Purchase.objects.get(pk=ord_id)
    data['order_detail'] = PurchaseDetail.get_order_detail(ord_id=ord_id)
    data['count'] = sum([i.pur_pro_count for i in data['order_detail']])
    data['price'] = sum([i.pur_pro_price for i in data['order_detail']])
    return render(request, 'edit_purchase_order.html', data)


def edit_purchase_date(request):
    data = {}
    try:
        purchase = Purchase.objects.get(pk=request.POST.get('order_id'))
        purchase.pur_modify_date = request.POST.get('new_date')
        purchase.save()
    except Exception as e:
        print(e)
    else:
        data['code'] = 'ok'
    return JsonResponse(data)


def add_product(request):
    data = {}
    order_id = request.GET.get('ord_id')
    pro_id = request.POST.get('pro_id')
    upload_file = request.FILES.get('file_in')
    if ProductInfo.objects.filter(pro_id=pro_id):
        product_info = ProductInfo.objects.get(pro_id=pro_id)
        data['pro_type'] = product_info.pro_type
        data['pro_unit_price'] = product_info.pro_unit_price
    if pro_id:
        if ProductInfo.objects.filter(pro_id=pro_id):
            # product_info = ProductInfo.objects.get(pro_id=pro_id)
            pro_count = request.POST.get('pro_count')
            rds.zincrby('order_' + order_id, pro_id, pro_count)
        else:
            data['code'] = '000'
            return JsonResponse(data)
    elif upload_file:
        file_data = []
        total_count = 0
        total_price = 0
        product_info = ProductInfo.objects.all()
        path = upload_purchase_file(Purchase.objects.get(pk=order_id).cust_info.cust_location + Purchase.objects.get(
            pk=order_id).cust_info.cust_name, upload_file)
        lt, check = excel_to_pro(path=path, column_num=2, sheet_num=0)
        for foo in lt:
            data_dict = {}

            # 判断导入数据格式
            if not str(foo[0]).split('.')[0].isdecimal() or not str(foo[1]).split('.')[0].isdecimal():
                # print(type(str(foo[0]).split('.')[0]), str(foo[0]).split('.')[0], type(str(foo[1])), str(foo[1]))
                return JsonResponse({'code': '222'})

            data_pro_id = str(foo[0]).split('.')[0]
            data_pro_count = int(foo[1])
            data_pro_type = product_info.get(pro_id=data_pro_id).pro_type
            data_pro_unit_price = product_info.get(pro_id=data_pro_id).pro_unit_price
            data_pro_price = data_pro_unit_price * data_pro_count
            data_dict['data_pro_id'] = data_pro_id
            data_dict['data_pro_count'] = data_pro_count
            data_dict['data_pro_type'] = data_pro_type
            data_dict['data_pro_unit_price'] = data_pro_unit_price
            data_dict['data_pro_price'] = data_pro_price
            file_data.append(data_dict)
            total_count += data_pro_count
            total_price += data_pro_price

            rds.zincrby('order_' + order_id, str(foo[0]).split('.')[0], foo[1])
        data['file_data'] = sorted(file_data, key=lambda x: x['data_pro_id'])
        data['total_count'] = total_count
        data['total_price'] = total_price
    data['code'] = '888'
    return JsonResponse(data)


def del_product(request):
    data = {}
    order_id = request.POST.get('order_id')
    pur_pro_id = request.POST.get('pro_id')
    pro_count = request.POST.get('pro_count')
    rds.zincrby('order_' + order_id, pur_pro_id, -int(pro_count))
    data['code'] = '888'
    return JsonResponse(data)


def complete_purchase_detail(request):
    data = {}
    order_id = request.POST.get('ord_id')
    predict_freight = request.POST.get('predict_freight')
    for i in rds.zrange('order_' + order_id, 0, -1):
        rds.sadd('members_of_order_' + order_id, i)
    for i in rds.zrange('order_' + order_id, 0, -1, withscores=True):
        pro_id = i[0].decode('utf-8')
        if PurchaseDetail.objects.filter(pur_id=order_id).filter(pro_id=pro_id):
            purchase_detail_info = PurchaseDetail.objects.filter(pur_id=order_id).get(pro_id=pro_id)
            if i[1] != 0:
                purchase_detail_info.pur_pro_count = int(i[1])
                purchase_detail_info.pur_pro_price = purchase_detail_info.product_info.pro_unit_price * purchase_detail_info.pur_pro_count
                purchase_detail_info.save()
            else:
                purchase_detail_info.delete()
        else:
            product_info = ProductInfo.objects.get(pro_id=pro_id)
            PurchaseDetail.objects.create(pur_id=int(order_id), pro_id=pro_id, pur_pro_count=int(i[1]),
                                          pur_pro_price=product_info.pro_unit_price * int(i[1]))
    pur_info = Purchase.objects.get(pk=order_id)
    pur_info.predict_freight = my_round(float(predict_freight))
    pur_info.update_price()
    rds.delete('order_' + order_id)
    data['code'] = 'ok'
    return JsonResponse(data)


def query_purchase(request):
    # 替换为redis, incrby -- query_purchase_detail
    # 记录是否出现的redis, sadd -- query_purchase_members
    # 记录变动purchase_id, sadd -- query_purchase_id
    if request.method == 'GET':
        data = {'title': '订单管理'}
        body_scroll = request.GET.get('body_scroll')
        order_detail = []
        rds.delete('query_purchase_members', 'query_purchase_detail', 'query_purchase_id')
        order_infos = Purchase.objects.filter(is_delete=False).filter(pur_status__in=['0', '1', '2'])
        purchase_details = PurchaseDetail.objects.filter(pur_id__in=[i.id for i in order_infos.filter(is_finished=False).filter(is_selected=True)])
        for i in order_infos.filter(is_finished=False).filter(is_selected=True):
            pur_id = i.id
            purchase_detail_infos = purchase_details.filter(pur_id=pur_id)
            rds.sadd('query_purchase_id', pur_id)
            for j in purchase_detail_infos:
                rds.zincrby('query_purchase_detail', j.pro_id, j.pur_pro_count)
                rds.sadd('query_purchase_members', j.pro_id)

        pro_id_members = [i.decode('utf-8') for i in rds.smembers('query_purchase_members')]
        storage_infos = ProductInfo.objects.filter(pro_id__in=pro_id_members)
        half_storage_infos = HalfFinishInfo.objects.filter(half_id__in=pro_id_members)

        for k in pro_id_members:
            order_detail.append(
                OrderDetail(pro_id=k, pro_count=rds.zscore('query_purchase_detail', k.encode('utf-8')),
                            storage_detail=storage_infos, half_storage_detail=half_storage_infos))

        data['order_infos'] = order_infos.order_by('pur_modify_date')
        data['order_detail'] = sorted(order_detail, key=lambda x: x.pro_id)
        data['body_scroll'] = body_scroll
        return render(request, 'query_purchase.html', data)
    else:
        return HttpResponse('error...')


def select_purchase(request):
    data = {}
    all_select = request.POST.get('all_select')
    if all_select != None:
        purchase_infos = Purchase.objects.filter(is_delete=False).filter(pur_status__in=['0', '1', '2']).filter(is_finished=False)
        purchase_infos.update(is_selected=all_select)
        data['code'] = '888'
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        purchase_infos = Purchase.objects.filter(pk=id)
        purchase_infos.update(is_selected=status)
        data['code'] = '888'
    return JsonResponse(data)


def select_detail(request):
    data = {}
    select_purchase = Purchase.objects.filter(is_delete=False).filter(pur_status__in=['0', '1', '2']).filter(is_selected=True)
    purchase_id = [i.id for i in select_purchase]
    detail_infos = PurchaseDetail.objects.filter(pur_id__in=purchase_id)
    if request.POST.get('check') == 'show_select_detail':
        detail_dict = {}
        for i in detail_infos:
            if not detail_dict.get(i.pro_id):
                detail_dict[i.pro_id] = i.pur_info.cust_info.cust_location + i.pur_info.cust_info.cust_name + 'X' + str(i.pur_pro_count)
            else:
                detail_dict[i.pro_id] += '  ' + i.pur_info.cust_info.cust_location + i.pur_info.cust_info.cust_name + 'X' + str(
                    i.pur_pro_count)
        data['pur_detail'] = detail_dict
        data['code'] = '888'
    return JsonResponse(data)


def comment_purchase_order(request):
    id = request.POST.get('order_id')
    comment = request.POST.get('comment')
    pur_info = Purchase.objects.get(pk=int(id))
    pur_info.pur_comment = comment
    pur_info.save()
    data = {'code': 'ok'}
    return JsonResponse(data)


def modify_date(request):
    ord_id = request.POST.get('ord_id')
    new_date = request.POST.get('new_date')
    Purchase_info = Purchase.objects.get(pk=ord_id)
    Purchase_info.pur_modify_date = new_date
    Purchase_info.save()
    data = {
        'code': '888'
    }
    return JsonResponse(data)


def refund_purchase(request):
    data = {
        'title': '客户退货',
    }
    cust_info = CustomerInfo.objects.all()
    data['cust_info'] = cust_info
    return render(request, 'refund_purchase.html', data)


def refund_select(request):
    data = {'cust_info':{}}
    location = request.POST.get('location')
    cust_infos = CustomerInfo.objects.filter(cust_location__contains=location).filter(is_delete=False)
    for i in cust_infos:
        data['cust_info'][i.cust_name] = i.id
    data['code'] = '888'
    return JsonResponse(data)


def refund_purchase_detail(request):
    data = {
        'title': '退货明细'
    }
    cust_id = request.GET.get('cust_id')
    if rds.zrange('refund_list', 0, -1, withscores=True):
        refund_list = sorted(rds.zrange('refund_list', 0, -1, withscores=True), key=lambda x: x[0])
        refund_purchase_detail = [i for i in refund_list]
        data['refund_purchase_detail'] = refund_purchase_detail
        data['total_count'] = sum([i[1] for i in refund_purchase_detail])
    else:
        data['total_count'] = 0
    data['cust_info'] = CustomerInfo.objects.get(pk=cust_id)
    return render(request, 'refund_purchase_detail.html', data)


def refund_purchase_detail_add(request):
    pro_id = request.POST.get('pro_id')
    pro_count = request.POST.get('pro_count')
    if pro_count:
        pro_count = int(pro_count)
    if ProductInfo.objects.filter(pro_id=pro_id):
        rds.zadd('refund_list', pro_id, pro_count)
    return JsonResponse({'code': '888'})


def refund_purchase_detail_delete(request):
    pro_id = request.POST.get('pro_id')
    rds.zrem('refund_list', pro_id)
    return JsonResponse({'code': '888'})


# 退货提交
def refund_purchase_detail_submit(request):
    return_code = request.POST.get('code')
    cust_id = request.POST.get('cust_id')
    actual_rebate = request.POST.get('rebate')

    if return_code == 'submit_refund' and cust_id:
        RefundPurchase.objects.create(ref_cust_id=int(cust_id))
        ref_purchase_id = RefundPurchase.objects.last().id
        for i in rds.zrange('refund_list', 0, -1, withscores=True):
            RefundPurchaseDetail.objects.create(ref_pro_id=i[0], ref_pro_count=int(i[1]),
                                                ref_purchase_id=ref_purchase_id)
            ref_pro_info = ProductInfo.objects.get(pro_id=i[0])
            ProductRecord.objects.create(pro_id=i[0], pro_operate='R', pro_old_count=ref_pro_info.pro_count,
                                         pro_new_count=ref_pro_info.pro_count + int(i[1]), pro_change_count=int(i[1]))
            ref_pro_info.pro_count += int(i[1])
            ref_pro_info.save()
        cust_info = CustomerInfo.objects.get(pk=int(cust_id))
        if not actual_rebate:
            cust_rebate = cust_info.cust_rebate
        else:
            cust_rebate = actual_rebate
        refund_purchase_order_info = RefundPurchase.objects.last()
        refund_id = refund_purchase_order_info.id
        # 按照订单折扣退货？
        cash_change = my_round(sum([i.pro_info.pro_unit_price * i.ref_pro_count * cust_rebate / 100 for i in
                           RefundPurchaseDetail.objects.filter(ref_purchase_id=refund_id)]))
        cust_rank_info = CustomerRank.objects.get(cust_id=int(cust_id))
        old_balance = cust_rank_info.balance
        new_balance = old_balance + cash_change
        cust_rank_info.balance = new_balance
        cust_rank_info.save()
        CashFlow.objects.create(cust_id=int(cust_id), flow_type='B', cash_change=cash_change, balance=new_balance,
                                ref_pur_id=refund_id)

        statement_output_detail_info = StatementOutputDetail.objects.filter(cust_id=cust_info.id).last()
        statement_output_detail_info.ref_pur_id = refund_id
        statement_output_detail_info.ref_pur_price = cash_change
        statement_output_detail_info.update_balance()
        for i in StatementOutputDetail.objects.filter(id__gt=statement_output_detail_info.id).filter(cust_id=int(cust_id)):
            i.origin_balance += cash_change
            i.update_balance()

        rds.delete('refund_list')
    return JsonResponse({'code': '888'})


def receipt(request):
    cust_condition = request.POST.get('cust_condition')
    if not CustomerRank.objects.all():
        for i in CustomerInfo.objects.all():
            CustomerRank.objects.create(cust_id=i.id)
    cust_info = CustomerRank.objects.filter(is_delete=False).order_by()
    if cust_condition:
        cust_info = sorted(
            [i for i in cust_info if cust_condition in (i.cust_info.cust_location + i.cust_info.cust_name)],
            key=lambda x: x.latest_pur_date, reverse=True)
    else:
        cust_info = cust_info.order_by('-latest_pur_date')
        cust_condition = ''
    data = {
        'title': '收款',
        'cust_info': cust_info,
        'cust_condition': cust_condition,
    }
    return render(request, 'receipt.html', data)


def receipt_income(request):
    data = {
        'title': '收款金额',
    }
    cust_id = request.GET.get('cust_id')
    data['infos'] = []
    if cust_id and CustomerRank.objects.filter(is_delete=False).filter(cust_id=int(cust_id)):
        purchase_infos = Purchase.objects.filter(is_delete=False).filter(cust_id=int(cust_id)).filter(payment_status=0)
        storage_out_infos = StorageOut.objects.filter(cust_id=int(cust_id)).filter(payment_status=0)
        cust_info = CustomerRank.objects.get(cust_id=int(cust_id))
        for i in purchase_infos:
            if i.pur_status != '3':
                data['infos'].append(i)
                print('没有出库...')
            else:
                print('已经出库...')
                data['infos'].append(storage_out_infos.get(pur_id=i.id))
        data['cust_info'] = cust_info
    return render(request, 'receipt_income.html', data)


def receipt_income_submit(request):
    cust_id = request.POST.get('cust_id')
    income = request.POST.get('account', 0.00)
    pur_id_list = request.POST.getlist('pur_id[]')
    if cust_id and CustomerRank.objects.filter(is_delete=False).filter(cust_id=int(cust_id)) and pur_id_list:
        cust_rank_info = CustomerRank.objects.get(cust_id=int(cust_id))
        cust_rank_info.balance += float(income)
        cust_rank_info.save()
    for i in pur_id_list:
        # 已经出库的订单处理
        if StorageOut.objects.filter(pur_id=int(i)):
            storage_out_info = StorageOut.objects.get(pur_id=int(i))
            purchase_info = Purchase.objects.get(pk=int(i))
            storage_out_info.payment_status = True
            purchase_info.payment_status = True
            if float(
                    income) + cust_rank_info.balance >= storage_out_info.storage_actual_price + storage_out_info.translation_expense:
                storage_out_info.is_enough = True
                purchase_info.is_enough = True
                is_enough = True
            else:
                is_enough = False
            purchase_info.save()
            storage_out_info.save()
            CashFlow.objects.create(cust_id=int(cust_id), flow_type='I', cash_change=float(income),
                                    balance=cust_rank_info.balance, pur_id=int(i), is_enough=is_enough)

            statement_output_detail_info = StatementOutputDetail.objects.get(pur_id=int(i))
            statement_output_detail_info.income = float(income)
            statement_output_detail_info.update_balance()
            for i in StatementOutputDetail.objects.filter(id__gt=statement_output_detail_info.id).filter(cust_id=int(cust_id)):
                i.origin_balance += float(income)
                i.update_balance()



        # 未出库的订单处理
        elif Purchase.objects.filter(pk=int(i)):
            purchase_info = Purchase.objects.get(pk=int(i))
            purchase_info.payment_status = True
            if float(
                    income) + cust_rank_info.balance >= my_round(purchase_info.pur_price * purchase_info.rebate / 100) + purchase_info.predict_freight:
                purchase_info.is_enough = True
                is_enough = True
            else:
                is_enough = False
            purchase_info.save()
            CashFlow.objects.create(cust_id=int(cust_id), flow_type='I', cash_change=float(income),
                                    balance=cust_rank_info.balance, pur_id=int(i), is_enough=is_enough)

            StatementOutputDetail.objects.create(cust_id=cust_id, origin_balance=cust_rank_info.balance - float(income),
                                                 pur_id=int(i), income=float(income), balance=cust_rank_info.balance)
    return JsonResponse({'code': '888'})


def output_statement(request):
    cust_id = request.GET.get('cust_id')
    pur_id = request.GET.get('pur_id')
    cust_info = CustomerInfo.objects.get(pk=int(cust_id))
    purchase_info = Purchase.objects.get(pk=int(pur_id))
    path = create_statement_purchase_directory()
    total_count = purchase_info.count
    total_price = purchase_info.pur_price
    total_actual_price = purchase_info.actual_price
    statement_data = create_statement_purchase_data(int(cust_id), int(pur_id))
    file_path, file_name = create_purchase_statement(cust_info=cust_info, purchase_info=purchase_info, path=path,
                                                     total_count=total_count,
                                                     total_price=total_price, total_actual_price=total_actual_price,
                                                     statement_data=statement_data)
    file = open(file_path, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=' + quote(file_name) + '.xlsx'
    return response


def edit_purchase_rebate(request):
    data = {}
    new_rebate = request.POST.get('rebate')
    ord_id = request.POST.get('ord_id')
    print(new_rebate, ord_id)
    if Purchase.objects.filter(pk=int(ord_id)):
        purchase_info = Purchase.objects.get(pk=int(ord_id))
        purchase_info.rebate = int(new_rebate)
        purchase_info.save()
    data['code'] = '888'
    return JsonResponse(data)


def change_handler(request):
    data = {}
    user_id = request.POST.get('user_id')
    pur_id = request.POST.get('pur_id')
    if user_id.isdigit() and pur_id.isdigit():
        if Purchase.objects.filter(id=int(pur_id)):
            purchase_info = Purchase.objects.get(id=int(pur_id))
            purchase_info.pur_handle = UserInfo.objects.get(id=int(user_id)).user_name
            purchase_info.save()
            print('cust_id:', user_id, pur_id)
            data['code'] = '888'
            data['user_name'] = purchase_info.pur_handle
    return JsonResponse(data)