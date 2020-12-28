# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 10:54:33 2020

@author: Robin Moreno Rinding

This program takes an image (b) and makes a haar transform on the image (n=log2(len(b))) times.
The program will plot the following images respectively:
    1: Original image
    2: Averages and detail coefficients
    3: Zoomed on the averages (compressed image)
    4: The reversed image (inverse haar 2d) to the original form (to be compared with the original image)
    
Note that this program could generate warnings about the number of images being opened (just ignore that...)
"""
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from numpy import asarray
import datetime


def imageData():
    """
    Generates image as array
    """
    img = Image.open('data_uppgift1.jpg').convert('LA')
    # img = Image.open('daniel_image.jpg').convert('LA') # Provade med en bild på min kompis daniel (smickrande bild)
    a = asarray(img)  #nu är bilden som en array och kan transformeras mha HAAR
    return a[0:4096,0:4096,0]
    # return a[500:1524,0:1024, 0]


def transform(array, divNum):
    """
    Transforms array. DivNum decides what to divide the sum/difference with (1 for inverse and 2 for forward algorithm)
    """
    tempArray = []
    
    for i in range(0, len(array) - 1, 2):
        #Vi beräknar de parvisa värdena för de första två kolumnerna
        tempArray.append(int((int(array[i])+int(array[i+1]))/divNum))
        tempArray.append(int((int(array[i])-int(array[i+1]))/divNum))
            
    return tempArray


def orderElements(array, reverse=False):
    """
    Order elements in array (moves averages to top left corner in array)
    reverse=True for inverse Haar 2D
    """
    if not reverse:
        index2=0
        for row in range(0, len(array), 2):
            index=0
            for el in range(0, len(array[row]) - 1, 2):
                array[row].insert(index, array[row].pop(el))
                index += 1
            array.insert(index2, array.pop(row))
            index2 += 1
    else:
        index = 0
        for row in range(int(len(array)/2), len(array), 1):
            array.insert(index + 1, array.pop(row))
            index += 2
        for row in range(0, len(array), 2):
            index = 0
            for el in range(int(len(array[row])/2), len(array[row]), 1):
                array[row].insert(index + 1, array[row].pop(el))
                index += 2
    return array
     
    
def haar2d(b, n):
    """
    Transforms image using haar 2D.
    It makes a transform on the vertical and horisontal directions, 
    then it collects all "averages" to the top left corner - which is the new, compressed image.
    This is iterated log2(len(b)) times (for 4096x4096 image => 12).
    """
    
    image = []
    for L in range(0, n): # Iterate over sweeps
        # Horizontal transform
        temp = []
        for row in range(0, len(b)):
            temp.append(transform(b[row].copy(), 2))
        
        # Vertical transform
        imageTemp = []
        temp = asarray(temp).transpose() # Transpose for col iterations
        for col in range(0, len(temp)):
            imageTemp.append(transform(temp[col].copy(), 2))
        
        # Order elements of transposed array (approx values in top left corner)
        imageTemp = asarray(orderElements(list(map(list, zip(*imageTemp)))))
    
        
        # Image to process in next iteration (top left)
        b = imageTemp[:int(len(imageTemp)/2), :int(len(imageTemp)/2)]
        if L == 0: # In the first iteration the image will just be the image
            image = imageTemp.copy()
        else: # in the other iterations we will have to 
            image[:int(len(imageTemp)), :int(len(imageTemp))] = imageTemp.copy()
        
    return asarray(image)



def haar2dInverse(b, n):
    """
    Restores image back to full-scale image
    Done from specified n (number of sweeps that has been done on the compressed image)
    """

    for L in range(n-1,-1,-1):
        zoomRange = int(2**(np.log2(len(b))-L)) # Where in b to look
        zoomB = b[:zoomRange,:zoomRange]
        # Reorder the average-pixels
        zoomB = asarray(orderElements(zoomB.tolist(), reverse=True))
    
        # Horisontal inverse transform
        temp = []
        for row in range(0, len(zoomB)):
            temp.append(transform(zoomB[row].copy(), 1))
        
        # Vertical inverse transform
        imageTemp = []
        temp = asarray(temp).transpose() # Transpose for col iterations
        for col in range(0, len(temp)):
            imageTemp.append(transform(temp[col].copy(), 1))
            
        #Transpose matrix again and store into b-matrix (replace area as specified by zoomRange)
        b[:zoomRange,:zoomRange] = asarray(list(map(list, zip(*imageTemp)))) 
    return b


# ------------------- MAIN CODE ----------------------------------------------
# Print start time
print('Program started at: ' + str(datetime.datetime.now()))

# Plot the original image
b = imageData()
plt.figure(figsize = (50,15))
plt.imshow(b, interpolation="nearest", cmap=plt.cm.gray)
plt.title('Original image')

# For all 12 sweeps, plot the result after each sweep (could take some time to generate...)
n=int(np.log2(len(b))) # <--------- ADJUST n here for different results
for sweep in range(0, n):
    # Plot the averages together with the detail coefficients
    b2 = haar2d(b.copy(), sweep+1)
    plt.figure(figsize=(50,15))
    plt.imshow(b2, interpolation="nearest", cmap=plt.cm.gray)
    plt.title('Number of sweeps: ' + str(sweep + 1))
    
    # Plot just the averages
    plt.figure(figsize=(50,15))
    plt.imshow(b2[:int(len(b2)/(2**(sweep+1))), :int(len(b2)/(2**(sweep+1)))], interpolation="nearest", cmap=plt.cm.gray)
    plt.title('Zoom (averages), Number of sweeps: ' + str(sweep + 1))

# Restores to initial image, from specified number of sweeps (default: int(np.log2(len(b))))
b3 = haar2dInverse(b2.copy(), n)
plt.figure(figsize=(50,15))
plt.imshow(b3, interpolation="nearest", cmap=plt.cm.gray)
plt.title('Restored image')
    
# Print end time
print('Program ended at' + str(datetime.datetime.now()))