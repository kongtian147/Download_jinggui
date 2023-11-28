import datetime
import os
import re
import tkinter as tk
import urllib.request
from urllib.parse import urlparse

import pandas as pd
import requests
import xlrd  # 注意 xlrd1.2.0版本支持对旧版excel格式的读取，默认pip为新版2.0.1
import xlwt
from bs4 import BeautifulSoup
from dateutil.parser import parse
import shutil
from warnings import simplefilter
from tqdm import tqdm

""" Notice
本代码爬取轨道数据来自于网站：https://s1qc.asf.alaska.edu/aux_poeorb/
代码需要更改地方有：
1.存放轨道数据文件夹位置
2.在上步文件夹下新建cookie.txt，存取网址的cookie信息:
    1)F12
    2)网络
    3)ctrl+r 获取cookied
注意：download下的headers数组里存放的实际上轨道数据的网站信息，这个根据电脑版本(win10,win11)或平台(window,OS)要进行小调
"""
timestart = datetime.datetime.now()


def download(dest_dir, url, cookie_path):
    print(url)
    print(dest_dir)
    cookie = str(open(cookie_path, "r").read())
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Host": "s1qc.asf.alaska.edu",
        "Referer": "https://s1qc.asf.alaska.edu/aux_poeorb/?sentinel1__mission=S1A&validity_start=2015-02-19",
        "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\", \"Google Chrome\";v=\"96\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows \"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54",
    }
    try:
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        f = open(dest_dir, "w")
        lines = response.readlines()
        for line in lines:
            f.write(line.decode())
        f.close()
    except:
        error_url.append(url)
        print("\tError retrieving the URL:", url)
    else:  # 没有异常
        if url in error_url:  # 在错误列表里
            error_url.remove(url)


def read_excel(dir_path):
    try:
        NeedTimeArray = []
        dir_list = os.listdir(dir_path)  # dir_path ：文件夹路径
        for dir in dir_list:  # 搜寻文件夹
            # 搜寻excel文件并读取存储到NeedTimeArray
            if os.path.splitext(dir)[1] == ".xlsx" or os.path.splitext(dir)[1] == ".xls" or os.path.splitext(dir)[
                1] == ".xlsm":  # 后缀为excel表格格式
                excel_path = os.path.join(dir_path, dir)
                work_book = xlrd.open_workbook(excel_path)  # 注意
                sheets = work_book.sheets()[0]  # 选定表
                nrows = sheets.nrows  # 获取行号
                ncols = sheets.ncols  # 获取列号
                for i in range(0, nrows):  # 第0行为表头,第一行为数据就改为0
                    data = sheets.row_values(i)  # 循环输出excel表中每一行，即所有数据
                    for j in range(len(data)):  # 将excel格式(如2015.06.22,2015-06-22)变成需要的8数字格式
                        data[j] = re.sub('[-,., ]', '', data[j])
                        NeedTimeArray.append(data)
        return NeedTimeArray
    except BaseException as e:  # 抛出异常的处理
        print(str(e))


'''
数据保存为表格
'''


def save_as_csv(array, path):
    data = pd.DataFrame(array)
    data.to_csv(path, mode='w', header=False, index=None)


# 遍历文件夹, 返回文件

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

def GenerateTable(path, EOF_dir):
    EOF_dir = EOF_dir
    date_xlsx = EOF_dir + '/datetable.xls'

    if not os.path.exists(EOF_dir):
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


'''
已存在精轨数据保存为表格
'''


# 生成日期xlsx表【文件后缀为EOF且大小大于4000k】
def RetrievalTable(EOF_dir):
    date_xlsx = EOF_dir + '/retrievaltable.xls'

    filelist = get_filelist(EOF_dir)
    datelist = []

    for i in filelist:
        if os.path.splitext(i)[-1] == '.EOF' and os.path.getsize(i) / 1024 > 4000:
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


'''
比较zip日期和已存在精轨日期，生成结果xls
'''
simplefilter(action='ignore', category=FutureWarning)


def removeRepeat(targetExcel, basisExcel, field, outputpath):
    resultExcelpath = outputpath + '/resultExcel.xls'
    count = 0
    ind = 1
    targetIndex = field + str(ind)
    resultExcel = {
        field + '1': []
    }
    header = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']

    print('读取数据')
    target_Excel = pd.read_excel(targetExcel, header=None, names=header, dtype='object')
    basis_Excel = pd.read_excel(basisExcel, header=None, names=['A'], dtype='object')
    print('读取成功')

    for index in tqdm(header):
        for i in tqdm(target_Excel[index], leave=False):
            if pd.isnull(i):
                continue
            elif i in list(basis_Excel['A']):
                continue
            else:
                resultExcel[targetIndex].append(i)
                count += 1
                if count >= 1020000:
                    count = 0
                    ind += 1
                    targetIndex = field + str(ind)
                    resultExcel[targetIndex] = []

    print('等待数据合并')
    df = pd.concat([pd.DataFrame(i) for i in resultExcel.values()], axis=1)
    df.fillna(0)  # 取消长短不一致问题
    df.to_excel(resultExcelpath, header=None, index=False)  # 取消表头与行号

    temp_dir = os.path.dirname(targetExcel) + '/tmp'
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    if os.path.exists(targetExcel):
        shutil.copy2(targetExcel, temp_dir + '/datetable.xls')
        os.remove(targetExcel)
    if os.path.exists(basisExcel):
        shutil.copy2(basisExcel, temp_dir + '/retrievaltable.xls')
        os.remove(basisExcel)

    # 上一行中自定义文件名！


# 生成日期xls数据list【文件后缀为EOF且大小大于4000k】

def RetrievalEOF(EOF_dir):
    filelist = get_filelist(EOF_dir)
    datelist = []

    for i in filelist:
        if os.path.splitext(i)[-1] == '.EOF' and os.path.getsize(i) / 1024 > 4000:
            filename = os.path.basename(i)
            datelist.append(filename)

    return datelist


# 转换SLC_tab为xls文件
def TabfiletoDataxls(file_path, EOF_dir):

    date_xlsx = EOF_dir + '/datetable.xls'
    datelist = []
    with open(file_path, 'r') as file:
        # 逐行读取文件内容
        for line in file:
            # 对每一行进行格式化处理
            formatted_line = line.strip()  # 移除行尾的换行符等
            # 获取每行倒数第8到第16个字符
            date = formatted_line[-16:-12] + '.' + formatted_line[-12:-10] + '.' + formatted_line[-10:-8]
            datelist.append(date)
            # print(date)  # 或者将格式化后的内容存储到其他地方

    tuple(datelist)

    # 保存tuple类型的datelist为.xls文件
    workbook = xlwt.Workbook(encoding='utf-8')
    booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
    for i, row in enumerate(datelist):
        booksheet.write(i, 0, row)
    workbook.save(date_xlsx)


if __name__ == '__main__':
    # 创建调用文件夹所需对象
    root = tk.Tk()
    root.withdraw()
    error_url = []  # 存放下载出错的文件名

    ''' 输入zip文件夹路径（其中尽可能只包含zip文件）|| 输出路径存放日期table、EOF文件（输出路径可以不存在） '''

    SLC_tab = r'SLC_tab'  # 加载压缩包路径
    EOF_dir = r'OPOD_dir'  # 加载精轨数据路径

    ''' 输入zip文件夹路径（其中尽可能只包含zip文件）|| 输出路径存放日期table、EOF文件（输出路径可以不存在） '''

    EOF_list = RetrievalEOF(EOF_dir)
    # print(EOF_list)

    E0F_history_dir = EOF_dir + '/history'
    if os.path.isdir(E0F_history_dir):
        Existing_EOF_file = get_filelist(E0F_history_dir)
    else:
        Existing_EOF_file = []

    TabfiletoDataxls(SLC_tab, EOF_dir)  # 生成SLC_tab文件日期表格

    cookie_path = r"D:\python_code\Download_jinggui\cookie.txt"  # cookie文件位置
    out_path = EOF_dir  # 存放datetable及轨道文件输出位置

    url_param_json = {}
    url_param_json['sentinel1__mission'] = 'S1A'

    date = '2015-01-01'  # 开始搜寻日期
    url_param_json['validity_start'] = date

    # 获得EOF下载网址
    url_param = urllib.parse.urlencode(url_param_json)  # url参数
    url = 'https://s1qc.asf.alaska.edu/aux_poeorb/?%s' % url_param  # 拼接
    html = requests.get(url).content
    dom = BeautifulSoup(html, "lxml")  # 解析html文档
    a_list = dom.findAll("a")  # 找出<a>
    eof_lists = [a['href'] for a in a_list if a['href'].endswith('.EOF')]  # 找出EOF
    TimeArray = []  # 存放网站爬取EOF文件的时间信息
    NeedTimeArray = read_excel(out_path)  # 存放下载数据的时间信息
    for eof in eof_lists:

        # 截取轨道文件的时间信息
        if os.path.splitext(eof)[1] == ".EOF" and os.path.basename(eof)[0:3] == 'S1A':  # 后缀是eof且前缀前三个字符为S1A
            SplitEOF = re.split(r'[_,.,\s ]\s*', eof)  # 将EOF文件分割

            SplitTime = SplitEOF[-2]  # 分割列表中取表中最后一个日期
            Time = parse(SplitTime)  # 转换成时间格式
            NeedTime = Time + datetime.timedelta(days=-1)  # 转换成所需时间
            NeedTimeNum = (re.sub('[-,:, ]', '', str(NeedTime)))[0:8]  # 将时间格式转换成需要的数字格式,sub为去除字符串中符号
            if NeedTimeNum in str(NeedTimeArray):
                TimeArray.append(NeedTimeNum)  # 存放准备下载的时间
                savefile = os.path.join(out_path, eof)
                if eof not in EOF_list:
                    print('来源：https://s1qc.asf.alaska.edu/aux_poeorb/')
                    print(eof)
                    download(savefile, 'https://s1qc.asf.alaska.edu/aux_poeorb/' + eof, cookie_path)
                    print("------------------------------------")
                    print("精密轨道数据下载完成")
                    print("------------------------------------")
                    if len(TimeArray) == len(NeedTimeArray):
                        print("所需精密轨道数据下载完成,共计%d个文件" % (len(TimeArray)))
                        print("------------------------------------")
                        break
                else:
                    print('来源：history')
                    print(eof)
                    search_value = eof
                    found_element = next((element for element in Existing_EOF_file if search_value in element), None)
                    shutil.copy(found_element, EOF_dir)
                    print("------------------------------------")
                    print("精密轨道数据复制完成")
            else:
                continue

    # 下载出错的数据重新下载
    while len(error_url) != 0:
        print("开始下载出错的数据")
        print("------------------------------------")
        print("出错的数据有")
        print(error_url)
        for eof in error_url:
            savefile = os.path.join(out_path, eof[39:])
            download(savefile, eof, cookie_path)

    timeend = datetime.datetime.now()
    print('Running time: %s Seconds' % (timeend - timestart))
