#encoding:utf-8
'''
@author: Mike
'''
import pandas as pd
import re
import os
import time

def freq_ir_extract(file_log):
    Freq=[]
    IR_Inten=[]
    for line in open(file_log,"r"):
        if "Frequencies --" in line:  #查找含有“Frequencies --”的行
            Freq.append(line)
        elif "IR Inten    --" in line: #查找含有"IR Inten    --"的行
            IR_Inten.append(line)    
    Freq_col=[]
    for line in Freq:
        item=line.strip('\n')
        item=re.split('\s+',item)  #'\s+'正则表达式，匹配多个空格
        Freq_col.append(item)
    IR_Inten_col=[]
    for line in IR_Inten:
        item=line.strip('\n')
        item=re.split('\s+',item)
        IR_Inten_col.append(item)
    result_freq=[]  #收集频率结果
    for i in range(0,len(Freq_col)):
        result_freq.append(Freq_col[i][3])
        result_freq.append(Freq_col[i][4])
        result_freq.append(Freq_col[i][5])
    result_ir=[]    #收集红外结果
    for i in range(0,len(IR_Inten_col)):
        result_ir.append(IR_Inten_col[i][4])
        result_ir.append(IR_Inten_col[i][5])
        result_ir.append(IR_Inten_col[i][6]) 
    #out={'Freq':result_freq,'IR':result_ir}
    #out = pd.DataFrame(data=out)
    #out = out.as_matrix(columns=None)  
    out = pd.DataFrame(result_ir,result_freq,columns=[''])
    return out

#获取工作目录下的所有文件名
def main(path):
    files = os.listdir(path)
    for file_log in files :
        if '.log' in file_log:
            out_file_name = file_log + '.dat'
            out=freq_ir_extract(file_log)
            out.to_csv(file_log+'.csv',header=False)
            try:
                out_file=open(out_file_name,'w')   #以w模式访问文件other.txt
                print(out, file=out_file)           #将列表内容写到文件
            except IOError:
                print ('File error')
            finally:
                out_file.close()
        if '.out' in file_log:
            out_file_name = file_log + '.dat'
            out=freq_ir_extract(file_log)
            out.to_csv(file_log.replace('.out','')+'.csv',header=False)
            try:
                out_file=open(out_file_name,'w')   #以w模式访问文件other.txt
                print(out, file=out_file)           #将列表内容写到文件
            except IOError:
                print ('File error')
            finally:
                out_file.close()

print('''\
脚本功能：从高斯09的log或者out结果文件中提取Frequencies和IR Inten信息
''')


path = input('请输入log或者out文件所在的文件夹：')
os.chdir(path)
print('当前工作文件夹 %s'%os.getcwd())
main(path)
is_continue = input('是否还需要继续处理（Y/N）：')
while is_continue == 'Y' or is_continue == 'y':
    path = input('请输入log或者out文件所在的文件夹：')
    os.chdir(path)
    print('当前工作文件夹：%s'%os.getcwd())
    main(path)
    is_continue = input('是否还需要继续处理（Y/N）：')
else:
    print('数据处理完成，程序即将关闭！')
    time.sleep(3)