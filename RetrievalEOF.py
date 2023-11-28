from selenium import webdriver
import json
import requests
import re, os, datetime
import pandas as pd
from datetime import datetime
import xlwt

'''
已存在数据保存为表格
'''


def save_as_csv(array, path):
    data = pd.DataFrame(array)
    data.to_csv(path, mode='w', header=False, index=None)


'''
遍历文件夹, 返回文件
'''


def get_filelist(self):
    """
    :param :dir
    :return:file_list
    """
    file_list = []
    for home, dirs, files in os.walk(self):
        for filename in files:
            # 文件名列表，包含完整路径
            file_list.append(os.path.join(home, filename).replace('\\', '/'))
            # # 文件名列表，只包含文件名
            # Filelist.append( filename)
    return file_list


# 生成日期xlsx表【文件后缀为EOF且大小大于4000k】
def RetrievalTable(EOF_dir):

    date_xlsx = EOF_dir + '/retrievaltable.xls'

    filelist = get_filelist(EOF_dir)
    datelist = []

    for i in filelist:
        if os.path.splitext(i)[-1] == '.EOF' and os.path.getsize(i)/1024 > 4000:
            filename = os.path.basename(i)
            date = filename[25:29] + '.' + filename[29:31] + '.' + filename[31:33]
            print(date)
            datelist.append(date)

    tuple(datelist)

    workbook = xlwt.Workbook(encoding='utf-8')
    booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
    for i, row in enumerate(datelist):
        booksheet.write(i, 0, row)
    workbook.save(date_xlsx)

    print("生成日期列表！\n")


if __name__ == "__main__":
    EOF_dir = 'OPOD_dir'
    RetrievalTable(EOF_dir)
