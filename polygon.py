from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style
import pandas as pd 
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib
from matplotlib.figure import Figure
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
import tkinter as tk
from tkinter import ttk 
from PIL import ImageTk, Image
import matplotlib.image as mpimg
from matplotlib.cbook import get_sample_data

from matplotlib._png import read_png
from pylab import *

#load data frame of sign TODO: get this from the user argument
df1 = pd.read_csv('signs_4.csv')
#create df with only required 
df_sign = df1[['SignId','pX','pY','Retro','COLOR']]
dz=0

red_signs_x=[]
red_signs_y=[]
dz_red_signs=[]

white_signs_x=[]
white_signs_y=[]
dz_white_signs=[]


for i,row in df_sign.iterrows():

    if row['COLOR']=='RED':
        red_signs_x.append(row['pX'])
        red_signs_y.append(row['pY'])
        dz_red_signs.append(row['Retro'])
    if row['COLOR']=='WHITE':
        white_signs_x.append(row['pX'])
        white_signs_y.append(row['pY'])
        dz_white_signs.append(row['Retro'])
dx=0.01
dy=0.01
LARGE_FONT=("Verdana",12)
print(len(red_signs_x),len(red_signs_y),len(dz_red_signs))
print(len(white_signs_x),len(white_signs_y),len(dz_white_signs))

# fig = plt.figure()
# ax1 = fig.add_subplot(111, projection='3d')
# ax1.bar3d(red_signs_x, red_signs_y, dz, dx, dy, dz_red_signs,color='r')
# ax1.bar3d(white_signs_x,white_signs_y,dz,dx,dy,dz_white_signs,color='w')
# ax1.scatter#d
# # fn = get_sample_data("status.png", asfileobj=False)
# # img = read_png(fn)
# # xx, yy = ogrid[0:img.shape[0], 0:img.shape[1]]
# # X = xx
# # Y = yy

# # ax1.plot_surface(X, Y, Z1, rstride=1, cstride=1, facecolors=img, shade=False)
# # surf = ax1.plot_surface(X, Y, Z, cmap=cm.RdYlGn_r, linewidth=0, antialiased=False)

# ax1.set_xlabel('x axis')
# ax1.set_ylabel('y axis')
# ax1.set_zlabel('Retro')

# plt.show()

if(len(red_signs_x)>0):
    plt.scatter(red_signs_x,red_signs_y, label='red', color='r', s=25, marker="o")
else:
    print("[INFO] No red points in this sign")
if(len(white_signs_x)>0):
    plt.scatter(white_signs_x,white_signs_y, label='white', color='grey', s=25, marker="o")
else:
    print("[INFO] No white points in this sign")

plt.xlabel('x')
plt.ylabel('y')
plt.title('Sign 1 (Full White Stop Sign)')
#plt.legend()
plt.show()
    