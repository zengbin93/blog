# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 09:16:38 2016
处理高斯计算结果
输入：.out或者.log文件
输出：.gjf文件
整理out输出结果作为新的gjf输入
Version: 1.2
@author: 曾斌
"""
import pandas as pd
import os
import re
from tkinter.filedialog import askdirectory

#判断out文件是否为正常结束的计算结果
def is_Nt(out_file):
    with open(out_file,'r') as f:
        for line in f:
            if 'Error termination' in line:
                Nt = False  #非正常结束，is_Nt为False
            elif 'Normal termination' in line:
                Nt = True   #正常结束，is_Nt为True
            else:
                Nt = ""
    return Nt

#获取元素符号
def get_symbolic(out_file):
    #关键字1,2(引号间的内容可以修改)
    w1 = 'Symbolic Z-matrix:\n'
    w2 = 'GradGradGradGradGradGradGrad'
    f = open(out_file,'r')
    buff = f.read()  #将整个文本文件读入
    pat = re.compile(w1+'(.*?)'+w2,re.S)
    part_f = pat.findall(buff)
    symbolic_c=[]  #list 存储元素符号
    part_f = str(part_f[0]).strip().split("\n")
    for i in range(1,len(part_f)):
        symbolic_c.append(part_f[i].strip().split(" ")[0].strip())
    #symbolic_c = pd.DataFrame(symbolic_c)
    return symbolic_c
#获取优化后的xyz坐标
def get_xyz(out_file):
    w1 = "Standard orientation:"
    w2 = "Rotational constants"
    f = open(out_file,"r")
    buff = f.read()
    pat = re.compile(w1+'(.*?)'+w2,re.S)
    results = pat.findall(buff)
    i = len(results)-1 #记录最后一次优化结果
    last_one = str(results[i])
    last_one = last_one.strip().split("\n")
    xyz=[]
    for line in range(4,len(last_one)-1):
        xyz.append(re.split('\s+',str(last_one[line]).strip()))
    xyz = pd.DataFrame(xyz)
    xyz_ = []
    for i in range(0,len(xyz)):
        a_ = xyz.iloc[i,3]
        b_ = xyz.iloc[i,4]
        c_ = xyz.iloc[i,5]
        xyz_.append((a_,b_,c_))
    xyz = xyz_
    return xyz
#将元素符号与xyz坐标合并
def bind_s_xyz(out_file):
    s = get_symbolic(out_file)
    xyz = get_xyz(out_file)
    s_xyz = []
    for i in range(0,len(s)):
        s_xyz.append(str(str(s[i])+" "+str(xyz[i]).strip("()")\
        .replace("\'",'').replace(",","")).replace(" ","    "))
    return s_xyz
   
#获取第8行（电荷+多重度）
def get_ch_mul(out_file):
    with open(out_file,"r") as f:
        for line in f:
            if "Charge =" in line:
                ch_mul=line
                break
    ch = ch_mul.strip().split("Charge =")[1].split("Multiplicity =")[0].strip()
    mul =ch_mul.strip().split("Multiplicity =")[1].strip()
    line8 = str(ch)+" "+str(mul)+"\n"
    return line8

def out_to_gjf(out_file):
    line1 = "%chk="+out_file.replace(".out","_int.chk")+"\n"
    line2 = "%nprocshared=1\n"
    line3 = "%mem=2000MB\n"
    line4 = "# opt=(cartesian,tight) freq ub3lyp/6-311+g(d) int=ultrafine symm=(loose,on) scf=(maxcyc=80,xqc) iop(1/8=10)\n"
    line5 = "\n"
    line6 = "Title Card Required\n"
    line7 = "\n"
    line8 = get_ch_mul(out_file)
    s_xyz = bind_s_xyz(out_file)
    end = "\n\n\n"
    gjf_name = str(out_file.replace(".out","_int.gjf"))
    f = open(gjf_name,"w")
    f.write(str(line1))
    f.write(str(line2))
    f.write(str(line3))
    f.write(str(line4))
    f.write(str(line5))
    f.write(str(line6))
    f.write(str(line7))
    f.write(str(line8))
    for i in range(0,len(s_xyz)):
        s_xyz_w = str(s_xyz[i])+"\n"
        f.write(s_xyz_w)
    f.write(str(end))
    f.close()


def log_to_gjf(out_file):
    line1 = "%chk="+out_file.replace(".log","_int.chk")+"\n"
    #line1 = get_log_line1(log_file)
    line2 = "%nprocshared=2\n"
    line3 = "%mem=2000MB\n"
    line4 = "# opt=(cartesian,tight) freq ub3lyp/6-311+g(d) int=ultrafine symm=(loose,on) scf=(maxcyc=80,xqc) iop(1/8=10)\n"
    line5 = "\n"
    line6 = "Title Card Required\n"
    line7 = "\n"
    line8 = get_ch_mul(out_file)
    s_xyz = bind_s_xyz(out_file)
    end = "\n\n\n"
    gjf_name = str(out_file.replace(".log","_int.gjf"))
    f = open(gjf_name,"w")
    f.write(str(line1))
    f.write(str(line2))
    f.write(str(line3))
    f.write(str(line4))
    f.write(str(line5))
    f.write(str(line6))
    f.write(str(line7))
    f.write(str(line8))
    for i in range(0,len(s_xyz)):
        s_xyz_w = str(s_xyz[i])+"\n"
        f.write(s_xyz_w)
    f.write(str(end))
    f.close()


def out_2_gjf():
    path = askdirectory()
    os.chdir(path)
    #获取工作目录下的所有文件名
    for root, dirs, files in os.walk(path):
        for out_file in files:
            #.out文件处理
            if '.out' in out_file:
                Nt = is_Nt(out_file)
                if Nt == True:
                    try:
                        out_to_gjf(out_file)
                    except:
                        print(out_file+"处理失败")
            #.log文件处理
            if '.log' in out_file:
                Nt = is_Nt(out_file)
                if Nt == True:
                    try:
                        log_to_gjf(out_file)
                    except:
                        print(out_file+"处理失败")

out_2_gjf()
               