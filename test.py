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


bins=[0,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1]

#load data frame of sign TODO: get this from the user argument
df1 = pd.read_csv('signs_1.csv')
#create df with only required 
df_sign = df1[['SignId','pX','pY','Retro','COLOR']]




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

for i,row in df_sign.iterrows():
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

LARGE_FONT=("Verdana",12)

def DBSCANMethod(rows):
	pts = rows[["x_cart", "y_cart", "z_cart"]].values

	dbscan = DBSCAN(eps = DBSCAN_EPS, min_samples = HITCOUNT, metric = 'l1')
	dbscan.fit(pts)

	keep_indices = (dbscan.labels_ != -1) # noisy samples are labelled -1
	keep_rows = rows[keep_indices]

	return keep_rows



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
class PageTwo(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label=tk.Label(self,text="Visalizer",font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1=ttk.Button(self,text="Go back to Homepage", 
        command=lambda: controller.show_frame(StartPage))
        button1.pack()


        fig = Figure(figsize=(5,5), dpi=100)

        fig_2d = Figure(figsize=(1,1),dpi=100)
    
        canvas=FigureCanvasTkAgg(fig,self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        # canvas._tkcanvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        canvas_2d=FigureCanvasTkAgg(fig_2d,self)
        canvas_2d.draw()
        canvas_2d.get_tk_widget().pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        toolbar = NavigationToolbar2Tk(canvas_2d, self)
        toolbar.update()
        canvas_2d._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



        ax1 = fig.add_subplot(111, projection='3d')
        print(type(ax1))
        ax2 = fig_2d.add_subplot(111)
        print(type(ax2))

        if len(x3_great_point)>0:
            #color the point green
            ax1.bar3d(x3_great_point, y3_great_point,z3_great_point, dx, dy, dz_great_point,color='g',alpha=0.5)
        else:
            pass
        if len(x3_average_point)>0:
            #color the point y
            ax1.bar3d(x3_average_point, y3_average_point,z3_average_point, dx, dy, dz_average_point,color='y',alpha=0.5)
        else:
            pass

        if len(x3_above_average_point)>0:
            #color the point orange
            ax1.bar3d(x3_above_average_point, y3_above_average_point, z3_above_average, dx, dy,dz_above_average_point ,color='m',alpha=0.5)
        else:
            pass

        if len(x3_very_poor)>0:
            #color the point orange
            ax1.bar3d(x3_very_poor, y3_very_poor, z3_very_poor, dx, dy,dz_very_poor,color='r',alpha=0.5)
        else:
            pass
        


        if(len(x3_great_point)>0):
            button3=ttk.Button(self,text="Only Good Points",
            command=lambda: [
            ax1.clear(),
            ax1.bar3d(x3_great_point, y3_great_point,z3_great_point, dx, dy, dz_great_point,color='g',alpha=0.5)
            ]
            ) 
            button3.pack()
        if(len(x3_very_poor)>0):
            button4=ttk.Button(self,text="Only Poor Points",
            command=lambda: [
            ax1.clear(),
            ax1.bar3d(x3_very_poor, y3_very_poor,z3_very_poor, dx, dy, dz_very_poor,color='r',alpha=0.5)
            ]
            ) 
            button4.pack()
        if(len(x3_above_average_point)>0):
            button5=ttk.Button(self,text="Only Above averge points",
            command=lambda: [
            ax1.clear(),
            ax1.bar3d(x3_above_average_point, y3_above_average_point,z3_above_average, dx, dy, dz_above_average_point,color='m',alpha=0.5)
            ]
            ) 
            button5.pack()
        if(len(x3_average_point)>0):
            button6=ttk.Button(self,text="Only average point",
            command=lambda: [
            ax1.clear(),
            ax1.bar3d(x3_average_point, y3_average_point,z3_average_point, dx, dy, dz_average_point,color='b',alpha=0.5)
            ]
            ) 
            button6.pack()
        if(len(retro_master)>0):
            print(len(retro_master))
            button7=ttk.Button(self,text="Histograms",
            command=lambda: [
        
            ax2.hist(dz_very_poor,bins=bins,histtype='bar',color='r'),
            ax2.hist(dz_great_point,bins=bins,histtype='bar',color='g'),
            ax2.hist(dz_average_point,bins=bins,histtype='bar',color='y'),
            ax2.hist(dz_above_average_point,bins=bins,histtype='bar',color='m'),
            fig_2d.canvas.flush_events()
            ]
            ) 
            button7.pack()
        
        

        

        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        ax1.set_zlabel('retro')
        ax1.set_zlim3d(0,1)

                
app=SignAnalyzer()
app.mainloop()
