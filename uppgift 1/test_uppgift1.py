# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 10:54:33 2020

@author: mnbe
"""
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from numpy import asarray
import pywt
import pywt.data
img=mpimg.imread('data_uppgift1.jpg')
#imgplot = plt.imshow(img)
img2 = Image.open('data_uppgift1.jpg').convert('LA')
a = asarray(img2)  #nu är bilden som en array och kan transformeras mha HAAR


original = pywt.data.camera()
b=a[0:4096,0:4096,0] 
plt.figure(figsize = (50,15))
plt.imshow(b, interpolation="nearest", cmap=plt.cm.gray)


HorizAvg = ( b[:,1:2:end] + b[:,2:2:end] ) / 2
HorizDiff = ( b[:,1:2:end] - b[:,2:2:end] ) / 2
Horiz = [HorizAvg HorizDiff];

VertAvg = ( Horiz[1:2:end,:] + Horiz[2:2:end,:] ) / 2
VertDiff = ( Horiz[1:2:end,:] - Horiz[2:2:end,:] ) / 2
Vert = [VertAvg; VertDiff];

I2=asarray(Vert).transpose()
plt.figure(figsize = (50,15))
plt.imshow(Vert, interpolation="nearest", cmap=plt.cm.gray)