# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 14:29:51 2017

@author: Mike
@version: 1.0
"""

'''
处理思路：
    1、读入文件，获取每个离子的飞行时间
    2、接收用户输入的分组数据
    3、统计每组的数量
    4、保存结果到文件
'''

# 1、读入文件，获取每个离子的飞行时间
f = input('请输入文件所在的位置（示例：c:\ions.txt）：')
with open(f,'r') as txt:
    txt.readline()
    datas = txt.readlines()
    
fly_t = [] # 存储每个离子的飞行时间
for data in datas:
    fly_t.append(data.split(';')[1])

if len(datas) != len(fly_t):
    print('离子数量与获取的飞行时间个数不一致，请检查输入文本文件的格式！！！')

# 2、接收用户输入的分组数据
g = input('请输入最小值|组距|分组数量（示例：10.0000|0.0010|10）：')
min_,interval,nums = g.split('|')

print('你输入的最小值是{0},组距是{1},分组数量是{2}'.format(min_,interval,nums))


# 3、统计每组的数量
groups = [float(min_)]
for i in range(1,int(nums)):
    groups.append(float(min_)+float(interval)*i)

counts = []
for i in range(int(nums)):
    counts.append('0')

for i in range(int(nums)):
    for t in fly_t:
        if i != 9:
            if float(groups[i+1]) > float(t) >= float(groups[i]):
                counts[i] = int(counts[i])+1
        else:
            if float(t) >= float(groups[i]):
                counts[i] = int(counts[i])+1

# 4、写入结果文件
with open('result.txt','w+') as f:
    for i in range(int(nums)):
        f.write(str(round(float(groups[i]),4))+'|'+str(counts[i])+'\n')
