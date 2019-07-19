import numpy as np

from matplotlib.widgets import LassoSelector
from matplotlib.path import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
plt.style.use('dark_background')
import statistics

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

def draw_histograms(all_selected):
    figure,ax_10=plt.subplots(1)
    ax_10.hist(all_selected,histtype='bar',color='green')
    plt.show()

all_selected=[]

if __name__ == '__main__':
    import matplotlib.pyplot as plt
   
    df1 = pd.read_csv('signs_13.csv')
    #create df with only required 
    df_sign = df1[['SignId','pX','pY','Retro','COLOR']]

    red_signs_x=[]
    red_signs_y=[]
    

    white_signs_x=[]
    white_signs_y=[]
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

    subplot_kw = dict(xlim=(0, 1), ylim=(0, 1), autoscale_on=False)
    bins=[0,0.1,0.2,0.3,0.4,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,1]
    print(len(dz))
    #print(dz)
    fig, ax = plt.subplots(subplot_kw=subplot_kw)
    fig2, ax2= plt.subplots(1)
    fig3,ax3=plt.subplots(1)
    
    
    ax2.hist(dz,bins,histtype='bar',color='w')
    pts = ax.scatter(red_signs_x, red_signs_y, color='r',s=80)
    pts_1 = ax.scatter(white_signs_x, white_signs_y, color='grey',s=80)
    selector = SelectFromCollection(ax, pts)
    selector_1=SelectFromCollection(ax,pts_1)
    
    def accept(event):
        if event.key == "enter":
            
            red_points_selected=[selector.xys[selector.ind]]
            white_points_selected=[selector_1.xys[selector_1.ind]]
            red_retro_points=[]
            white_retro_points=[]
            all_points_selected=[]

            for point in red_points_selected[0]:
                row_red=df_sign.loc[(df_sign['pX'] == point[0]) & (df_sign['pY'] == point[1])]
                red_retro_points.append(row_red['Retro'])
               
            for point in white_points_selected[0]:
                row_white=(df_sign.loc[(df_sign['pX'] == point[0]) & (df_sign['pY'] == point[1])])
                white_retro_points.append(row_white['Retro'])
            
            all_selected=red_retro_points+white_retro_points
            
            
            print("[INFO] You have selected {} red and {} white points".format(len(red_retro_points),len(white_retro_points)))
            print(len(all_selected))
            selector.disconnect()
            selector_1.disconnect()
            ax.set_title("")
            draw_histograms(all_selected)
            fig.canvas.draw()
            #fig2.canvas.draw()
            
            #draw_histograms(red_retro_points,white_retro_points)

    fig.canvas.mpl_connect("key_press_event", accept)
    ax.set_title("Retro Polygon tool")
   
    
    plt.show()

