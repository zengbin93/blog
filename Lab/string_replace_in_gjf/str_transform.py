# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 13:14:07 2016

@author: Mike
"""
import os
from tkinter.filedialog import askdirectory
path = askdirectory()
os.chdir(path)
print('''用于文件夹中gif文件内容修改！

使用方法：
    from  需要修改的字符
    to    目标字符
''')


def modifyip(tfile, sstr, rstr):
    """
    功能：替换文件中的字符串
    """
    try:
        lines = open(tfile, 'r').readlines()
        flen = len(lines) - 1
        for i in range(flen):
            if sstr in lines[i]:
                lines[i] = lines[i].replace(sstr, rstr)
        open(tfile, 'w').writelines(lines)
    except Exception as e:
        print(e)


f = input('请输入需要修改的字符：')
t = input('请输入目标字符：')
for root, dirs, files in os.walk(path):
    for file in files:
        if '.gjf' in file:
            modifyip(file, f, t)
            print('当前文件处理完成', file)
