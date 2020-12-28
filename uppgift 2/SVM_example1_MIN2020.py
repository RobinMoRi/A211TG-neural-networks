# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 17:03:45 2019

@author: Magnus Bengtsson
"""

import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
def objective(x):
      d=0.5*(x[0]*x[0]+x[1]*x[1])*1000
      return d
def constraint1(x):
    y =(1,1,1,1,1,1,-1,-1,-1,-1,-1,-1)
    x1=(6,	8,	12,	10,	15,	13,	3,	7,	4,	8,	7,	10)
    x2=(15,	12,	13,	10,	10,	8,	10,	7,	6,	4,	4,	2)
    x3=(15,	12,	13,	10,	10,	8,	10,	7,	6,	4,	4,	2)
    n=len(y)
    c=np.zeros(n)
    for i in range(len(y)):
          c[i]=(x[0]*x1[i]+x[1]*x2[i]+x[2])*y[i]-1; #written in positive null form
    return c


# initial guesses
n = 3
x0 = np.zeros(n)
x0[0] = 100
x0[1] = 100
x0[2] = 100



# show initial objective
print('Initial Objective: ' + str(objective(x0)))

# optimize
b = (-100,100)
bnds = (b, b, b)
con1 = {'type': 'ineq', 'fun': constraint1} 

cons = ([con1])
solution = minimize(objective,x0,method='SLSQP',bounds=bnds,constraints=cons)
x = solution.x

# show final objective
print('Final Objective: ' + str(objective(x)))

# print solution
print('Solution')
print('x1 = ' + str(x[0]))
print('x2 = ' + str(x[1]))
print('x3 = ' + str(x[2]))
x1=(6,	8,	12,	10,	15,	13,	3,	7,	4,	8,	7,	10)
y=(15,	12,	13,	10,	10,	8,	10,	7,	6,	4,	4,	2)
y2=-x[0]*np.divide(x1, x[1])-x[2]/x[1]
#y2=-x[0]*x1/x[1]-x[2]/x[1]
plt.plot(x1, y, 'ro',x1,y2)
plt.axis([0, 15, 0, 20])
plt.show()
x1=(6,	8,	12,	10,	15,	13,	3,	7,	4,	8,	7,	10)
x2=(15,	12,	13,	10,	10,	8,	10,	7,	6,	4,	4,	2)
if (x[0]*4.0+x[1]*22.5+x[2])-1<0:
    print('nedre ')