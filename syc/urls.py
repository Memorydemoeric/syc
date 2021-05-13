"""syc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
# from django.contrib import admin
from customer import views as customer_views
from purchase import views as purchase_views
from storage import views as storage_views
from plan import views as plan_views
from information import views as information_views
from report import views as report_views
from system import views as system_views
from salary import views as salary_views

urlpatterns = [
    url(r'^sign_in/$', system_views.sign_in),
    url(r'^check_out_passwd/$', system_views.check_out_passwd),

    url(r'^purchase/$', purchase_views.pur_manage),
    url(r'^purchase/show_pur/$', purchase_views.show_purchase_order),
    url(r'^purchase/output_statement/$', purchase_views.output_statement),
    url(r'^purchase/create_pur/$', purchase_views.create_purchase_order),
    url(r'^purchase/delete_pur/$', purchase_views.delete_purchase_order),
    url(r'^purchase/comment_pur/$', purchase_views.comment_purchase_order),
    url(r'^purchase/edit_pur/$', purchase_views.edit_purchase_order),
    url(r'^purchase/edit_pur_date/$', purchase_views.edit_purchase_date),
    url(r'^purchase/edit_pur_rebate/$', purchase_views.edit_purchase_rebate),
    url(r'^purchase/create_pur_detail/$', purchase_views.add_product),
    url(r'^purchase/del_order_detail/$', purchase_views.del_product),
    url(r'^purchase/complete_order_detail/$', purchase_views.complete_purchase_detail),
    url(r'^purchase/query_purchase/$', purchase_views.query_purchase),
    url(r'^purchase/select_detail/$', purchase_views.select_detail),
    url(r'^purchase/query_purchase/modify_date/$', purchase_views.modify_date),
    url(r'^purchase/select_purchase/$', purchase_views.select_purchase),
    url(r'^purchase/refund_purchase/$', purchase_views.refund_purchase),
    url(r'^purchase/refund_select/$', purchase_views.refund_select),
    url(r'^purchase/refund_purchase_detail/$', purchase_views.refund_purchase_detail),
    url(r'^purchase/refund_purchase_detail_add/$', purchase_views.refund_purchase_detail_add),
    url(r'^purchase/refund_purchase_detail_delete/$', purchase_views.refund_purchase_detail_delete),
    url(r'^purchase/refund_purchase_detail_submit/$', purchase_views.refund_purchase_detail_submit),
    url(r'^purchase/receipt/$', purchase_views.receipt),
    url(r'^purchase/receipt_income/$', purchase_views.receipt_income),
    url(r'^purchase/receipt_income_submit/$', purchase_views.receipt_income_submit),
    url(r'^purchase/change_handler/$', purchase_views.change_handler),

    url(r'^plan/$', plan_views.plan_manage),
    url(r'^plan/create_plan/$', plan_views.create_plan),
    url(r'^plan/add_plan_detail/$', plan_views.add_plan_detail),
    url(r'^plan/del_plan_detail/$', plan_views.del_plan_detail),
    url(r'^plan/clear_plan_detail/$', plan_views.clear_plan_detail),
    url(r'^plan/submit_plan_detail/$', plan_views.submit_plan_detail),
    url(r'^plan/clear_rds/$', plan_views.clear_rds),
    url(r'^plan/file_down/$', plan_views.file_down),

    url(r'^storage/$', storage_views.storage_manage),
    url(r'^storage/product_storage/$', storage_views.product_storage),
    url(r'^storage/half_storage/$', storage_views.half_storage),
    url(r'^storage/all_storage/$', storage_views.all_storage),
    url(r'^storage/alter_storage/$', storage_views.alter_storage),
    url(r'^storage/product_storage_in/$', storage_views.product_storage_in),
    url(r'^storage/storage_in_add/$', storage_views.storage_in_add),
    url(r'^storage/storage_in_upload/$', storage_views.storage_in_upload),
    url(r'^storage/storage_in_clear/$', storage_views.storage_in_clear),
    url(r'^storage/storage_in_detail_modify/$', storage_views.storage_in_detail_modify),
    url(r'^storage/storage_in_detail_del/$', storage_views.storage_in_detail_del),
    url(r'^storage/storage_in_confirm/$', storage_views.storage_in_confirm),
    url(r'^storage/storage_in_submit/$', storage_views.storage_in_submit),
    url(r'^storage/storage_outing/$', storage_views.storage_outing),
    url(r'^storage/product_storage_out/$', storage_views.product_storage_out),
    url(r'^storage/product_storage_out_edit/$', storage_views.product_storage_out_edit),
    url(r'^storage/product_storage_out_del/$', storage_views.product_storage_out_del),
    url(r'^storage/product_storage_out_submit/$', storage_views.product_storage_out_submit),
    url(r'^storage/product_storage_out_reset/$', storage_views.storege_out_reset),
    url(r'^storage/storage_out_commit/$', storage_views.storage_out_commit),
    url(r'^storage/storage_out_list_output/$', storage_views.storage_out_list_output),
    url(r'^storage/storage_output_download/$', storage_views.storage_output_download),
    url(r'^storage/half_storage_in/$', storage_views.half_storage_in),
    url(r'^storage/half_storage_in_add/$', storage_views.half_storage_in_add),
    url(r'^storage/half_storage_in_upload/$', storage_views.half_storage_in_upload),
    url(r'^storage/half_storage_in_clear/$', storage_views.half_storage_in_clear),
    url(r'^storage/half_storage_in_detail_modify/$', storage_views.half_storage_in_detail_modify),
    url(r'^storage/half_storage_in_detail_del/$', storage_views.half_storage_in_detail_del),
    url(r'^storage/half_storage_in_confirm/$', storage_views.half_storage_in_confirm),
    url(r'^storage/half_storage_in_submit/$', storage_views.half_storage_in_submit),

    url(r'^info/$', information_views.infomation_manage),
    url(r'^info/finish_product_infomation/$', information_views.finish_product_information),
    url(r'^info/half_product_infomation/$', information_views.half_product_information),
    url(r'^info/add_product/$', information_views.add_product),
    url(r'^info/edit_product/$', information_views.edit_product),
    url(r'^info/delete_product/$', information_views.delete_product),
    url(r'^info/upload_storage_info/$', information_views.upload_storage_info),
    url(r'^info/customer_info/$', information_views.customer_info),
    url(r'^info/add_customer_info/$', information_views.add_customer_info),
    url(r'^info/edit_customer_info/$', information_views.edit_customer_info),
    url(r'^info/delete_customer_info/$', information_views.delete_customer_info),
    url(r'^info/upload_customer_info/$', information_views.upload_customer_info),
    url(r'^info/show_user_info/$', information_views.show_user_info),
    url(r'^info/add_user_info/$', information_views.add_user_info),
    url(r'^info/del_user_info/$', information_views.del_user_info),
    url(r'^info/change_user_info/$', information_views.change_user_info),
    url(r'^info/get_user_info/$', information_views.get_user_info),


    url(r'^report/$', report_views.report_manage),
    url(r'^report/statement/$', report_views.statement),
    url(r'^report/statement_select_location/$', report_views.statement_select_location),
    url(r'^report/statement_detail/$', report_views.statement_detail),
    url(r'^report/edit_report_detail/$', report_views.edit_report_detail),
    url(r'^report/edit_report_detail_modify/$', report_views.edit_report_detail_modify),
    url(r'^report/edit_report_detail_delete/$', report_views.edit_report_detail_delete),
    url(r'^report/edit_report_detail_submit/$', report_views.edit_report_detail_submit),
    url(r'^report/report_list_order/$', report_views.report_list_order),
    url(r'^report/report_storage_out_detail/$', report_views.report_storage_out_detail),
    url(r'^report/report_change_income/$', report_views.report_change_income),
    url(r'^report/report_refund_detail/', report_views.report_refund_detail),
    url(r'^report/report_translation_expense_edit/$', report_views.translation_expense_edit),
    url(r'^report/report_translation_comment_edit/$', report_views.translation_comment_edit),
    url(r'^report/report_statement_output/$', report_views.statement_output),
    url(r'^report/report_storage_in_product/$', report_views.storage_in_product),
    url(r'^report/report_storage_in_product_detail/$', report_views.storage_in_product_detail),
    url(r'^report/report_storage_in_half_detail/$', report_views.storage_in_half_detail),
    url(r'^report/report_storage_in_half/$', report_views.storage_in_half),
    url(r'^report/report_storage_in_recover/$', report_views.storage_in_recover),
    url(r'^report/report_storage_in_edit/$', report_views.storage_in_edit),
    url(r'^report/report_storage_in_confirm/$', report_views.storage_in_confirm),
    url(r'^report/report_storage_in_submit/$', report_views.storage_in_submit),
    url(r'^report/change_handler/$', report_views.change_handler),
    url(r'^report/product_statistics/$', report_views.product_statistics),

    # url(r'^input_pro/$', storage_views.input_pro),
    # url(r'^input_half/$', storage_views.input_half),
    # url(r'^input_cust/$', customer_views.input_cust),

    url(r'^system/$', system_views.system_manage),
    url(r'^system/clear_temp_xlsx/$', system_views.clear_temp_xlsx),
    url(r'^system/excel_to_excel/$', system_views.excel_to_excel),
    url(r'^system/translate_file_down/$', system_views.translation_file_down),
    url(r'^system/power_off/$', system_views.power_off),
    url(r'^system/show_original_balance/$', system_views.show_original_balance),
    url(r'^system/change_original_balance/$', system_views.change_original_balance),


    url(r'^salary/$', salary_views.index),
]
