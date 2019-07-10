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

style.use('ggplot')


#load data frame of sign 
df_sign = pd.read_csv('signs.csv')
#create df with only required 
df1 = df_sign[['pX','pY','Retro']]
print(df1.head())

x3=[i for i in df1['pX']]
y3=[i for i in df1['pY']]
z3=[i for i in df1['Retro']]



# fig = plt.figure()
# ax1 = fig.add_subplot(111, projection='3d')

# x3 = [1,2,3,4,5,6,7,8,9,10]
# y3 = [5,6,7,8,2,5,6,3,7,2]
# z3 = np.zeros(10)
# dx = np.ones(10)
# dy = np.ones(10)
# dz = [1,2,3,4,5,6,7,8,9,10]

# ax1.bar3d(x3, y3, z3, dx, dy, dz)


# ax1.set_xlabel('x')
# ax1.set_ylabel('y')
# ax1.set_zlabel('retro')

# plt.show()