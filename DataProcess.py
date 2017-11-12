# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 16:09:41 2017

@author: maliang
"""
import pandas as pd
import matplotlib.pyplot as plt
from functools import reduce

def add(a, b):
    return a+b

def popchar(string, char):
    SeqList = list(string)
    newSeqList = [item for item in SeqList if item != char]
    return reduce(add, newSeqList)
    
df = pd.read_csv('DataExtracted_DianPing.csv', sep=',', encoding='GBK')
prices = list(df['人均'])
for i in range(len(prices)):
    prices[i] = int(popchar(prices[i], '￥'))

tastes = list(df['口味'])
envs = list(df['环境'])
services = list(df['服务'])

lim = [6.0, 10.0, 0, 700]
fig = plt.figure(dpi = 500, figsize=(12,5))
p1 = plt.subplot(1,3,1)
p2 = plt.subplot(1,3,2)
p3 = plt.subplot(1,3,3)
p1.scatter(tastes, prices, s = 10)
p2.scatter(envs, prices, s = 10)
p3.scatter(services, prices, s = 10)

p1.axis(lim)
p2.axis(lim)
p3.axis(lim)

p1.set_title('Taste-Price')
p2.set_title('Environment-Price')
p3.set_title('Service-Price')
plt.tight_layout()
fig.savefig('TasteEnvironmentService-Price.jpg')
plt.close(fig)