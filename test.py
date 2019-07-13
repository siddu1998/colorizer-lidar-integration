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




LARGE_FONT=("Verdana",12)
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
def qf(param):
    print(param)
class StartPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label=tk.Label(self,text="GeorgiaTech LiDAR point based Sign Analyser",font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1=ttk.Button(self,text="Bad Points", 
        command=lambda: controller.show_frame(PageOne))

        button1.pack()
        button2=ttk.Button(self,text="Good Points", 
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
        label=tk.Label(self,text="Good Points",font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1=ttk.Button(self,text="Back Home", 
        command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2=ttk.Button(self,text="Bad Points", 
        command=lambda: controller.show_frame(PageOne))
        button2.pack()

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
            

        #length and width of each bar
        dx=0.03
        dy=0.03

        #heights of each point category
        z3_very_poor=np.zeros(len(x3_very_poor))
        z3_average_point=np.zeros(len(x3_average_point))
        z3_above_average=np.zeros(len(x3_above_average_point))
        z3_great_point=np.zeros(len(x3_great_point))

        fig = Figure(figsize=(2,2), dpi=75)
        canvas=FigureCanvasTkAgg(fig,self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



        ax1 = fig.add_subplot(111, projection='3d')

        if len(x3_great_point)>0:
            #color the point green
            ax1.bar3d(x3_great_point, y3_great_point,z3_great_point, dx, dy, dz_great_point,color=(0,1,0,0.6))
        else:
            pass
        if len(x3_average_point)>0:
            #color the point y
            ax1.bar3d(x3_average_point, y3_average_point,z3_average_point, dx, dy, dz_average_point,color='y')
        else:
            pass
        if len(x3_very_poor)>0:
            #color the point red
            ax1.bar3d(x3_very_poor, y3_very_poor, z3_very_poor, dx, dy, dz_very_poor,color='r')
        else:
            pass

        if len(x3_above_average_point)>0:
            #color the point orange
            ax1.bar3d(x3_above_average_point, y3_above_average_point, z3_above_average, dx, dy,dz_above_average_point ,color=(0.6,0.3,0.0,0.6))
        else:
            pass



        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        ax1.set_zlabel('retro')
        ax1.set_zlim3d(0,1)


                
app=SignAnalyzer()
app.mainloop()
