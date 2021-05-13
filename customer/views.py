from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from customer.models import CustomerInfo
from common.excel_operation import excel_to_pro


def input_cust(request):
    lt = []
    path = '/home/fish/Desktop/test/cust_info.xls'
    data = excel_to_pro(path=path, column_num=5, sheet_num=0)
    for foo in data:
        lt.append(CustomerInfo(cust_location=foo[0], cust_name=foo[1], cust_mobilephone=foo[2],
                               cust_address=foo[3], cust_phone=foo[4]))
    CustomerInfo.objects.bulk_create(lt)
    return HttpResponse('客户导入成功')