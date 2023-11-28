import os
import shutil
import pandas as pd
from tqdm import tqdm
from warnings import simplefilter

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
    shutil.move(targetExcel, temp_dir)
    shutil.move(basisExcel, temp_dir)
    # 上一行中自定义文件名！


if __name__ == "__main__":
    # 引号内填写需要去重的表格路径

    targetExcel = r'OPOD_dir/datetable.xls'

    # 引号内填写依据表格的路径

    basisExcel = r'OPOD_dir/retrievaltable.xls'

    # 引号内填写输出字段

    field = ''

    # 结果文件输出路径

    outputpath = './OPOD_dir'

    removeRepeat(targetExcel, basisExcel, field, outputpath)
