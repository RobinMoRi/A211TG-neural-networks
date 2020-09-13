# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 10:54:33 2020

@author: mnbe
"""
from numpy import asarray
from numpy import savetxt
with open('data1D.txt', 'r') as f:
    data = f.read()
    

# define data
data = asarray([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]])
# save to csv file
savetxt('data1D.csv', data, delimiter=',')

# load numpy array from csv file
from numpy import loadtxt
# load array
data2 = loadtxt('data1D.txt', delimiter=',')
# print the array
print(data)