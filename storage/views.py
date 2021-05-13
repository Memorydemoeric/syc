from urllib.parse import quote

from django.db.models import Q
from django.http import JsonResponse, FileResponse
from django.shortcuts import render, redirect
from common import rds

from common.excel_operation import excel_to_pro, export_purchase_list

# Create your views here.
from common.file_operation import purchase_output_path, upload_storage_in_info
from purchase.models import PurchaseDetail, Purchase
from report.models import CashFlow, CustomerRank, StatementOutputDetail
from storage.helper import OutDetail, create_storage_out_list, purchase_compare, AllStorageInfo
from storage.models import ProductInfo, HalfFinishInfo, ProductRecord, HalfFinishRecord, StorageInProduct, \
    StorageInDetailHalf, StorageInHalf, StorageInDetailProduct
from user.models import UserInfo


def storage_manage(request):
    data = {
        'title': '库存管理'
    }
    return render(request, 'storage_manage.html', data)


def product_storage(request):
    if request.method == 'GET':
        count_order = request.GET.get('order_by_count', '0')
        storage_product_info = ProductInfo.objects.filter(is_delete=False).order_by('pro_id')
        total = sum([i.pro_count for i in storage_product_info])
        if count_order == '1':
            storage_product_info = storage_product_info.order_by('pro_count')
        elif count_order == '2':
            storage_product_info = storage_product_info.order_by('-pro_count')
        data = {
            'title': '成品管理',
            'storage_product_info': storage_product_info,
            'total': total,
            'order': count_order,
        }
        return render(request, 'product_storage.html', data)
    else:
        pro_id = request.POST.get('pro_id')
        storage_product_info = ProductInfo.objects.filter(is_delete=False).filter(pro_id__contains=pro_id).order_by('pro_id')
        total = sum([i.pro_count for i in storage_product_info])
        data = {
            'title': '成品管理',
            'storage_product_info': storage_product_info,
            'total': total
        }
        return render(request, 'product_storage.html', data)


def half_storage(request):
    if request.method == 'GET':
        count_order = request.GET.get('order_by_count', '0')
        storage_half_finish = HalfFinishInfo.objects.filter(is_delete=False).order_by('half_id')
        total = sum([i.half_count for i in storage_half_finish])
        if count_order == '1':
            storage_half_finish = storage_half_finish.order_by('half_count')
        elif count_order == '2':
            storage_half_finish = storage_half_finish.order_by('-half_count')
        data = {
            'title': '半成品管理',
            'storage_half_finish': storage_half_finish,
            'total': total,
            'order': count_order,
        }
        return render(request, 'half_storage.html', data)
    else:
        pro_id = request.POST.get('pro_id')
        storage_half_finish = HalfFinishInfo.objects.filter(is_delete=False).filter(half_id__contains=pro_id).order_by('half_id')
        total = sum([i.half_count for i in storage_half_finish])
        data = {
            'title': '成品管理',
            'storage_half_finish': storage_half_finish,
            'total': total
        }
        return render(request, 'half_storage.html', data)


def all_storage(request):
    if request.method == 'GET':
        pro_count_order = request.GET.get('pro_order', '0')
        half_count_order = request.GET.get('half_order', '0')
        if not pro_count_order.isdigit() or not half_count_order.isdigit():
            pro_count_order = '0'
            half_count_order = '0'
        product_info = ProductInfo.objects.filter(is_delete=False).order_by('pro_id')
        half_info = HalfFinishInfo.objects.filter(is_delete=False).order_by('half_id')
        all_storage_info = [AllStorageInfo(pro_id=i.pro_id, pro_count=i.pro_count,
                                           half_count=half_info.get(half_id=i.pro_id).half_count) for i in product_info]

        if pro_count_order == '0':
            if half_count_order == '1':
                all_storage_info.sort(key=lambda x: x.half_count)
            elif half_count_order == '2':
                all_storage_info.sort(key=lambda x: -x.half_count)
        elif pro_count_order == '1':
            if half_count_order == '0':
                all_storage_info.sort(key=lambda x: x.pro_count)
            elif half_count_order == '1':
                all_storage_info.sort(key=lambda x: (x.pro_count, x.half_count))
            elif half_count_order == '2':
                all_storage_info.sort(key=lambda x: (x.pro_count, -x.half_count))
        elif pro_count_order == '2':
            if half_count_order == '0':
                all_storage_info.sort(key=lambda x: -x.pro_count)
            elif half_count_order == '1':
                all_storage_info.sort(key=lambda x: (-x.pro_count, x.half_count))
            elif half_count_order == '2':
                all_storage_info.sort(key=lambda x: (-x.pro_count, -x.half_count))

        product_total = sum([i.pro_count for i in all_storage_info])
        half_total = sum([i.half_count for i in all_storage_info])
        total = half_total + product_total
        data = {
            'title': '全部库存',
            'storage_all': all_storage_info,
            'total': total,
            'pro_order': pro_count_order,
            'half_order': half_count_order,
            'pre_pro_order': str(int(pro_count_order) + 1) if int(pro_count_order) < 2 else '0',
            'pre_half_order': str(int(half_count_order) + 1) if int(half_count_order) < 2 else '0',
        }
        return render(request, 'all_storage.html', data)
    else:
        pro_id = request.POST.get('pro_id')
        product_info = ProductInfo.objects.all().filter(pro_id=pro_id)
        half_info = HalfFinishInfo.objects.all()
        all_storage_info = [AllStorageInfo(pro_id=i.pro_id, pro_count=i.pro_count,
                                           half_count=half_info.get(half_id=i.pro_id).half_count) for i in product_info]
        product_total = sum([i.pro_count for i in all_storage_info])
        half_total = sum([i.half_count for i in all_storage_info])
        total = half_total + product_total
        data = {
            'title': '全部库存',
            'storage_all': all_storage_info,
            'total': total
        }
        return render(request, 'all_storage.html', data)


def alter_storage(request):
    storage_type = request.POST.get('type')
    storage_id = request.POST.get('pro_id')
    storage_count = request.POST.get('count')
    if storage_type == 'product':
        storage_product = ProductInfo.objects.get(pro_id=storage_id)
        old_count = storage_product.pro_count
        storage_product.pro_count = storage_count
        storage_product.save()
        ProductRecord.product_modify(pro_id=storage_id, operate='M', old_count=int(old_count),
                                     new_count=int(storage_count))
        data = {
            'code': '888'
        }
        return JsonResponse(data)
    elif storage_type == 'half':
        storage_half = HalfFinishInfo.objects.get(half_id=storage_id)
        old_count = storage_half.half_count
        storage_half.half_count = storage_count
        storage_half.save()
        HalfFinishRecord.half_modify(pro_id=storage_id, operate='M', old_count=int(old_count),
                                     new_count=int(storage_count))
        data = {
            'code': '999'
        }
        return JsonResponse(data)


def product_storage_in(request):
    rds.delete('product_storage_members')
    for member in ProductInfo.objects.all():
        rds.sadd('product_storage_members', member.pro_id)
    modify_info = rds.zrange('product_storage_in_list', 0, -1, withscores=True)
    total_count = sum([i[1] for i in modify_info])
    modify_info.sort(key=lambda x: x[0])
    data = {
        'title': '成品入库',
        'in_info': modify_info,
        'total_count': total_count,
    }
    return render(request, 'product_storage_in.html', data)


def storage_in_add(request):
    data = {}
    pro_id = request.POST.get('pro_id')
    pro_count = request.POST.get('pro_count')
    if rds.sismember('product_storage_members', pro_id) and pro_count:
        if rds.sismember('product_storage_in_members', pro_id):
            data['code'] = '000'
            data['pro_id'] = pro_id
            data['pro_count'] = pro_count
        else:
            rds.sadd('product_storage_in_members', pro_id)
            data['code'] = '888'
        rds.zincrby('product_storage_in_list', str(pro_id), int(pro_count))
    else:
        data['code'] = '999'
    return JsonResponse(data)


def storage_in_clear(request):
    data = {}
    if request.POST.get('order') == 'clear_list':
        rds.delete('product_storage_in_list', 'product_storage_in_members', 'product_storage_temp')
        data['code'] = '888'
    return JsonResponse(data)


def storage_in_detail_modify(request):
    pro_id = request.POST.get('pro_id')
    pro_count = request.POST.get('pro_count')
    pro_old_count = request.POST.get('pro_old_count')
    count_change = int(pro_count) - int(pro_old_count)
    rds.zincrby('product_storage_in_list', pro_id, count_change)
    data = {'code': '888'}
    return JsonResponse(data)


def storage_in_detail_del(request):
    pro_id = request.POST.get('pro_id')
    pro_count = request.POST.get('pro_count')
    rds.zincrby('product_storage_in_list', pro_id, -int(pro_count))
    if rds.zscore('product_storage_in_list', pro_id) == 0:
        rds.srem('product_storage_in_members', pro_id)
        rds.zrem('product_storage_in_list', pro_id)
    data = {'code': '888'}
    return JsonResponse(data)


def storage_in_confirm(request):
    old_info = sorted(ProductInfo.objects.filter(pro_id__in=list(rds.smembers('product_storage_in_members'))),
                      key=lambda x: x.pro_id)
    storage_in_list = sorted(rds.zrange('product_storage_in_list', 0, -1, withscores=True), key=lambda x: x[0])
    if rds.zrange('storage_temp', 0, -1):
        rds.delete('storage_temp')
    for i in range(len(old_info)):
        old_info[i].in_count = storage_in_list[i][1]
        old_info[i].new_info = old_info[i].pro_count + old_info[i].in_count
        rds.zadd('storage_temp', old_info[i].pro_id, old_info[i].new_info)
    data = {
        'title': '成品入库',
        'old_info': old_info,
    }
    return render(request, 'product_storage_in_confirm.html', data)


def storage_in_submit(request):
    product_infos = ProductInfo.objects.filter(pro_id__in=rds.smembers('product_storage_in_members'))
    half_infos = HalfFinishInfo.objects.filter(half_id__in=rds.smembers('product_storage_in_members'))
    StorageInProduct.objects.create(
        in_total_count=sum([i[1] for i in rds.zrange('product_storage_in_list', 0, -1, withscores=True)]))
    in_pur_id = StorageInProduct.objects.last().id
    for i in sorted(rds.zrange('product_storage_in_list', 0, -1, withscores=True), key=lambda x: x[0]):
        product_info = product_infos.get(pro_id=i[0])
        ProductRecord.product_modify(pro_id=i[0], old_count=product_info.pro_count,
                                     new_count=product_info.pro_count + i[1], operate='I')
        product_info.pro_count += i[1]
        product_info.save()
        half_info = half_infos.get(half_id=i[0])
        HalfFinishRecord.half_modify(pro_id=i[0], old_count=half_info.half_count, new_count=half_info.half_count - i[1],
                                     operate='O')
        half_info.half_count -= i[1]
        half_info.save()
        StorageInDetailProduct.objects.create(pro_id=i[0].decode('utf-8'), in_count=i[1], in_pur_id=in_pur_id)
    rds.delete('product_storage_in_list', 'product_storage_in_members', 'product_storage_temp')
    return redirect('/storage/')


def storage_outing(request):
    pur_id_list = request.POST.getlist('order_id[]')
    for i in rds.smembers('storage_outing_set'):
        rds.delete('storage_out_' + i.decode('utf-8'))
    rds.delete('storage_outing_set')
    rds.delete('storage_out_submit')
    rds.delete('storage_out_handler')
    for num in pur_id_list:
        rds.sadd('storage_outing_set', num)
        header = 'storage_out_' + num
        storage_outing_list = PurchaseDetail.objects.filter(pur_id=int(num))
        for foo in storage_outing_list:
            rds.zadd(header, foo.pro_id, foo.pur_pro_count)
    return JsonResponse({'code': '888'})


def storege_out_reset(request):
    data = {}
    ord_id = request.POST.get('order_id')
    header = 'storage_out_' + ord_id
    print(ord_id)
    rds.srem('storage_out_submit', ord_id)
    rds.delete(header)
    storage_outing_list = PurchaseDetail.objects.filter(pur_id=int(ord_id))
    for foo in storage_outing_list:
        rds.zadd(header, foo.pro_id, foo.pur_pro_count)
    data['code'] = '888'
    return JsonResponse(data)


def product_storage_out(request):
    out_select = sorted(Purchase.objects.filter(is_delete=False).filter(pk__in=rds.smembers('storage_outing_set')),
                        key=lambda x: x.id)
    ord_id = request.GET.get('ord_id')
    page_scroll = request.GET.get('scroll')
    if out_select:
        if ord_id:
            storage_out_list = sorted([OutDetail(i[0], i[1], Purchase.objects.get(pk=ord_id).rebate) for i in
                                       rds.zrange('storage_out_' + ord_id, 0, -1, withscores=True)],
                                      key=lambda x: x.pro_id)
            total_count = sum([i.pro_count for i in storage_out_list])
            total_ordinary_price = sum([i.pro_ordinary_price for i in storage_out_list])
            total_price = sum([i.pro_price for i in storage_out_list])
            user_info = UserInfo.objects.filter(is_delete=False).filter(~Q(id=1))
            # print(storage_out_list)
            # print(ord_id)
            is_out = [int(i.decode('utf-8')) for i in rds.smembers('storage_out_submit')]
            translation_expense_dict = rds.hgetall('storage_out_translation')
            translation_expense = translation_expense_dict.get(ord_id.encode('utf-8'), '')
            query_handler = rds.hget('storage_out_handler', ord_id).decode('utf-8') if rds.hget('storage_out_handler',
                                                                                                ord_id) else None
            data = {
                'title': '成品出库',
                'out_select': out_select,
                'out_detail': storage_out_list,
                'ord_id': int(ord_id),
                'total_count': total_count,
                'total_ordinary_price': total_ordinary_price,
                'total_price': total_price,
                'is_out': is_out,
                'user_info': user_info,
                'query_user': query_handler,
                'translation_expense': translation_expense,
                'page_scroll': page_scroll
            }
            return render(request, 'product_storage_out.html', data)
        else:
            return redirect('/storage/product_storage_out/?ord_id=' + str(out_select[0].id))
    else:
        return render(request, 'product_storage_out.html')


def product_storage_out_edit(request):
    ord_id = request.POST.get('ord_id')
    pro_id = request.POST.get('pro_id')
    pro_count = request.POST.get('pro_count')
    if ord_id and pro_id and pro_count:
        rds.zadd('storage_out_' + ord_id, pro_id, int(pro_count))
        if str(ord_id).encode('utf-8') in rds.smembers('storage_out_submit'):
            rds.srem('storage_out_submit', str(ord_id))
    return JsonResponse({'code': '888'})


def product_storage_out_del(request):
    ord_id = request.POST.get('ord_id')
    pro_id = request.POST.get('pro_id')
    if ord_id and pro_id:
        rds.zrem('storage_out_' + ord_id, pro_id)
        if str(ord_id).encode('utf-8') in rds.smembers('storage_out_submit'):
            rds.srem('storage_out_submit', str(ord_id))
    return JsonResponse({'code': '888'})


def product_storage_out_submit(request):
    ord_id = request.POST.get('ord_id')
    handler = request.POST.get('pur_handler')
    translation_expense = request.POST.get('translation_expense')
    rds.sadd('storage_out_submit', ord_id)
    rds.hset('storage_out_handler', ord_id, handler)
    rds.hset('storage_out_translation', ord_id, translation_expense)
    return JsonResponse({'code': '888'})


def storage_out_commit(request):
    if request.POST.get('order') == 'storage_out_commit' and rds.smembers('storage_outing_set'):
        order_id_list = [i.decode('utf-8') for i in sorted(rds.smembers('storage_outing_set'))]
        handler_dict = rds.hgetall('storage_out_handler')
        translation_expense = rds.hgetall('storage_out_translation')
        rds.delete('storage_out_increase_temp')
        for i in order_id_list:
            storage_out_cache_elements, storage_actual_price, cust_id = create_storage_out_list(
                ord_id=i, pur_handler=handler_dict[i.encode('utf-8')].decode('utf-8'),
                translation_expense=translation_expense[i.encode('utf-8')].decode('utf-8')
            )
            for foo in storage_out_cache_elements:
                rds.zincrby('storage_out_increase_temp', foo[0], foo[1])
            storage_out_temp = sorted(rds.zrange('storage_out_increase_temp', 0, -1, withscores=True),
                                      key=lambda x: x[0])
            product_infos = ProductInfo.objects.all()
            for foo in storage_out_temp:
                product_info = product_infos.get(pro_id=foo[0].decode('utf-8'))
                product_info.pro_count -= int(foo[1])
                product_info.save()
            purchase_compare(ord_id=i, pur_handler=handler_dict[i.encode('utf-8')].decode('utf-8'))
            cash_change = storage_actual_price + float(translation_expense[i.encode('utf-8')].decode('utf-8'))
            customer_rank_info = CustomerRank.objects.get(cust_id=cust_id)
            balance = customer_rank_info.balance - cash_change
            customer_rank_info.balance = balance
            customer_rank_info.save()
            CashFlow.objects.create(cust_id=cust_id, pur_id=int(i), flow_type='O', cash_change=cash_change,
                                    balance=balance)
            if StatementOutputDetail.objects.filter(pur_id=int(i)):
                statement_output_detail_info = StatementOutputDetail.objects.get(pur_id=int(i))
                statement_output_detail_info.pur_actual_price = cash_change
                statement_output_detail_info.update_balance()
                for j in StatementOutputDetail.objects.filter(id__gt=statement_output_detail_info.id).filter(
                        cust_id=cust_id):
                    j.origin_balance -= cash_change
                    j.update_balance()
            else:
                StatementOutputDetail.objects.create(cust_id=cust_id, origin_balance=balance + cash_change,
                                                     pur_id=int(i), pur_actual_price=cash_change, balance=balance)
            rds.delete('storage_out_increase_temp')
            rds.delete('storage_out_' + i)
        rds.delete('storage_outing_set')
    return JsonResponse({'code': '888'})


def half_storage_in(request):
    rds.delete('half_storage_members')
    for member in HalfFinishInfo.objects.all():
        rds.sadd('half_storage_members', member.half_id)
    modify_info = rds.zrange('half_storage_in_list', 0, -1, withscores=True)
    total_count = sum([i[1] for i in modify_info])
    modify_info.sort(key=lambda x: x[0])
    data = {
        'title': '半成品入库',
        'in_info': modify_info,
        'total_count': total_count,
    }
    return render(request, 'half_storage_in.html', data)


def half_storage_in_add(request):
    data = {}
    pro_id = request.POST.get('pro_id')
    pro_count = request.POST.get('pro_count')
    if rds.sismember('half_storage_members', pro_id) and pro_count:
        if rds.sismember('half_storage_in_members', pro_id):
            data['code'] = '000'
            data['pro_id'] = pro_id
            data['pro_count'] = pro_count
        else:
            rds.sadd('half_storage_in_members', pro_id)
            data['code'] = '888'
        rds.zadd('half_storage_in_list', str(pro_id), int(pro_count))
    else:
        data['code'] = '999'
    return JsonResponse(data)


def half_storage_in_clear(request):
    data = {}
    if request.POST.get('order') == 'clear_list':
        rds.delete('half_storage_in_list', 'half_storage_in_members', 'half_storage_temp')
        data['code'] = '888'
    return JsonResponse(data)


def half_storage_in_detail_modify(request):
    pro_id = request.POST.get('pro_id')
    pro_count = request.POST.get('pro_count')
    rds.zadd('half_storage_in_list', pro_id, int(pro_count))
    data = {'code': '888'}
    return JsonResponse(data)


def half_storage_in_detail_del(request):
    pro_id = request.POST.get('pro_id')
    rds.zrem('half_storage_in_list', pro_id)
    rds.srem('half_storage_in_members', pro_id)
    data = {'code': '888'}
    return JsonResponse(data)


def half_storage_in_confirm(request):
    old_info = sorted(HalfFinishInfo.objects.filter(half_id__in=list(rds.smembers('half_storage_in_members'))),
                      key=lambda x: x.half_id)
    storage_in_list = sorted(rds.zrange('half_storage_in_list', 0, -1, withscores=True), key=lambda x: x[0])
    if rds.zrange('half_storage_temp', 0, -1):
        rds.delete('half_storage_temp')
    for i in range(len(old_info)):
        old_info[i].in_count = storage_in_list[i][1]
        old_info[i].new_info = old_info[i].half_count + old_info[i].in_count
        rds.zadd('half_storage_temp', old_info[i].half_id, old_info[i].new_info)
    data = {
        'title': '半成品入库',
        'old_info': old_info,
    }
    return render(request, 'half_storage_in_confirm.html', data)


def half_storage_in_submit(request):
    half_infos = HalfFinishInfo.objects.filter(half_id__in=rds.smembers('half_storage_in_members'))
    StorageInHalf.objects.create(
        in_total_count=sum([i[1] for i in rds.zrange('half_storage_in_list', 0, -1, withscores=True)]))
    in_pur_id = StorageInHalf.objects.last().id
    for i in sorted(rds.zrange('half_storage_in_list', 0, -1, withscores=True), key=lambda x: x[0]):
        half_info = half_infos.get(half_id=i[0])
        HalfFinishRecord.half_modify(pro_id=i[0], old_count=half_info.half_count, new_count=half_info.half_count + i[1],
                                     operate='I')
        half_info.half_count += i[1]
        half_info.save()
        StorageInDetailHalf.objects.create(pro_id=i[0].decode('utf-8'), in_count=i[1], in_pur_id=in_pur_id)
    rds.delete('half_storage_in_list', 'half_storage_in_members', 'half_storage_temp')
    return redirect('/storage/')


def storage_out_list_output(request):
    order_id = request.POST.get('ord_id')
    purchase_info = Purchase.objects.get(pk=int(order_id)).pur_comment
    cust_info = Purchase.objects.get(pk=int(order_id)).cust_info
    product_infos = ProductInfo.objects.filter(
        pro_id__in=[i.decode('utf-8') for i in rds.zrange('storage_out_' + order_id, 0, -1)])
    data = [(i[0].decode('utf-8'), i[1], product_infos.get(pro_id=i[0].decode('utf-8')).pro_unit_price) for i in
            rds.zrange('storage_out_' + order_id, 0, -1, withscores=True)]
    data.sort(key=lambda x: x[0])
    file_name = export_purchase_list(data=data, file_name=cust_info.cust_location + cust_info.cust_name + purchase_info)
    return JsonResponse({'code': '888', 'file_name': file_name})


def storage_output_download(request):
    file_name = request.GET.get('file_name')
    file_path, out_file_name = purchase_output_path(file_name=file_name)
    file = open(file_path, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=' + quote(out_file_name) + '.xlsx'
    return response


def storage_in_upload(request):
    file_info = request.FILES.get('file_info')
    in_type = 'product'
    file_path = upload_storage_in_info(file_info, in_type)
    lt, check_word = excel_to_pro(file_path, 2, 0)
    if check_word == '成品入库' and in_type == 'product':
        rds.delete('product_storage_in_list', 'product_storage_in_members')
        for i in lt:
            pro_id = str(i[0]).split('.')[0]
            pro_count = int(i[1])
            if rds.sismember('product_storage_members', pro_id):
                rds.sadd('product_storage_in_members', pro_id)
                rds.zadd('product_storage_in_list', pro_id, pro_count)
    return JsonResponse({'code': '888'})


def half_storage_in_upload(request):
    file_info = request.FILES.get('file_info')
    in_type = 'half'
    file_path = upload_storage_in_info(file_info, in_type)
    lt, check_word = excel_to_pro(file_path, 2, 0)
    if check_word == '半成品入库' and in_type == 'half':
        rds.delete('half_storage_in_list', 'half_storage_in_members')
        for i in lt:
            pro_id = str(i[0]).split('.')[0]
            pro_count = int(i[1])
            if rds.sismember('half_storage_members', pro_id):
                rds.sadd('half_storage_in_members', pro_id)
                rds.zadd('half_storage_in_list', pro_id, pro_count)
    return JsonResponse({'code': '888'})
