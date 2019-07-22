"""
################################################
Author : Sai Siddartha Maram    (msaisiddartha1@gmail.com)
Data   : July 2019
Summary: An application to visualize 3D LiDAR data and generate statistical insights about it and recommend the 
         apt replacement strategy
###############################################

Description 
-------------------
Filters signs based on the sign id and associates each LiDAR point with the corresponding normalized retro intensity values.
Then plots 3D bar charts and histograms and classifies each point broadly into 4 classes based on their retro-intensity values.
Post whicjh

"""




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


bins=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]

#load data frame of sign TODO: get this from the user argument
df1 = pd.read_csv('signs.csv')
#create df with only required 

df1 = df1[['SignId','pX','pY','Retro']]
df1 = df1.groupby('SignId')
df1 = df1.get_group(int(input("Please enter the sign you want to plot")))
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

LARGE_FONT=("Verdana",9)




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


class StartPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label=tk.Label(self,text="LiDAR point based Sign Analyser",font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        label1=tk.Label(self,text="Welcome to Sign Analyser, This tool is use to visualize signs and generate analysis of the signs captured by LiDAR points")
        label1.pack(pady=10,padx=10)
        
        
        
        button2=ttk.Button(self,text="Plot Sign", 
        command=lambda: controller.show_frame(PageTwo))

        button2.pack()

class PageOne(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label=tk.Label(self,text="Bad Points on the sign",font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1=ttk.Button(self,text="Back Home", 
        command=lambda: controller.show_frame(StartPage))
        button1.pack()

user_pX=[]
user_pY=[]
user_dZ=[]


def updated_graph_points(df):
    
    

    print(len(df['Retro']))
    print(len(df['pX']))
    print(len(df['pY']))
    fig = plt.figure()
    ax_pop = fig.add_subplot(111, projection='3d')
    dx=0.03
    dy=0.03
    ax_pop.bar3d(df['pX'],df['pY'], 0, dx, dy, df['Retro'])
    plt.show()



class PageTwo(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label=tk.Label(self,text="Visalizer",font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1=ttk.Button(self,text="Go back to Homepage", 
        command=lambda: controller.show_frame(StartPage))
        button1.pack()


        fig = Figure(figsize=(5,4), dpi=100)

        fig_2d = Figure(figsize=(6,1),dpi=50)
    
        canvas=FigureCanvasTkAgg(fig,self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)

        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        # canvas._tkcanvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        canvas_2d=FigureCanvasTkAgg(fig_2d,self)
        canvas_2d.draw()
        canvas_2d.get_tk_widget().pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        toolbar = NavigationToolbar2Tk(canvas_2d, self)
        toolbar.update()
        canvas_2d._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        
        
        
        median=statistics.median(retro_master)
        standard_deviation=statistics.stdev(retro_master)



        median_label=tk.Label(self,text="Median of full Sign:{}".format(median),font=LARGE_FONT)
        median_label.pack(pady=10,padx=10)
        if median>0.7:
            classification_status='Good Sign No change neeed'
        if median<0.69:
            classification_status='Poor Sign as per retro Standards, Please consided changing the sign'
        
        sd_label=tk.Label(self,text="Standard Deviation of full:{}".format(standard_deviation),font=LARGE_FONT)
        sd_label.pack(pady=10,padx=10)

        classification_label=tk.Label(self,text="Classification Status {}".format(classification_status),font=LARGE_FONT)
        classification_label.pack(pady=10,padx=10)

        ax1 = fig.add_subplot(111, projection='3d')
        print(type(ax1))
        ax2 = fig_2d.add_subplot(111)
        print(type(ax2))


        

        if len(x3_great_point)>0:
            #color the point green
            ax1.bar3d(x3_great_point, y3_great_point,z3_great_point, dx, dy, dz_great_point,color='g')
        else:
            pass
        if len(x3_average_point)>0:
            #color the point y
            ax1.bar3d(x3_average_point, y3_average_point,z3_average_point, dx, dy, dz_average_point,color='y')
        else:
            pass

        if len(x3_above_average_point)>0:
            #color the point orange
            ax1.bar3d(x3_above_average_point, y3_above_average_point, z3_above_average, dx, dy,dz_above_average_point ,color='m')
        else:
            pass

        if len(x3_very_poor)>0:
            #color the point orange
            ax1.bar3d(x3_very_poor, y3_very_poor, z3_very_poor, dx, dy,dz_very_poor,color='r')
        else:
            pass
        


        if(len(x3_great_point)>0):
            button3=ttk.Button(self,text="Only Good Points",
            command=lambda: [
            ax1.clear(),
            ax1.bar3d(x3_great_point, y3_great_point,z3_great_point, dx, dy, dz_great_point,color='g')
            ]
            ) 
            button3.pack()
        if(len(x3_very_poor)>0):
            button4=ttk.Button(self,text="Only Poor Points",
            command=lambda: [
            ax1.clear(),
            ax1.bar3d(x3_very_poor, y3_very_poor,z3_very_poor, dx, dy, dz_very_poor,color='r')
            ]
            ) 
            button4.pack()
        if(len(x3_above_average_point)>0):
            button5=ttk.Button(self,text="Only Above averge points",
            command=lambda: [
            ax1.clear(),
            ax1.bar3d(x3_above_average_point, y3_above_average_point,z3_above_average, dx, dy, dz_above_average_point,color='m')
            ]
            ) 
            button5.pack()
        if(len(x3_average_point)>0):
            button6=ttk.Button(self,text="Only average point",
            command=lambda: [
            ax1.clear(),
            ax1.bar3d(x3_average_point, y3_average_point,z3_average_point, dx, dy, dz_average_point,color='b')
            ]
            ) 
            button6.pack()
        if(len(retro_master)>0):
            print(len(retro_master))
            button7=ttk.Button(self,text="Histograms",
            command=lambda: [
        
            ax2.hist(dz_very_poor,bins,histtype='bar',color='r'),
            ax2.hist(dz_great_point,bins,histtype='bar',color='g'),
            ax2.hist(dz_average_point,bins,histtype='bar',color='y'),
            ax2.hist(dz_above_average_point,bins,histtype='bar',color='m')
            ]
            ) 
            button7.pack()
        a=0
        bin_value_to_show_points = tk.Entry(self)
        bin_value_to_show_points.pack()

        button_to_plot_entered_value=ttk.Button(self,text="Plot points below entered value", 
        command=lambda: [
        updated_graph_points(df1.loc[(df1['Retro'] <= float(bin_value_to_show_points.get()))])

                        ]
        
        )
        
        
        button_to_plot_entered_value.pack()

        

        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        ax1.set_zlabel('retro')
        ax1.set_zlim3d(0,1)

                
app=SignAnalyzer()
app.mainloop()
