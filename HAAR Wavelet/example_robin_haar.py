#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 15:07:02 2020

@author: Robin Moreno Rinding
"""
import matplotlib.pyplot as plt
import numpy as np

class Signal:
    def __init__(self, s, x):
        self.s = s
        self.x = x
        
def generateData():
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
        
    return Signal(y+y1+y2+y3+y4, x)

#---------------- Fast In-Place Haar Wavelet Transform -----------------------
def haarTransform(s, sweepReset):
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
              if L==sweepReset: # Vid svep 4 nollställer vi alla koefficienter
                  s[K*J+I]=0
    
          I=J
          J=J*2 # %tar andra halvan
    return s.copy()

#------------ Fast In-Place Inverse Haar Wavelet Transform --------------------

def haarInverseTransform(s):
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
    return s.copy()


sig = generateData() #Generate x and y from simulated signal

s0 = sig.s
s1 = haarTransform(s0.copy(), 4)
s2 = haarInverseTransform(s1.copy())
plt.plot(sig.x, s0, label='Initial Signal')
plt.plot(sig.x, s1, label='Fast In-Place Haar Wavelet Transform')
plt.plot(sig.x, s2, label='Fast In-Place Inverse Haar Wavelet Transform')
plt.legend(loc="upper left")