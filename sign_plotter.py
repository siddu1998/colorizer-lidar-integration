"""
Author : Sai Siddartha Maram
email  : smaram_be16@thapar.edu , smaram7@gatech.edu

Description : 
The function takes a set of points stored in the csv file. These points correspond to LiDAR points
reflected of the sign, task is to generate a 3D plot of the points and use the retrointensity to determine the color code of the points
""" 


from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style
import pandas as pd 
import matplotlib.cm as cm
import matplotlib.colors as colors


style.use('fivethirtyeight')


#load data frame of sign 
df1 = pd.read_csv('signs_4.csv',name=['SignId','pX','pY','Retro'])
#create df with only required 
#df1 = df_sign[['SignId','pX','pY','Retro']]
print(df1.head())

x3=[i for i in df1['pX'] ]
y3=[i for i in df1['pY'] ]
z3=0

dx=0.05 *np.ones(len(x3))
dy=0.05
dz=[i for i in df1['Retro']]


fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')

max_dz=max(dz)

normalized_dz=[i/max_dz for i in dz]

colors = plt.cm.jet(dz)
print(type(colors))
#ax1.bar3d(x3,y3,z3)
ax1.bar3d(x3, y3, z3, dx, dy, dz,color=colors)


ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_zlabel('retro')
ax1.set_zlim3d(0,1)
plt.show()