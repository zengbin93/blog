# -*- coding: utf-8 -*-
"""
处理高斯计算结果
输入：.out或者.log文件
输出：.csv文件
columns=['文件名','计算方法','电荷','多重度','E','E0','E+E0','给出的E+E0']

"""
import pandas as pd
import os
from tkinter.filedialog import askdirectory
path = askdirectory()
os.chdir(path)
#os.getcwd()   #取得当前工作目录

#判断out文件是否为正常结束的计算结果
def error_in(out_file):
    for line in open(out_file,'r'):
        if 'Error termination' in line:
            er = 'Error termination'
        elif 'Normal termination' in line:
            er = 'Normal termination'
    return er
    
#提取opt信息
def opt_col(out_file):
    opt = ''
    for line in open(out_file,'r'):
        if '# opt=' in line:
            opt=line.strip()
            break
    return opt

#提取Charge信息
def charge_col(out_file):
    charge=''
    for line in open(out_file,'r'):
        if 'Charge = ' in line:
            charge = line.split('Charge = ')[1].strip().split('Multiplicity =')[0].strip()
            break
    return charge
    
#提取Multiplicity信息
def m_col(out_file):
    m = ''
    for line in open(out_file,'r'):
        if 'Multiplicity =' in line:
            m=line.split('Multiplicity =')[1].strip()
            break
    return m
    
#提取HF信息
def hf_col(out_file):
    hf=0.0000
    line_all=''
    for line in open(out_file,'r'):
        line_all = line_all + line.strip()
    hf=float(line_all.split('HF=')[1].split('S2=')[0].strip('|\\'))
    return hf
    
#提取Zero-point correction信息
def zero_point_col(out_file):
    zero_point=0.0000
    for line in open(out_file,'r'):
        if 'Zero-point correction=' in line:
            zero_point=float(line.strip().split('correction=')[1].strip().split(' ')[0])
            break
    return zero_point

#提取opt信息  failed
def sum_e_zp_col(out_file):
    sum_e_zp = 0.0000
    for line in open(out_file,'r'):
        if 'Sum of electronic and zero-point Energies=' in line:
            sum_e_zp = float(line.split('electronic and zero-point Energies=')[1].strip())
            break
    return sum_e_zp

#获取工作目录下的所有文件名
data_col = []
for root, dirs, files in os.walk(path):
    for out_file in files:
        if '.out' in out_file:
            er = error_in(out_file)
            if er == 'Normal termination':
                data_col.append([out_file.replace('.out',''),opt_col(out_file),
                charge_col(out_file),m_col(out_file),hf_col(out_file),
                zero_point_col(out_file),
                hf_col(out_file)+zero_point_col(out_file),
                sum_e_zp_col(out_file)])
        if '.log' in out_file:
            er = error_in(out_file)
            if er == 'Normal termination':
                data_col.append([out_file.replace('.log',''),opt_col(out_file),
                charge_col(out_file),m_col(out_file),hf_col(out_file),
                zero_point_col(out_file),
                hf_col(out_file)+zero_point_col(out_file),
                sum_e_zp_col(out_file)])                         
#print(data_col)                    
data_col = pd.DataFrame(data=data_col,
                        columns=['文件名','计算方法','电荷','多重度','E','E0','E+E0','给出的E+E0'])
data_col.to_csv('1_result.csv',header=True)

