# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 11:11:22 2020

@author: mnbe
"""

import matplotlib.pyplot as plt
import numpy as np
plt.plot([1, 2, 3, 4])
plt.ylabel('some numbers')
plt.show()

plt.plot([1, 2, 3, 4], [1, 4, 9, 16])

plt.plot([1, 2, 3, 4], [1, 4, 9, 16], 'ro')
plt.axis([0, 6, 0, 20])
plt.show()
x=np.zeros(1000)
y=np.zeros(1000)
y1=np.zeros(1000)
y2=np.zeros(1000)
y3=np.zeros(1000)
y4=np.zeros(1000)
for i in range(0,1000):
    y[i]=100+3*i-.003*np.power(i,2)+0.0000013*np.power(i,3)
    x[i]=i
    y1[i]=100*np.sin(5*i*np.pi/180)
    y2[i]=100*np.sin(10*i*np.pi/180)
    y3[i]=100*np.sin(20*i*np.pi/180)
    y4[i]=100*np.sin(20*i*np.pi/180)
    
#plt.plot(x[1:1000], y[1:1000]+y1[1:1000]+y2[1:1000]+y3[1:1000])
plt.plot(x, y+y1+y2+y3+y4)
plt.show()
plt.plot(x, y+y1+y2+y3)
plt.show()
plt.plot(x, y+y1+y4)
plt.show()
    