# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 11:11:22 2020

@author: mnbe
"""

import matplotlib.pyplot as plt
import numpy as np
# plt.plot([1, 2, 3, 4])
# plt.ylabel('some numbers')
# plt.show()
# plt.title('Some numbers plot')

# plt.plot([1, 2, 3, 4], [1, 4, 9, 16])

# plt.plot([1, 2, 3, 4], [1, 4, 9, 16], 'ro')
# plt.axis([0, 6, 0, 20])
plt.show()
j=np.power(2,7)
x=np.zeros(j)
y=np.zeros(j)
y1=np.zeros(j)
y2=np.zeros(j)
y3=np.zeros(j)
y4=np.zeros(j)
for i in range(0,j):
    y[i]=100+3*i-.003*np.power(i,2)+0.0000013*np.power(i,3)
    x[i]=i
    y1[i]=100*np.sin(5*i*np.pi/180)
    y2[i]=100*np.sin(10*i*np.pi/180)
    y3[i]=100*np.sin(20*i*np.pi/180)
    y4[i]=100*np.sin(40*i*np.pi/180)
    
#plt.plot(x[1:1000], y[1:1000]+y1[1:1000]+y2[1:1000]+y3[1:1000])
plt.title('Initial signal (simulated)')
plt.plot(x, y+y1+y2+y3+y4)

plt.show()

#-------------------------------------------
# In place fast haar wavelet transform
s=y+y1+y2+y3+y4
s0=s
print('Dim of S: ', s.shape)
n=int(np.log2(len(s)))
I=1
J=2
M=int(np.power(2,n))
for L in range(1,n+1):
      M=int(M/2)
      for K in range(0,(M)):
          a1=(s[K*J]+s[K*J+I])/2
          c2=(s[K*J]-s[K*J+I])/2
          s[K*J]=a1
          s[K*J+I]=c2
          if L==4: # Vid svep 4 nollställer vi alla koefficienter
              s[K*J+I]=0

      I=J
      J=J*2 # %tar andra halvan
     
plt.title('Koeffiecienter med medelvärde')
plt.plot(x,s)
print('Dim of S1: ', s.shape)
plt.show()

#-------------------------------------------
#Inverse transform
n=int(np.log2(len(s)))
I=np.power(2,n-1);
J=2*I;
M=1;
K=0;
for L in range(n+1,1,-1):
    for K in range(0,(M)):
         a1=(s[K*J]+s[K*J+I])
         c2=(s[K*J]-s[K*J+I])
         s[K*J]=a1
         s[K*J+I]=c2
    J=I;
    I=np.int(I/2);
    M=2*M;
s2=s
print('Dim of S2: ', s2.shape)
plt.title('Filtrerat data')
plt.plot(x,s2)