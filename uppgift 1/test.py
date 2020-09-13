#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 10:10:46 2020

@author: mac
"""
import numpy as np
# array = [[1,2,3,4,5,6,7,8], [1,2,3,4,5,6,7,8], [2,2,3,4,5,6,7,8], [1,2,3,4,5,6,7,8], [3,2,3,4,5,6,7,8], [1,2,3,4,5,6,7,8], [4,2,3,4,5,6,7,8], [1,2,3,4,5,6,7,8]]

# print(array)
# index2=0
# for row in range(0, len(array), 2):
#     index=0
#     for el in range(0, len(array[row]) - 1, 2):
#         array[row].insert(index, array[row].pop(el))
#         index += 1
#     array.insert(index2, array.pop(row))
#     index2 += 1
# print(array)

# index = 0
# for row in range(int(len(array)/2), len(array), 1):
#     array.insert(index + 1, array.pop(row))
#     index += 2
# for row in range(0, len(array), 2):
#     index = 0
#     print(row)
#     for el in range(int(len(array[row])/2), len(array[row]), 1):
#         array[row].insert(index + 1, array[row].pop(el))
#         index += 2


# print(array)

# index=0
# for row in range(0, len(array), 2):
#     array.insert(index, array.pop(row))
#     index += 1
# print(array)


n = 12

lengthMatrix=4096
sizes = [int(2**(np.log2(lengthMatrix)-item)) for item in range(n-1,-1,-1)]
print(sizes)

