import datetime
import os

from django.http import JsonResponse, HttpResponse, FileResponse
from django.shortcuts import render, redirect

# Create your views here.
from common import rds
from common.excel_operation import export_to_excel
from plan.helper import CreatePlanDetail, create_excel_data
from plan.models import PlanList, PlanDetail
from purchase.models import PurchaseDetail, Purchase
from storage.models import ProductInfo


def plan_manage(request):
    data = {'title': '生产管理'}
    return render(request, 'plan_manage.html', data)


def create_plan(request):
    if request.method == 'POST':
        rds.delete('plan_detail')
        order_list = request.POST.getlist('order_id[]')
        plan_list = PurchaseDetail.objects.filter(pur_id__in=order_list)
        for i in plan_list:
            rds.zincrby('plan_detail', i.pro_id, i.pur_pro_count)
        return JsonResponse({'code': '888'})
    else:
        plan = PlanList()
        plan_detail_lt = [CreatePlanDetail(i[0], i[1]) for i in rds.zrange('plan_detail', 0, -1, withscores=True) if i[1] != 0]
        lt_sort = sorted(plan_detail_lt, key=lambda i: i.pro_id)
        data = {
            'title': '生产安排',
            'plan_detail': lt_sort,
            'plan': plan,
        }
        return render(request, 'create_plan.html', data)


def del_plan_detail(request):
    data = {}
    pro_id = request.POST.get('pro_id')
    rds.zrem('plan_detail', str(pro_id))
    data['code'] = '888'
    return JsonResponse(data)


def add_plan_detail(request):
    pro_id = request.POST.get('pro_id')
    pro_count = request.POST.get('pro_count')
    if ProductInfo.objects.filter(pro_id=pro_id) and pro_count != 0:
        rds.zadd('plan_detail', pro_id, pro_count)
    return JsonResponse({'code': '888'})


def clear_plan_detail(request):
    rds.delete('plan_detail')
    return redirect('/plan/create_plan/')


def submit_plan_detail(request):
    data = {'code': None}
    if rds.zrange('plan_detail', 0, -1, withscores=True):
        date_now = datetime.datetime.now().date()
        if PlanList.objects.filter(plan_create_time__year=date_now.year, plan_create_time__month=date_now.month, plan_create_time__day=date_now.day):
            plan_id = PlanList.objects.filter(plan_create_time__year=date_now.year, plan_create_time__month=date_now.month,
                                    plan_create_time__day=date_now.day).first().id
            PlanList.objects.filter(plan_create_time__year=date_now.year, plan_create_time__month=date_now.month,
                                    plan_create_time__day=date_now.day).first().delete()
            PlanDetail.objects.filter(plan_id=plan_id).delete()
        PlanList.objects.create()
        plan_id = PlanList.objects.last().id
        plan_detail_list = [PlanDetail(plan_id=plan_id, plan_pro_id=str(i[0]), plan_count=int(i[1])) for i in
                            rds.zrange('plan_detail', 0, -1, withscores=True)]
        PlanDetail.objects.bulk_create(plan_detail_list)
        data = create_excel_data()
        file_path = export_to_excel(data)
        data = {
            'code': os.path.split(file_path)[-1]
        }
    return JsonResponse(data)


def clear_rds(request):
    rds.delete('plan_detail')
    pur = Purchase.objects.filter(is_delete=False).filter(is_selected=True).filter(pur_status__in=['0', '2'])
    for foo in pur:
        foo.pur_status = '1'
        foo.save()
    data = {
        'code': '888'
    }
    return JsonResponse(data)


def file_down(request):
    file_name = request.GET.get('file_name')
    file = open( os.path.join('/home/fish/project/syc/file_bak/plan', file_name), 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=' + file_name
    return response
