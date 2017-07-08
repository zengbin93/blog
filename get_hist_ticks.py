# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 12:22:28 2017

@author: Mike
"""

import tushare as ts
from datetime import date,timedelta,datetime
import pandas as pd
import logging

# 创建一个logger 
logger = logging.getLogger('mylogger') 
logger.setLevel(logging.DEBUG) 
   
# 创建一个handler，用于写入日志文件 
fh = logging.FileHandler('get_hist_ticks_result.log') 
fh.setLevel(logging.DEBUG) 
   
# 再创建一个handler，用于输出到控制台 
ch = logging.StreamHandler() 
ch.setLevel(logging.DEBUG) 
   
# 定义handler的输出格式 
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s') 
fh.setFormatter(formatter) 
ch.setFormatter(formatter) 
   
# 给logger添加handler 
logger.addHandler(fh) 
logger.addHandler(ch) 
   
# 记录一条日志 
#logger.info('foorbar') 


def get_hist_ticks(codes,start,end,csv):
    '''获取codes中所有股票从start到end的所有历史分笔数据'''
    delta = timedelta(days=1)
    for code in codes:
        d_ = start
        while d_ <= end:
            # 调用ts获取历史分笔数据
            try:
                ticks = ts.get_tick_data(code,date=d_,retry_count=10)
                ticks['date'] = d_
                ticks['code'] = '|'+code
                ticks.to_csv(csv,index=False,mode='a',encoding='gbk')
                logger.info('{0}在{1}的分笔数据获取成功！'.format(code,d_))
            except:
                logger.info('{0}在{1}的分笔数据获取失败！'.format(code,d_))  
            d_ = d_ + delta
    
    # 读取csv文件，去掉重复数据
    datas = pd.read_csv(csv,encoding='gbk')
    datas = datas.drop_duplicates().dropna()
    datas = datas[datas['time'] != 'time']
    datas = datas[['code','date','time','price','change','volume','amount','type']]
    datas = datas.sort_values(by=['code','date','time'])
    datas.to_csv(csv,index=False,encoding='gbk')
    return datas


if __name__ == '__main__':
    # 需要下载历史分笔数据的代码    
    codes = ['600122','600977','601611','002256','002631','601595']
    # 存储数据的csv文件
    csv = 'hist_ticks.csv'
    # 开始和结束日期
    start = date(2015,1,1)
    end = datetime.now().date()
    # 调用函数开始下载
    get_hist_ticks(codes=codes,start=start,end=end,csv=csv)
    