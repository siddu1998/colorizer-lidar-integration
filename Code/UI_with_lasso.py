"""
################################################
Author : Sai Siddartha Maram    (msaisiddartha1@gmail.com)
Data   : July 2019
Summary: 1. An application to visualize 3D LiDAR data and generate statistical insights about it and recommend the 
         apt replacement strategy
         2. Provide smooth Selection mechanism using concept of Lasso selection
         3. Generate and compare statistical trends upon regions of intrests
         4. Dicscusses Retro intensity spatially
         5. Study on retro intensity and its dependence with color
         6. Study of retro intensity as a property of age
###############################################
"""

import numpy as np

from matplotlib.widgets import LassoSelector
from matplotlib.path import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
plt.style.use('dark_background')
import statistics
import csv

#imports

import os
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
import statistics


#bins for the histogram
bins=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]



#load data from the the lidar inventory
df1 = pd.read_csv('../Data/signs.csv')

#load only these coloumns
df1 = df1[['SignId','pX','pY','Retro','COLOR']]
#group the signs by sign Id
df1 = df1.groupby('SignId')

#enter the sign you want to study
sign=int(input("Please enter the sign you want to plot"))
#get those particular signs
df1 = df1.get_group(sign)

#less then 0.4
x3_very_poor=[]
y3_very_poor=[]
dz_very_poor=[]

#between 0.4-0.5
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

retro_master=[]

red_signs_x=[]
red_signs_y=[]


white_signs_x=[]
white_signs_y=[]

blue_signs_x=[]
blue_signs_y=[]

green_signs_x=[]
green_signs_y=[]

yellow_signs_x=[]
yellow_signs_y=[]

dz=[]

for i,row in df1.iterrows():
    if row['COLOR']=='RED':
        red_signs_x.append(row['pX'])
        red_signs_y.append(row['pY'])
        dz.append(row['Retro'])
    if row['COLOR']=='WHITE':
        white_signs_x.append(row['pX'])
        white_signs_y.append(row['pY'])
        dz.append(row['Retro'])
    if row['COLOR']=='BLUE':
        blue_signs_x.append(row['pX'])
        blue_signs_y.append(row['pY'])
    if row['COLOR']=='GREEN':
        green_signs_x.append(row['pX'])
        green_signs_y.append(row['pY'])
    if row['COLOR']=='YELLOW':
        yellow_signs_x.append(row['pX'])
        yellow_signs_y.append(row['pY'])






#categorize points TODO: there is an efficient way to do it using iloc (time constraint hence left it here using simple for loop)
for i,row in df1.iterrows():
    retro_master.append(row['Retro'])
    if row['Retro']<0.4:
        x3_very_poor.append(row['pX'])
        y3_very_poor.append(row['pY'])
        dz_very_poor.append(row['Retro'])
    if 0.41<row['Retro']<0.5:
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
    

#length and width of each bar
dx=0.03
dy=0.03



#heights of each point category
z3_very_poor=np.zeros(len(x3_very_poor))
z3_average_point=np.zeros(len(x3_average_point))
z3_above_average=np.zeros(len(x3_above_average_point))
z3_great_point=np.zeros(len(x3_great_point))


#font size
LARGE_FONT=("Verdana",9)



#Creating the Tkinter APP
class SignAnalyzer(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        container=tk.Frame(self)

        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames={}
        for F in (StartPage,PageOne,PageTwo):
            frame = F(container,self)
            self.frames[F]=frame
            frame.grid(row=0,column=0,sticky="nsew")
        
        self.show_frame(StartPage)

    def show_frame(self,cont):
        frame=self.frames[cont]
        frame.tkraise()



#Front page
class StartPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label=tk.Label(self,text="LiDAR point based Sign Analyser",font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        label1=tk.Label(self,text="Welcome to Sign Analyser, This tool is use to visualize signs and generate analysis of the signs captured by LiDAR points")
        label1.pack(pady=10,padx=10)
        
        
        #Button to populate histogram and the whole chart itself
        button2=ttk.Button(self,text="Plot Sign", 
        command=lambda: controller.show_frame(PageTwo))

        button2.pack()

        # lasso_button=ttk.Button(self,text='Go to Lasso Tool',command=lambda:controller.show_frame(PageThree))
        # lasso_button.pack()


class PageOne(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label=tk.Label(self,text="Bad Points on the sign",font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1=ttk.Button(self,text="Back Home", 
        command=lambda: controller.show_frame(StartPage))
        button1.pack()



#when user wants his points between certain ranges we can plot using this function
def updated_graph_points(df,value_title):

    print(len(df['Retro']))
    print(len(df['pX']))
    print(len(df['pY']))


    fig = plt.figure()
    ax_pop = fig.add_subplot(111, projection='3d')
    dx=0.03
    dy=0.03
    ax_pop.bar3d(df['pX'],df['pY'], 0, dx, dy, df['Retro'],color='b')
    plt.title('This contains all signs below {} marked in blue'.format(value_title))
    plt.show()

class SelectFromCollection(object):

    def __init__(self, ax, collection, alpha_other=0.3):
        self.canvas = ax.figure.canvas
        self.collection = collection
        self.alpha_other = alpha_other

        self.xys = collection.get_offsets()
        self.Npts = len(self.xys)

        # Ensure that we have separate colors for each object
        self.fc = collection.get_facecolors()
        if len(self.fc) == 0:
            raise ValueError('Collection must have a facecolor')
        elif len(self.fc) == 1:
            self.fc = np.tile(self.fc, (self.Npts, 1))

        self.lasso = LassoSelector(ax, onselect=self.onselect)
        self.ind = []

    def onselect(self, verts):
        path = Path(verts)
        self.ind = np.nonzero(path.contains_points(self.xys))[0]
        
        self.fc[:, -1] = self.alpha_other
        self.fc[self.ind, -1] = 1
        self.collection.set_facecolors(self.fc)
        self.canvas.draw_idle()

    def disconnect(self):
        self.lasso.disconnect_events()
        self.fc[:, -1] = 1
        self.collection.set_facecolors(self.fc)
        self.canvas.draw_idle()



class PageTwo(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent,relief='solid', bg='black')
        label=tk.Label(self,text="Visualizer",font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1=ttk.Button(self,text="Go back to Homepage", 
        command=lambda: controller.show_frame(StartPage))
        button1.pack()

        self.median_selected=0
        self.std_dev_selected=0

        self.fig = Figure(figsize=(5,5), dpi=100)

        self.fig_2d = Figure(figsize=(6,5),dpi=50)
    
        self.canvas=FigureCanvasTkAgg(self.fig,self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)

        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        # canvas._tkcanvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas_2d=FigureCanvasTkAgg(self.fig_2d,self)
        self.canvas_2d.draw()
        self.canvas_2d.get_tk_widget().pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas_2d, self)
        self.toolbar.update()
        self.canvas_2d._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        
        
        
        median=statistics.median(retro_master)
        standard_deviation=statistics.stdev(retro_master)

        self.color_code_3d_green=tk.Label(self,text="Green >0.61",bg='black',foreground='green')
        self.color_code_3d_green.pack(side='top', anchor='e')
        
        self.color_code_3d_purple=tk.Label(self,text="0.51<purple<0.60",bg='black',foreground='magenta')
        self.color_code_3d_purple.pack(side='top', anchor='e')

        median_label=tk.Label(self,text="Median of full Sign:{}".format(median),font=LARGE_FONT,bg='black',foreground="yellow")
        median_label.pack(side='bottom',pady=10,padx=10)
        if median>0.7:
            classification_status='Good Sign No change neeed'
        if median<0.69:
            classification_status='Poor Sign as per retro Standards, Please consided changing the sign'
        
        sd_label=tk.Label(self,text="Standard Deviation of full:{}".format(standard_deviation),font=LARGE_FONT,bg='black',foreground="yellow")
        sd_label.pack(side='bottom',pady=10,padx=10)

        classification_label=tk.Label(self,text="Classification Status {}".format(classification_status),font=LARGE_FONT,bg='black',foreground="yellow")
        classification_label.pack(side='bottom',pady=10,padx=10)

        self.ax1 = self.fig.add_subplot(111, projection='3d')
        self.ax2 = self.fig_2d.add_subplot(111)


        

        if len(x3_great_point)>0:
            #color the point green
            self.ax1.bar3d(x3_great_point, y3_great_point,z3_great_point, dx, dy, dz_great_point,color='g')
        else:
            pass
        if len(x3_average_point)>0:
            #color the point y
            self.ax1.bar3d(x3_average_point, y3_average_point,z3_average_point, dx, dy, dz_average_point,color='y')
        else:
            pass

        if len(x3_above_average_point)>0:
            #color the point orange
            self.ax1.bar3d(x3_above_average_point, y3_above_average_point, z3_above_average, dx, dy,dz_above_average_point ,color='m')
        else:
            pass

        if len(x3_very_poor)>0:
            #color the point orange
            self.ax1.bar3d(x3_very_poor, y3_very_poor, z3_very_poor, dx, dy,dz_very_poor,color='r')
        else:
            pass
        


        if(len(x3_great_point)>0):
            button3=ttk.Button(self,text="Only Good Points",
            command=lambda: [
            self.ax1.clear(),
            self.ax1.bar3d(x3_great_point, y3_great_point,z3_great_point, dx, dy, dz_great_point,color='g')
            ]
            ) 
            button3.pack(side='left', padx='5', pady='10')
        if(len(x3_very_poor)>0):
            button4=ttk.Button(self,text="Only Poor Points",
            command=lambda: [
            self.ax1.clear(),
            self.ax1.bar3d(x3_very_poor, y3_very_poor,z3_very_poor, dx, dy, dz_very_poor,color='r')
            ]
            ) 
            button4.pack(side='left', padx='5', pady='10')
        if(len(x3_above_average_point)>0):
            button5=ttk.Button(self,text="Only Above averge points",
            command=lambda: [
            self.ax1.clear(),
            self.ax1.bar3d(x3_above_average_point, y3_above_average_point,z3_above_average, dx, dy, dz_above_average_point,color='m')
            ]
            ) 
            button5.pack(side='left', padx='5', pady='10')
        if(len(x3_average_point)>0):
            button6=ttk.Button(self,text="Only average point",
            command=lambda: [
            self.ax1.clear(),
            self.ax1.bar3d(x3_average_point, y3_average_point,z3_average_point, dx, dy, dz_average_point,color='b')
            ]
            ) 
            button6.pack(side='left', padx='5', pady='10')
        if(len(retro_master)>0):
            print(len(retro_master))
            button7=ttk.Button(self,text="Histograms",
            command=lambda: [
        
            self.ax2.hist(dz_very_poor,bins,histtype='bar',color='r'),
            self.ax2.hist(dz_great_point,bins,histtype='bar',color='g'),
            self.ax2.hist(dz_average_point,bins,histtype='bar',color='y'),
            self.ax2.hist(dz_above_average_point,bins,histtype='bar',color='m')
            ]
            ) 
            button7.pack(side='left', padx='5', pady='10')
        a=0
        bin_value_to_show_points = tk.Entry(self)
        bin_value_to_show_points.pack(side='left', padx='5', pady='10')

        button_to_plot_entered_value=ttk.Button(self,text="Plot points below entered value", 
        command=lambda: [
        updated_graph_points(df1.loc[(df1['Retro'] <= float(bin_value_to_show_points.get()))],bin_value_to_show_points.get())
        
                        ]
        
        )
        button_to_plot_entered_value.pack(side='left', padx='5', pady='10')


        

        self.ax1.set_xlabel('x')
        self.ax1.set_ylabel('y')
        self.ax1.set_zlabel('retro')
        self.ax1.set_zlim3d(0,1)
        self.ax1.set_title("3D retro-color-plot")
        self.ax2.set_title("All Historgrams")
        self.subplot_kw = dict(xlim=(0, 1), ylim=(0, 1), autoscale_on=False)
        self.bins=[0,0.1,0.2,0.3,0.4,0.5,0.525,0.55,0.6,0.65,0.675,0.7,0.725,0.75,0.775,0.8,0.85,0.9,1]
        print(len(dz))

        #self.fig,self.ax = plt.subplots(subplot_kw=self.subplot_kw)
        
        self.fig_lasso=Figure(figsize=(5,4),dpi=100)
        
        self.canvas=FigureCanvasTkAgg(self.fig_lasso,self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)

        self.ax=self.fig_lasso.add_subplot(111)

        self.pts = self.ax.scatter(red_signs_x, red_signs_y, color='r',s=80)
        #white point selector
        self.pts_1 = self.ax.scatter(white_signs_x, white_signs_y, color='grey',s=80)
        #blue point selector
        self.pts_2 = self.ax.scatter(blue_signs_x, blue_signs_y, color='b',s=80)
        #green point selector
        self.pts_3 = self.ax.scatter(green_signs_x, green_signs_y, color='g',s=80)
        #yellow point selector
        self.pts_4 = self.ax.scatter(yellow_signs_x,yellow_signs_y, color='y',s=80)
        
        self.selector = SelectFromCollection(self.ax, self.pts)
        self.selector_1=SelectFromCollection(self.ax,self.pts_1)
        self.selector_2=SelectFromCollection(self.ax,self.pts_2)
        self.selector_3=SelectFromCollection(self.ax,self.pts_3)
        self.selector_4=SelectFromCollection(self.ax,self.pts_4)
        #self.fig.canvas.mpl_connect("key_press_event", self.accept())
        self.ax.set_title("Retro Polygon tool")
        #self.canvas.show()
        self.button_accept_points=ttk.Button(self,text="Finalized points", 
        command= self.enter_click)
        self.button_accept_points.pack(side='left', padx='5', pady='10')

    def enter_click(self):
        red_points_selected=[self.selector.xys[self.selector.ind]]
        white_points_selected=[self.selector_1.xys[self.selector_1.ind]]
        blue_points_selected=[self.selector_2.xys[self.selector_2.ind]]
        green_points_selected=[self.selector_3.xys[self.selector_3.ind]]
        yellow_points_selected=[self.selector_4.xys[self.selector_4.ind]]
        
        red_retro_points=[]
        white_retro_points=[]
        green_retro_points=[]
        yellow_retro_points=[]
        blue_retro_points=[]



        all_points_selected=[]

        for point in red_points_selected[0]:            
            row_red=df1.loc[(df1['pX'] == point[0]) & (df1['pY'] == point[1])]
            red_retro_points.append([int(row_red['SignId']),float(row_red['pX']),float(row_red['pY']),float(row_red['Retro'])])
        for point in white_points_selected[0]:
            row_white=(df1.loc[(df1['pX'] == point[0]) & (df1['pY'] == point[1])])
            white_retro_points.append([int(row_white['SignId']),float(row_white['pX']),float(row_white['pY']),float(row_white['Retro'])])

        for point in blue_points_selected[0]:     
            row_blue=df1.loc[(df1['pX'] == point[0]) & (df1['pY'] == point[1])]
            blue_retro_points.append([int(row_blue['SignId']),float(row_blue['pX']),float(row_blue['pY']),float(row_blue['Retro'])])

        for point in green_points_selected[0]:
            row_green=df1.loc[(df1['pX'] == point[0]) & (df1['pY'] == point[1])]
            green_retro_points.append([int(row_green['SignId']),float(row_green['pX']),float(row_green['pY']),float(row_green['Retro'])])

        for point in yellow_points_selected[0]:
            row_yellow=df1.loc[(df1['pX'] == point[0]) & (df1['pY'] == point[1])]
            yellow_retro_points.append([int(row_yellow['SignId']),float(row_yellow['pX']),float(row_yellow['pY']),float(row_yellow['Retro'])])
            

            
        df_white= pd.DataFrame(white_retro_points, columns=["SignId","pX","pY","Retro"])
        df_white.to_csv('../Data/white_retro_points.csv', index=True)

        df_red=pd.DataFrame(red_retro_points,columns=["SignId","pX","pY","Retro"])
        df_red.to_csv('../Data/red_retro_points.csv',index=True)


        df_blue=pd.DataFrame(blue_retro_points,columns=["SignId","pX","pY","Retro"])
        df_blue.to_csv('../Data/blue_retro_points.csv',index=True)

        df_green=pd.DataFrame(green_retro_points,columns=["SignId","pX","pY","Retro"])
        df_green.to_csv('../Data/green_retro_points.csv',index=True)

        df_yellow=pd.DataFrame(yellow_retro_points,columns=["SignId","pX","pY","Retro"])
        df_yellow.to_csv('../Data/yellow_retro_points.csv',index=True)


            
        print("[INFO] You have selected {} red and {} white points {} blue points {} green points".format(len(red_retro_points),len(white_retro_points),len(blue_retro_points),len(green_retro_points)))
        self.update_histograms_based_on_selected()   


    def update_histograms_based_on_selected(self):
        df_red_retro_selected=pd.read_csv('../Data/red_retro_points.csv')
        df_white_retro_selected=pd.read_csv('../Data/white_retro_points.csv')
        df_blue_retro_selected=pd.read_csv('../Data/blue_retro_points.csv')
        df_green_retro_selected=pd.read_csv('../Data/green_retro_points.csv')
        df_yellow_retro_selected=pd.read_csv('../Data/yellow_retro_points.csv')

        df_red_retro_selected = df_red_retro_selected[['SignId','pX','pY','Retro']]
        df_white_retro_selected=df_white_retro_selected[['SignId','pX','pY','Retro']]
        df_blue_retro_selected=df_blue_retro_selected[['SignId','pX','pY','Retro']]
        df_green_retro_selected=df_green_retro_selected[['SignId','pX','pY','Retro']]
        df_yellow_retro_selected=df_yellow_retro_selected[['SignId','pX','pY','Retro']]
        df_all_points=df1['Retro']

        self.ax2.clear()
        
        bins = [0,0.1,0.2,0.3,0.4,0.425,0.45,0.475,0.5,0.525,0.550,0.575,0.6,0.625,0.65,0.675,0.70,0.725,0.75,0.775,0.8,0.825,0.85,0.875,0.9,0.925,0.95,0.975,1]



        self.ax2.hist(df_all_points,bins,histtype='bar',color='b',rwidth=0.8)
        self.ax2.hist(df_white_retro_selected['Retro'], bins,histtype='bar',color='gray', rwidth=0.8)
        self.ax2.hist(df_red_retro_selected['Retro'], bins,histtype='bar',color='r',alpha=0.3, rwidth=0.8)
        self.ax2.hist(df_blue_retro_selected['Retro'], bins,histtype='bar',color='b',alpha=0.3, rwidth=0.8)
        self.ax2.hist(df_yellow_retro_selected['Retro'], bins,histtype='bar',color='y',alpha=0.3, rwidth=0.8)
        self.ax2.hist(df_green_retro_selected['Retro'], bins,histtype='bar',color='g',alpha=0.3, rwidth=0.8)


        

                
app=SignAnalyzer()
app.mainloop()

