#encoding:utf-8
import numpy as np
import matplotlib.pyplot as plt
import random

MAX = 1000000

# 计算最近邻类簇中心
def nearestNeighbor(index):
    dd = MAX
    neighbor = -1
    for i in range(length):
        if dist[index, i] < dd and rho[index] < rho[i]:
            dd = dist[index, i]
            neighbor = i
    if result[neighbor] == -1:
        result[neighbor] = nearestNeighbor(neighbor)
    return result[neighbor]

# Read data
fileName = input("Enter the file's name: ")
location = []
label = []
for line in open(fileName, "r"):
    items = line.strip("\n").split(",")
    label.append(int(items.pop()))  # pop 从列表中移除并返回最后一个对象
    tmp = []
    for item in items:
        tmp.append(float(item))
    location.append(tmp)
location = np.array(location)       # n*2
label = np.array(label)             # n*1
length = len(location)              # length 位置（对象）总数

# Calculate distance
dist = np.zeros((length, length))  # 存储各点之间的距离
ll = []
begin = 0
while begin < length-1:  # begin控制外循环
    end = begin + 1
    while end < length:  # end控制内循环
        dd = np.linalg.norm(location[begin]-location[end])   # ？距离计算公式
        dist[begin][end] = dd
        dist[end][begin] = dd
        ll.append(dd)
        end = end + 1
    begin = begin + 1
ll = np.array(ll)

# 阈值确定思路：对所有距离进行排序，取2%分位数
# percent = float(raw_input("Enter the average percentage of neighbors: "))
percent = 2.0
position = int(len(ll) * percent / 100)
sortedll = np.sort(ll)
dc = sortedll[position]    #阈值

# local density
rho = np.zeros((length, 1))   # rho n*1 记录每个点的局部密度
begin = 0
while begin < length-1:
    end = begin + 1
    while end < length:
        rho[begin] = rho[begin] + np.exp(-(dist[begin][end]/dc) ** 2)
        rho[end] = rho[end] + np.exp(-(dist[begin][end]/dc) ** 2)
        #if dist[begin][end] < dc:
        #    rho[begin] = rho[begin] + 1
        #    rho[end] = rho[end] + 1
        end = end + 1
    begin = begin + 1

# 求比点的局部密度大的点到该点的最小距离
delta = np.ones((length, 1)) * MAX
maxDensity = np.max(rho)
begin = 0
while begin < length:
    if rho[begin] < maxDensity:
        end = 0
        while end < length:
            if rho[end] > rho[begin] and dist[begin][end] < delta[begin]:
                delta[begin] = dist[begin][end]
            end = end + 1
    else:
        delta[begin] = 0.0
        end = 0
        while end < length:
            if dist[begin][end] > delta[begin]:
                delta[begin] = dist[begin][end]
            end = end + 1
    begin = begin + 1

rate1 = 0.5
#Aggregation Spiral 0.6
#Jain Flame 0.8
#D31 0.75
#R15 0.6
#Compound 0.5
#Pathbased 0.2
thRho = rate1 * (np.max(rho) - np.min(rho)) + np.min(rho)

rate2 = 0.3
#Aggregation Spiral 0.2
#Jain Flame 0.2
#D31 0.05
#R15 0.1
#Compound 0.08
#Pathbased 0.4
thDel = rate2 * (np.max(delta) - np.min(delta)) + np.min(delta)


result = np.ones(length, dtype=np.int) * (-1)
center = 0
for i in range(length): #items:
    if rho[i] > thRho and delta[i] > thDel:
        result[i] = center
        center = center + 1

for i in range(length):
    dist[i][i] = MAX

for i in range(length):
    if result[i] == -1:
        result[i] = nearestNeighbor(i)
    else:
        continue

# 作决策图，rho  局部密度，delta  到具有更高局部密度对象的距离的最小值
plt.plot(rho, delta, '.')
plt.xlabel('rho'), plt.ylabel('delta')
plt.show()

# 设定colors
R = list(range(256))
random.shuffle(R)
R = np.array(R)/255.0
G = list(range(256))
random.shuffle(G)
G = np.array(G)/255.0
B = list(range(256))
random.shuffle(B)
B = np.array(B)/255.0
colors = []
for i in range(256):
    colors.append((R[i], G[i], B[i]))

# 聚类结果作图
plt.figure()
for i in range(length):
    index = result[i]
    plt.plot(location[i][0], location[i][1], color = colors[index], marker = '.')
plt.xlabel('x'), plt.ylabel('y')
plt.show()

# 利用原始类标签作图，验证聚类结果的准确性
plt.figure()
for i in range(length): # 利用循环将每一个点画到图上
    index = label[i]
    plt.plot(location[i][0], location[i][1], color = colors[index], marker = '.')
plt.xlabel('x'), plt.ylabel('y')
plt.show()