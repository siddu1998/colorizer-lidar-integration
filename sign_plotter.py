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


style.use('dark_background')


#load data frame of sign 
df1 = pd.read_csv('signs_13.csv')
#create df with only required 
df_sign = df1[['SignId','pX','pY','Retro']]

#less then 0.3
x3_very_poor=[]
y3_very_poor=[]
dz_very_poor=[]

#between 0.31-0.5
x3_average_point=[]
y3_average_point=[]
dz_average_point=[]

#between 0.51-0.6
x3_above_average_point=[]
y3_above_average_point=[]
dz_above_average_point=[]

#between 0.61-1
x3_great_point=[]
y3_great_point=[]
dz_great_point=[]


for i,row in df_sign.iterrows():
    if row['Retro']<0.3:
        x3_very_poor.add(row['pX'])
        y3_very_poor.add(row['pY'])
        dz_very_poor.add(row['Retro'])
    if 0.31<row['Retro']<0.5:
        x3_average_point.append(row['pX'])
        y3_average_point.append(row['pY'])
        dz_average_points.append(row['Retro'])
    if 0.51<row['Retro']<0.6:
        x3_above_average_point.append(row['pX'])
        y3_above_average_point.append(row['pY'])
        dz_above_average_point.append(row['Retro'])
    if row['Retro']>0.61:
        x3_great_point.append(row['pX'])
        y3_great_point.append(row['pY'])
        dz_great_point.append(row['Retro'])
    


dx=0.02
dy=0.02
z3_very_poor=np.zeros(len(x3_very_poor))
z3_average_point=np.zeros(len(x3_average_point))
z3_above_average=np.zeros(len(x3_above_average_point))
z3_great_point=np.zeros(len(x3_great_point))

fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')

# if len(x3_great_point)>0:
#     ax1.bar3d(x3_great_point, y3_great_point, z3, dx, dy, dz_great_point,color='g')
# if len(x3_above_average_point)>0:
#     ax1.bar3d(x3_average_point, y3_average_point, z3, dx, dy, dz_average_point,color='b')
# if len(x3_very_poor)>0:
#     ax1.bar3d(x3_very_poor, y3_very_poor, z3, dx, dy, dz_very_poor,color='r')

if len(x3_great_point)>0:
    ax1.bar3d(x3_great_point, y3_great_point,z3_great_point, dx, dy, dz_great_point,color='g')
else:
    pass
if len(x3_average_point)>0:
    ax1.bar3d(x3_average_point, y3_average_point,z3_average_point, dx, dy, dz_average_point,color='orange')
else:
    pass
if len(x3_very_poor)>0:
    ax1.bar3d(x3_very_poor, y3_very_poor, z3_very_poor, dx, dy, dz_very_poor,color='r')
else:
    pass

if len(x3_above_average_point)>0:
    ax1.bar3d(x3_above_average_point, y3_above_average_point, z3_above_average, dx, dy,dz_above_average_point ,color='y')
else:
    pass

ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_zlabel('retro')
ax1.set_zlim3d(0,1)
plt.show()
