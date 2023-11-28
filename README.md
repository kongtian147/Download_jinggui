# Download_jinggui——哨兵1号精轨数据下载

## 介绍

本代码爬取轨道数据来自于网站：https://s1qc.asf.alaska.edu/aux_poeorb/
代码需要更改地方有：
1.存放轨道数据文件夹位置
2.在上步文件夹下新建cookie.txt，存取网址的cookie信息:
    1)F12
    2)网络
    3)ctrl+r 获取cookied
注意：download下的headers数组里存放的实际上轨道数据的网站信息，这个根据电脑版本(win10,win11)或平台(window,OS)要进行小调

## 环境

```
urllib3==1.26.13
pandas==2.0.0
requests==2.28.1
xlwt==1.3.0
python-dateutil==2.8.2
```

## 文件夹结构
文件

DownloadByTabfile.py——根据SLC_tab下载所需精轨数据

main.py——根据ZIP_dir下载所需精轨数据

cookie.txt——精轨网站cookie



文件夹

OPOD_dir						下载精轨文件存放路径	

|---->history					 历史精轨数据

