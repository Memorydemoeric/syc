import os

import datetime

from syc import settings


def create_base_directory(base_path):
    year = str(datetime.datetime.now().year)
    month = str(datetime.datetime.now().month)
    year_month = year + '.' + month
    path = os.path.join(base_path, year_month)
    if not os.path.exists(path):
        print('不存在的文件')
        os.makedirs(path)
    else:
        print('文件已存在')
    return path

def upload_purchase_file(cust_name, file):
    base_path = settings.PURCHASE_BAK
    year = str(datetime.datetime.now().year)
    month = str(datetime.datetime.now().month)
    day = str(datetime.datetime.now().day)
    year_month = year + '.' + month
    path = os.path.join(base_path, year_month)
    if not os.path.exists(path):
        print('不存在的文件')
        os.makedirs(path)
    else:
        print('文件已存在')
    file_name = month + '.' + day + '_' + cust_name + '.xls'
    with open(os.path.join(path, file_name), 'wb') as wf:
        for foo in file.chunks():
            wf.write(foo)
            wf.flush()
    return os.path.join(path, file_name)


def upload_storage_file(file):
    base_path = settings.STORAGE_BAK
    year = str(datetime.datetime.now().year)
    month = str(datetime.datetime.now().month)
    day = str(datetime.datetime.now().day)
    year_month = year + '.' + month
    path = os.path.join(base_path, year_month)
    if not os.path.exists(path):
        print('不存在的文件')
        os.makedirs(path)
    else:
        print('文件已存在')
    file_name = month + '.' + day + '_storage.xls'
    with open(os.path.join(path, file_name), 'wb') as wf:
        for foo in file.chunks():
            wf.write(foo)
            wf.flush()
    return os.path.join(path, file_name)


def upload_customer_file(file):
    base_path = settings.CUSTOMER_BAK
    year = str(datetime.datetime.now().year)
    month = str(datetime.datetime.now().month)
    day = str(datetime.datetime.now().day)
    year_month = year + '.' + month
    path = os.path.join(base_path, year_month)
    if not os.path.exists(path):
        print('不存在的文件')
        os.makedirs(path)
    else:
        print('文件已存在')
    file_name = month + '.' + day + '_customer.xlsx'
    with open(os.path.join(path, file_name), 'wb') as wf:
        for foo in file.chunks():
            wf.write(foo)
            wf.flush()
    return os.path.join(path, file_name)


def upload_translation(file, file_name):
    base_path = settings.PURCHASE_TRANSLATION_ORIGIN
    for i in os.listdir(base_path):
        os.remove(os.path.join(base_path, i))
    file_path = os.path.join(base_path, file_name + '.xlsx')
    with open(file_path, 'wb') as wf:
        for foo in file.chunks():
            wf.write(foo)
            wf.flush()
    return file_path


def upload_storage_in_info(file, in_type):
    month = str(datetime.datetime.now().month)
    day = str(datetime.datetime.now().day)
    month_day = month + '_' + day
    base_path = settings.STORAGE_IN
    path = create_base_directory(base_path)
    file_path = os.path.join(path, month_day + '.xls')
    with open(file_path, 'wb') as wf:
        for foo in file.chunks():
            wf.write(foo)
            wf.flush()
    return file_path


def create_purchase_output_directory():
    base_path = settings.PURCHASE_OUTPUT
    year = str(datetime.datetime.now().year)
    month = str(datetime.datetime.now().month)
    year_month = year + '.' + month
    path = os.path.join(base_path, year_month)
    if not os.path.exists(path):
        print('不存在的文件')
        os.makedirs(path)
    else:
        print('文件已存在')
    return path


def purchase_output_path(file_name):
    year = str(datetime.datetime.now().year)
    month = str(datetime.datetime.now().month)
    day = str(datetime.datetime.now().day)
    year_month = year + '.' + month
    base_path = settings.PURCHASE_OUTPUT
    out_file_name = month + '.' + day + '_' + file_name
    file_path = os.path.join(os.path.join(base_path, year_month), out_file_name + '.xlsx')
    return file_path, out_file_name


def create_statement_finish_directory():
    base_path = settings.FINISHSTATEMENTOUT
    year = str(datetime.datetime.now().year)
    month = str(datetime.datetime.now().month)
    year_month = year + '.' + month
    path = os.path.join(base_path, year_month)
    if not os.path.exists(path):
        print('不存在的文件')
        os.makedirs(path)
    else:
        print('文件已存在')
    return path


def create_statement_purchase_directory():
    base_path = settings.PURCHASESTATEMENTOUT
    year = str(datetime.datetime.now().year)
    month = str(datetime.datetime.now().month)
    year_month = year + '.' + month
    path = os.path.join(base_path, year_month)
    if not os.path.exists(path):
        print('不存在的文件')
        os.makedirs(path)
    else:
        print('文件已存在')
    return path