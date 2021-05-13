import os
from urllib.parse import unquote, quote

from django.http import JsonResponse, FileResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from common.excel_operation import translate_purchase_excel, export_translation_excel
from common.file_operation import upload_translation
from common.security import encrypt_password_by_md5, get_uuid
from report.models import CustomerRank
from syc import settings
from user.models import UserInfo


def system_manage(request):
    data = {
        'title': '系统维护'
    }
    return render(request, 'system_manage.html', data)


def excel_to_excel(request):
    data = {
        'title': 'excel转换'
    }
    if request.method == 'GET':
        return render(request, 'excel_to_excel.html', data)
    else:
        file_info = request.FILES.get('file_upload')
        file_name = request.POST.get('file_name')
        file_path = upload_translation(file_info, file_name)
        lt = translate_purchase_excel(file_path)
        export_translation_excel(lt, file_name)
        return JsonResponse({'code': file_name})


def translation_file_down(request):
    file_name = unquote(request.GET.get('file_name'))
    file = open( os.path.join(settings.PURCHASE_TRANSLATION_ORIGIN, file_name + '.xlsx'), 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=' + quote(file_name) + '.xlsx'
    return response


def sign_in(request):
    data = {'title': '用户登录'}
    return render(request, 'sign_in.html', data)


def check_out_passwd(request):
    data = {}
    passwd = request.POST.get('passwd')
    uuid = get_uuid()

    if UserInfo.objects.filter(telephone_number=passwd).filter(is_delete=False):
        token = encrypt_password_by_md5(uuid)
        request.session['token'] = token
        request.session.set_expiry(0)
        user_info = UserInfo.objects.get(telephone_number=passwd)
        user_info.load_in_token = token
        user_info.save()
        data['code'] = '888'
    else:
        data['code'] = '999'
    return JsonResponse(data)


def power_off(request):
    os.system('init 0') # 需要配合 /sbin/shutdown 权限使用
    return HttpResponse('关机中...')


def show_original_balance(request):
    data = {}
    cust_condition = request.GET.get('cust_condition')
    customer_rank = CustomerRank.objects.filter(is_delete=False)
    if cust_condition:
        customer_rank = [i for i in customer_rank if cust_condition in (i.cust_info.cust_location + i.cust_info.cust_name)]
        data['cust_condition'] = cust_condition
    else:
        customer_rank = CustomerRank.objects.all()
    data['cust_rank'] = customer_rank
    return render(request, 'modify_original_balance.html', data)


def change_original_balance(request):
    data = {}
    new_balance = request.POST.get('new_balance')
    cust_id = request.POST.get('cust_id')
    if CustomerRank.objects.filter(cust_id=int(cust_id)):
        cust_rank = CustomerRank.objects.get(cust_id=int(cust_id))
        cust_rank.balance = float(new_balance)
        cust_rank.save()
    data['code'] = '888'
    return JsonResponse(data)


def clear_temp_xlsx(request):
    data = {}
    operate_code = request.POST.get('operate_code')

    if operate_code == 'ok':
        # 清空服务器缓存信息
        file_bak_path = settings.FILE_BAK
        search_catalog = os.listdir(file_bak_path)
        while search_catalog:
            operate_dir = search_catalog.pop()
            for i in os.listdir(os.path.join(file_bak_path, operate_dir)):
                next_level_dir = os.path.join(operate_dir, i)
                if os.path.isdir(os.path.join(file_bak_path, next_level_dir)):
                    search_catalog.append(os.path.join(file_bak_path, next_level_dir))
                    print(search_catalog)
                else:
                    os.remove(os.path.join(file_bak_path, next_level_dir))
                    print('----------------------------------------------------')
                    print('文件目录', operate_dir)
                    print('删除文件', i)

    data['code'] = '888'
    return JsonResponse(data)
