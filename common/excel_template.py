import datetime


def date_now():
    return datetime.datetime.now().strftime('%m月%d日')


def statement_head(ws, cust_info, pur_comment=''):
    ws.merge_cells('C2:D2')
    ws.merge_cells('F2:G2')
    cust_title = cust_info.cust_location + cust_info.cust_name + pur_comment
    data_list = [['', '', '', cust_title, '发货单（）', '', date_now(), '单请A'],
                 ['编号', '数量', '标准零售价', '', '金额', '备注', '', '']]

    return ws
