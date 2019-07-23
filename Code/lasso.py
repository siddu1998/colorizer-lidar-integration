import numpy as np

from matplotlib.widgets import LassoSelector
from matplotlib.path import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
plt.style.use('dark_background')
import statistics
import csv

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

all_selected=[]

if __name__ == '__main__':
    import matplotlib.pyplot as plt
   
    df1 = pd.read_csv('../Data/signs.csv')
    #create df with only required 

    df1 = df1[['SignId','pX','pY','Retro','COLOR']]
    df1 = df1.groupby('SignId')
    df_sign = df1.get_group(int(input("Please enter sign for lasso analysis")))

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

    
    for i,row in df_sign.iterrows():
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

    subplot_kw = dict(xlim=(0, 1), ylim=(0, 1), autoscale_on=False)
    bins=[0,0.1,0.2,0.3,0.4,0.5,0.525,0.55,0.6,0.65,0.675,0.7,0.725,0.75,0.775,0.8,0.85,0.9,1]
    print(len(dz))

    fig, ax = plt.subplots(subplot_kw=subplot_kw)
    
    
    
    #red point selector
    pts = ax.scatter(red_signs_x, red_signs_y, color='r',s=80)
    #white point selector
    pts_1 = ax.scatter(white_signs_x, white_signs_y, color='grey',s=80)
    #blue point selector
    pts_2 = ax.scatter(blue_signs_x, blue_signs_y, color='b',s=80)
    #green point selector
    pts_3 = ax.scatter(green_signs_x, green_signs_y, color='g',s=80)
    #yellow point selector
    pts_4 = ax.scatter(yellow_signs_x,yellow_signs_y, color='y',s=80)
    
    selector = SelectFromCollection(ax, pts)
    selector_1=SelectFromCollection(ax,pts_1)
    selector_2=SelectFromCollection(ax,pts_2)
    selector_3=SelectFromCollection(ax,pts_3)
    selector_4=SelectFromCollection(ax,pts_4)

    
    def accept(event):
        if event.key == "enter":
            
            red_points_selected=[selector.xys[selector.ind]]
            
            white_points_selected=[selector_1.xys[selector_1.ind]]
            blue_points_selected=[selector_2.xys[selector_2.ind]]
            green_points_selected=[selector_3.xys[selector_3.ind]]
            yellow_points_selected=[selector_4.xys[selector_4.ind]]
            
            red_retro_points=[]
            white_retro_points=[]
            green_retro_points=[]
            yellow_retro_points=[]
            blue_retro_points=[]



            all_points_selected=[]

            for point in red_points_selected[0]:
                
                row_red=df_sign.loc[(df_sign['pX'] == point[0]) & (df_sign['pY'] == point[1])]
                print("---------------------")
                print(type(row_red['SignId']))
                print(int(row_red['SignId']))
                print(float(row_red['Retro']))
                print('-------------------')
                red_retro_points.append([int(row_red['SignId']),float(row_red['pX']),float(row_red['pY']),float(row_red['Retro'])])
               
            for point in white_points_selected[0]:
                row_white=(df_sign.loc[(df_sign['pX'] == point[0]) & (df_sign['pY'] == point[1])])
                white_retro_points.append([int(row_white['SignId']),float(row_white['pX']),float(row_white['pY']),float(row_white['Retro'])])
           
            for point in blue_points_selected[0]:     
                row_blue=df_sign.loc[(df_sign['pX'] == point[0]) & (df_sign['pY'] == point[1])]
                blue_retro_points.append([int(row_blue['SignId']),float(row_blue['pX']),float(row_blue['pY']),float(row_blue['Retro'])])

            for point in green_points_selected[0]:
                row_green=df_sign.loc[(df_sign['pX'] == point[0]) & (df_sign['pY'] == point[1])]
                green_retro_points.append([int(row_green['SignId']),float(row_green['pX']),float(row_green['pY']),float(row_green['Retro'])])

            for point in yellow_points_selected[0]:
                row_yellow=df_sign.loc[(df_sign['pX'] == point[0]) & (df_sign['pY'] == point[1])]
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
            print(len(all_selected))
            selector.disconnect()
            selector_1.disconnect()
            selector_2.disconnect()
            selector_3.disconnect()
            selector_4.disconnect()

            ax.set_title("")
            fig.canvas.draw()
    
    fig.canvas.mpl_connect("key_press_event", accept)
    ax.set_title("Retro Polygon tool")
   
    
    plt.show()

