# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 10:39:09 2016

@author: Mike
"""

import pandas as pd,re

def get_MOC(file,key1,key2):
    # 读入out文件
    f = open(file,'r')
    buff = f.read()
    # 利用re查找文件中的所有分子轨道系数，最后一部分为目标数据
    key_1 = key1
    print('key1',key_1)
    key_2 = key2
    print('key2',key_2)
    pat = re.compile(key_1+'(.*?)'+key_2,re.S)
    res = re.findall(pat,buff)
    res = res[-1]    # res表示目标数据
    
    # 计算目标数据中含有Eigenvalues的个数(数据块的数量)
    pat_1 = re.compile('Eigenvalues')
    res_1 = re.findall(pat_1,res)
    print(res_1)
    part_len = len(res_1)
    print('目标数据中含有Eigenvalues的个数:',part_len)
    
    # 去除目标数据中的首尾多余字符，按分行符拆分
    res = res.strip('\n').split('\n')
    res_len = len(res)-1
    print('res数据的行数：',res_len)
    
    # 计算每个数据块的长度
    part = int(res_len/part_len)
    print('每个数据块的长度：',part)
    
    # 按数据块长度、数量进行循环，合并数据
    res_reshape = []
    for i in range(0,part):
        row_col = res[i]
        for j in range(1,part_len):
            row_col = row_col + '  ' + res[j*part+i][20:72]
        res_reshape.append(row_col)
    print("结果数据长度：",len(res_reshape))
    # 清理空轨道数据,按列整理成dataframe数据格式
    V_pos = res_reshape[1].find('V')
    res_O = []
    for line in res_reshape:
        #line = line[0:V_pos-10]
        a1 = line[0:20]
        a2 = line[20:V_pos-8].strip(' ')
        a2 = re.split('\s+',a2)
        a2 = '|'.join(a2)
        a3 = a1+'|'+a2
        a3 = a3.split('|')
        res_O.append(a3)
    return res_O

file = "Ni2CO4-_31_A1_2th_4_C2v_big_chk_full.out"
Alpha_key1 = "Alpha Molecular Orbital Coefficients"
Beta_key1 = "Beta Molecular Orbital Coefficients"
key2 = "Alpha Density Matrix:"
res_O = get_MOC(file,Alpha_key1,key2)
res_O = pd.DataFrame(res_O)

csv_name = file.replace('.out','') + Alpha_key1+'.csv'
res_O.to_csv(csv_name)



    