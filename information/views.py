from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from common.excel_operation import excel_to_pro
from common.file_operation import upload_storage_file, upload_customer_file
from common.security import encrypt_password_by_md5
from customer.models import CustomerInfo
from report.models import CustomerRank
from storage.models import ProductInfo, HalfFinishInfo
from user.models import UserInfo


def infomation_manage(request):
    data = {
        'title': '基本资料',
    }
    return render(request, 'info_manage.html', data)


def finish_product_information(request):
    finish_info = sorted(ProductInfo.objects.filter(is_delete=False).all(), key=lambda x: x.pro_id)
    data = {
        'title': '成品信息',
        'info':finish_info,
    }
    return render(request, 'finish_product_information.html', data)


def half_product_information(request):
    half_info = sorted(HalfFinishInfo.objects.filter(is_delete=False).all(), key=lambda x: x.half_id)
    data = {
        'title': '半成品信息',
        'info': half_info,
    }
    return render(request, 'half_product_information.html', data)


def add_product(request):
    pro_id = request.POST.get('pro_id')
    if not ProductInfo.objects.filter(pro_id=pro_id) and pro_id:
        ProductInfo.objects.create(pro_id=pro_id, pro_type='包')
        HalfFinishInfo.objects.create(half_id=pro_id, half_type='半成品')
        return JsonResponse({'code': '888'})
    else:
        return JsonResponse({'code': '000'})


def edit_product(request):
    pro_unit_cost = request.POST.get('pro_info[new_unit_cost]')
    pro_unit_price = request.POST.get('pro_info[new_unit_price]')
    pro_type = request.POST.get('type')
    pro_id = request.POST.get('pro_id')
    if pro_type == 'finish':
        product_info = ProductInfo.objects.get(pro_id=pro_id)
        if pro_unit_price: product_info.pro_unit_price = float(pro_unit_price)
        if pro_unit_cost: product_info.pro_unit_cost = float(pro_unit_cost)
        product_info.save()
    elif pro_type == 'half':
        product_info = HalfFinishInfo.objects.get(half_id=pro_id)
        if pro_unit_price: product_info.half_unit_price = float(pro_unit_price)
        if pro_unit_cost: product_info.half_unit_cost = float(pro_unit_cost)
        product_info.save()
    return JsonResponse({'code': '888'})


def delete_product(request):
    pro_id = request.POST.get('pro_id')
    product_info = ProductInfo.objects.get(pro_id=pro_id)
    product_info.is_delete = True
    product_info.save()
    half_info = HalfFinishInfo.objects.get(half_id=pro_id)
    half_info.is_delete = True
    half_info.save()
    return JsonResponse({'code': '888'})


def upload_storage_info(request):
    data = {}
    file = request.FILES.get('excel')
    pro_type = request.GET.get('pro_type')
    file_path = upload_storage_file(file)
    lt, check_word = excel_to_pro(path=file_path, column_num=5, sheet_num=0)
    for i in lt:
        if check_word == '成品库存' or check_word == '半成品库存':
            if pro_type == 'half':
                i[0] = str(i[0]).split('.')[0]
                half_infos = HalfFinishInfo.objects.filter(half_id=i[0])
                if half_infos:
                    half_info = half_infos.first()
                    half_info.half_count = i[2]
                    half_info.half_unit_cost = i[3] if i[3] else 0.00
                    half_info.half_unit_price = i[4] if i[4] else 0.00
                    half_info.save()
                else:
                    HalfFinishInfo.objects.create(half_id=i[0], half_count=i[2], half_unit_cost=i[3], half_unit_price=i[4])
            if pro_type == 'finish':
                finish_infos = ProductInfo.objects.filter(pro_id=i[0])
                if finish_infos:
                    finish_info = finish_infos.first()
                    finish_info.pro_count = i[2]
                    finish_info.pro_unit_cost = i[3] if i[3] else 0.00
                    finish_info.pro_unit_price = i[4] if i[4] else 0.00
                    finish_info.save()
                else:
                    ProductInfo.objects.create(pro_id=i[0], pro_count=i[2], pro_unit_cost=i[3], pro_unit_price=i[4])
            data['code'] = '888'
        else:
            data['code'] = '000'
    return JsonResponse(data)


def customer_info(request):
    location = request.GET.get('location')
    if location:
        cust_info = [i for i in CustomerInfo.objects.filter(is_delete=False).order_by('cust_location') if location in i.cust_location + i.cust_name]
        if not cust_info:
            cust_info = CustomerInfo.objects.filter(is_delete=False).order_by('cust_location')
    else:
        cust_info = CustomerInfo.objects.all().filter(is_delete=False).order_by('cust_location')
    data = {
        'title': '客户信息',
        'cust_info': cust_info,
    }
    return render(request, 'customer_info.html', data)


def add_customer_info(request):
    cust_location = request.POST.get('cust_location')
    cust_name = request.POST.get('cust_name')
    cust_mobilephone = request.POST.get('cust_mobilephone')
    cust_address = request.POST.get('cust_address')
    cust_phone = request.POST.get('cust_phone')
    cust_rebate = request.POST.get('cust_rebate')
    CustomerInfo.objects.create(cust_location=cust_location, cust_name=cust_name, cust_mobilephone=cust_mobilephone, cust_address=cust_address, cust_phone=cust_phone, cust_rebate=cust_rebate)
    CustomerRank.objects.create(cust_id=CustomerInfo.objects.last().id)
    return JsonResponse({'code': '888'})


def edit_customer_info(request):
    cust_id = request.POST.get('cust_id')
    cust_location = request.POST.get('cust_location')
    cust_name = request.POST.get('cust_name')
    cust_mobilephone = request.POST.get('cust_mobilephone')
    cust_address = request.POST.get('cust_address')
    cust_phone = request.POST.get('cust_phone')
    cust_rebate = request.POST.get('cust_rebate')
    cust_info = CustomerInfo.objects.get(pk=int(cust_id))
    if cust_location: cust_info.cust_location = cust_location
    if cust_name: cust_info.cust_name = cust_name
    if cust_mobilephone: cust_info.cust_mobilephone = cust_mobilephone
    if cust_address: cust_info.cust_address = cust_address
    if cust_phone: cust_info.cust_phone = cust_phone
    if cust_rebate: cust_info.cust_rebate = float(cust_rebate)
    cust_info.save()
    return JsonResponse({'code': '888'})


def delete_customer_info(request):
    cust_id = request.POST.get('pro_id')
    cust_infos = CustomerInfo.objects.filter(pk=int(cust_id))
    if cust_infos:
        cust_info = cust_infos.first()
        cust_info.is_delete = True
        cust_info.save()
        cust_rank = CustomerRank.objects.filter(cust_id=int(cust_id)).first()
        cust_rank.is_delete = True
        cust_rank.save()
    return JsonResponse({'code': '888'})


def upload_customer_info(request):
    file = request.FILES.get('excel')
    file_path = upload_customer_file(file)
    lt, check_word = excel_to_pro(path=file_path, column_num=5, sheet_num=0)
    if check_word == '客户信息':
        for i in lt:
            cust_infos = CustomerInfo.objects.filter(cust_location=i[0]).filter(cust_name=i[1])
            if cust_infos:
                cust_info = cust_infos.first()
                cust_info.cust_location = i[0]
                cust_info.cust_name = i[1]
                cust_info.cust_mobilephone = i[2]
                cust_info.cust_address = i[3]
                cust_info.cust_phone = i[4]
                cust_info.save()
            else:
                CustomerInfo.objects.create(cust_location=i[0], cust_name=i[1], cust_mobilephone=i[2], cust_address=i[3], cust_phone=i[4])
        data = {'code': '888'}
    else:
        data = {'code': '000'}
    return JsonResponse(data)


def show_user_info(request):
    data = {}
    user_info = UserInfo.objects.filter(is_delete=False).all()
    data['user_info'] = user_info
    return render(request, 'user_info.html', data)


def add_user_info(request):
    data = {
        'title': '用户信息'
    }
    user_name = request.POST.get('user_name')
    if user_name and not UserInfo.objects.filter(user_name=user_name):
        UserInfo.objects.create(user_name=user_name)
        new_user_info = UserInfo.objects.get(user_name=user_name)
        data['new_user_info'] = {'user_id':new_user_info.id, 'user_name': new_user_info.user_name, 'telephone_number': new_user_info.telephone_number, 'comment': new_user_info.comment}
        data['code'] = '888'
    else:
        data['code'] = '000'
    return JsonResponse(data)


def del_user_info(request):
    data = {}
    user_id = request.POST.get('user_id')
    if UserInfo.objects.filter(pk=int(user_id)):
        user_info = UserInfo.objects.get(pk=int(user_id))
        user_info.is_delete = True
        user_info.save()
        data['code'] = '888'
    return JsonResponse(data)


def change_user_info(request):
    data = {}
    user_id = request.POST.get('user_id')
    user_name = request.POST.get('user_name')
    user_telephone_number = request.POST.get('user_telephone_number')
    user_comment = request.POST.get('user_comment')
    if UserInfo.objects.filter(pk=user_id):
        user_info = UserInfo.objects.get(pk=user_id)
        user_info.user_name = user_name
        user_info.telephone_number = user_telephone_number
        user_info.password = encrypt_password_by_md5(user_info.user_name + user_info.telephone_number)
        user_info.comment = user_comment
        user_info.save()
    data['code'] = '888'
    return JsonResponse(data)


def get_user_info(request):
    data = {}
    check_word = request.POST.get('get_user_info')
    if check_word == 'ok':
        user_info = {i.id: i.user_name for i in UserInfo.objects.filter(is_delete=False).filter(~Q(id=1))}
        data['user_info'] = user_info
        data['code'] = '888'
    return JsonResponse(data)