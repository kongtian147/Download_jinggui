from selenium import webdriver
import json
import requests
import re, os, datetime
import pandas as pd
from datetime import datetime
import xlwt

'''
数据保存为表格
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


# 生成日期xlsx表
def GenerateTable(path, output_path):
    EOF_dir = output_path + '/OPOD_dir'
    date_xlsx = EOF_dir + '/datetable.xls'

    if not os.path.exists(EOF_dir):
        os.makedirs(EOF_dir)
    else:
        os.remove(EOF_dir)
        os.makedirs(EOF_dir)

    filelist = get_filelist(path)
    datelist = []

    for i in filelist:
        filename = os.path.basename(i)
        date = filename[17:21] + '.' + filename[21:23] + '.' + filename[23:25]
        datelist.append(date)

    tuple(datelist)

    workbook = xlwt.Workbook(encoding='utf-8')
    booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
    for i, row in enumerate(datelist):
        booksheet.write(i, 0, row)
    workbook.save(date_xlsx)

    print("生成日期列表！\n")


if __name__ == "__main__":
    path = r'F:\test\offset\zip_dir'  # 输入 zip_dir文件夹路径
    output_path = r'F:\test\offset'  # 输出 EOF_dir文件夹存放目录
    GenerateTable(path, output_path)
