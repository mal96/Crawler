# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 22:27:44 2017
data process
@author: maliang
"""
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

path = '985data\\'

FileList_raw = os.listdir(path)
FileList = [item for item in FileList_raw if item[-3:] == 'csv']
UnivList = [item.split('.')[0] for item in FileList]
del(FileList_raw)

Dataset = {}
for file, univ in zip(FileList, UnivList):
    Dataset[univ] = pd.read_csv(path+file, sep=',', encoding='GBK')

com_num = {}
for univ in Dataset:
    num_list = list(Dataset[univ]['点评数量'])
    com_num[univ] = num_list

for univ in com_num:
    num_list = np.array(com_num[univ]).astype(int)
    fig = plt.figure(dpi = 300)
    bins = int((max(num_list) - min(num_list))/30)
    plt.hist(num_list, bins=bins, facecolor='g', alpha=0.9)
    plt.tight_layout()
    fig.savefig(path + 'com_num\\' + univ + '.jpg')
    plt.close(fig)

prices = {}
for univ in Dataset:
    price_list_str = list(Dataset[univ]['人均'])
    price_list = [int(item[1:]) for item in price_list_str]
    prices[univ] = price_list

mean_price = {}
for univ in prices:
    mean_price[univ] = np.mean(prices[univ])

ff = open('meanprice.csv', 'a+')
for univ in mean_price:
    ff.write(univ+ ',')
    ff.write(str(mean_price[univ])+ '\n')
ff.close()

tastes = {}
envs = {}
sers = {}
for univ in Dataset:
    tastes[univ] = list(Dataset[univ]['口味'])
    envs[univ] = list(Dataset[univ]['环境'])
    sers[univ] = list(Dataset[univ]['服务'])

m_taste = {}
m_env = {}
m_ser = {}
for univ in Dataset:
    m_taste[univ] = np.mean(tastes[univ])
    m_env[univ] = np.mean(envs[univ])
    m_ser[univ] = np.mean(sers[univ])
print(m_taste, m_env, m_ser, sep = '\n--------------\n')


f = open('rate.csv', 'a+')
f.write(',')
f.write('口味'+','+'环境'+','+'服务'+'\n')
for univ in m_taste:
    f.write(univ+',')
    f.write(str(m_taste[univ])+',')
    f.write(str(m_env[univ])+',')
    f.write(str(m_ser[univ])+'\n')
f.close()
    
    
    
    







