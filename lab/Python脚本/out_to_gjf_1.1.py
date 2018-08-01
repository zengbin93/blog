# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 09:16:38 2016
处理高斯计算结果
输入：.out或者.log文件
输出：.gjf文件
整理out输出结果作为新的gjf输入
version: 1.1
@author: 曾斌
"""
import os
import re
from tkinter.filedialog import askdirectory
path = askdirectory()
os.chdir(path)

#判断out文件是否为正常结束的计算结果
def is_Nt(out_file):
    with open(out_file,'r') as f:
        for line in f:
            if 'Error termination' in line:
                Nt = False  #非正常结束，is_Nt为False
            elif 'Normal termination' in line:
                Nt = True   #正常结束，is_Nt为True
    return Nt

#获取元素符号&优化后的xyz坐标
def get_symbo_xyz(out_file):
    w1 = " Cartesian coordinates read from the checkpoint file:\n"
    w2 = " Recover connectivity data from disk."
    f = open(out_file,"r")
    buff = f.read()
    pat = re.compile(w1+'(.*?)'+w2,re.S)
    results = pat.findall(buff)
    symbo_xyz = str(results[0]).strip().split('\n')
    return symbo_xyz[2:len(symbo_xyz)]

#获取第1行
def get_line1(out_file):
    line1 = "%chk="+out_file.replace(".out","_int.chk")+"\n"
    return line1
    
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

def save_gjf(out_file):
    line1 = get_line1(out_file)
    line2 = "%nprocshared=1\n"
    line3 = "%mem=1000MB\n"
    line4 = "# opt=(cartesian,tight) freq ub3lyp/6-311+g(d) int=ultrafine symm=(loose,on) scf=(maxcyc=80,xqc) iop(1/8=10)\n"
    line5 = "\n"
    line6 = "Title Card Required\n"
    line7 = "\n\n\n"
    line8 = get_ch_mul(out_file)
    s_xyz = get_symbo_xyz(out_file)
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
        s_xyz_w = str(s_xyz[i]).strip()+"\n"
        f.write(s_xyz_w)
    f.close()

#获取工作目录下的所有文件名
for root, dirs, files in os.walk(path):
    for out_file in files:
        if '.out' in out_file:
            Nt = is_Nt(out_file)
            if Nt == True:
                try:
                    save_gjf(out_file)
                except:
                    print(out_file)
        if '.log' in out_file:
            Nt = is_Nt(out_file)
            if Nt == True:
                try:
                    save_gjf(out_file)
                except:
                    print(out_file)