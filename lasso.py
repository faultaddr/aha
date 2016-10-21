# -*- coding:utf-8 -*-
import numpy as np
import scipy.io as sio
#from sklearn import decomposition
#from mpl_toolkits.mplot3d import Axes3D
#import matplotlib.pyplot as plt
K=[]
matfn='C:\\Users\\panda\\Desktop\\hhh.mat'
data=sio.loadmat(matfn)
array=data['D']
array_T=array.T
value=[]
for i in range(6128):
  for j in range(90):
    if(array_T[i][j]!=0):
      array_T[i][j]=1
for x in range(6128):
  for y in range(6128):
    K.append(int(np.dot(array_T[x],array_T[y])))
  value.append(K)
  K=[]
c=np.array(value)
fp=open('vector2.txt','a')
for line in value:
  for num in line:
    fp.write(str(num))
    fp.write(" ")
    #print num
  fp.write("\n")
  #print "\n"
fp.close()
#pca = decomposition.PCA(n_components=3, copy=False, whiten=False)
#newData=pca.fit_transform(c)
#x,y,z = newData[0],newData[1],newData[2]
#fig = plt.figure()
#ax = fig.add_subplot(111,projection='3d')


#ax.scatter(x[:229],y[:229],z[:229],c='y')
#ax.scatter(x[230:459],y[230:459],z[230:459],c='r')

#ax.set_zlabel('Z')
#ax.set_ylabel('Y')
#ax.set_xlabel('X')
#plt.show()