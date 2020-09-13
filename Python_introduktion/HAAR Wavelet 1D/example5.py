# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 21:06:53 2020

@author: mnbe
"""

import numpy as np
"""barne=np.log2(arne)
barne=np.log(arne)
arne=np.exp2(10)
arne=np.exp(10)
karne=np.power(2,2)
x=[1,2,3,4,5,1,1,1,1];
test=len(x)
%=======================================================
%Det tog 30 minuter att kodifiera algoritmen på sid 28 i 
%Wavelets made easy
%===================================================="""
s=[3, 1, 0, 4, 8, 6, 9, 9] #indata

n=int(np.log2(len(s)))
I=1
J=2
M=int(np.power(2,n))
K=0
L=1

for L in range(1,n+1):
     M=int(M/2)
     for K in range(0,(M)):
         a1=(s[K*J]+s[K*J+I])/2
         c2=(s[K*J]-s[K*J+I])/2
         s[K*J]=a1
         s[K*J+I]=c2

     I=J
     J=J*2 # %tar andra halvan
    
""" 
s_t=5     1     0    -2    -3     1    -1     0 # %första värdet är medelvärdet, resten koefficenter för 1:a 2:a resp 3:e sweep
%===============================================
matlabvarianten
s=[3 1 0 4 8 6 9 9];indata
% s2=[9 7 6 2;5 3 4 4;8 2 4 0;6 0 2 2];
% s=s2(1,:);
n=log2(length(s))
I=1;
J=2;
M=2^n;
K=0;
s
for L=1:1:n
%     for ijk=1:4
% s=s2(ijk,:);        
M=M/2;
for K=0:1:M-1
a1=(s(K*J+1)+s(K*J+I+1))/2;
c2=(s(K*J+1)-s(K*J+I+1))/2;
s(K*J+1)=a1;
s(K*J+I+1)=c2;
% s2(ijk,:)=s; 
end
I=J;
J=J*2; %tar andra halvan
%     end
% I=1;
% J=2;
% M=2^n;    
end

%filtrering"""

