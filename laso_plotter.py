import matplotlib.pyplot as plt
import pandas as pd






#load red-white color data
df_red_retro_selected=pd.read_csv('red_retro_points.csv')
df_white_retro_selected=pd.read_csv('white_retro_points.csv')

df_red_retro_selected = df_red_retro_selected[['SignId','pX','pY','Retro']]
df_white_retro_selected=df_white_retro_selected[['SignId','pX','pY','Retro']]



df_all_points=pd.read_csv('signs_4.csv')
df_all_points=df_all_points['Retro']

bins = [0,0.1,0.2,0.3,0.4,0.425,0.45,0.475,0.5,0.525,0.550,0.575,0.6,0.625,0.65,0.675,0.70,0.725,0.75,0.775,0.8,0.825,0.85,0.875,0.9,0.925,0.95,0.975,1]



plt.hist(df_all_points,bins,histtype='bar',color='b',rwidth=0.8)
plt.hist(df_white_retro_selected['Retro'], bins,histtype='bar',color='black', rwidth=0.8)
plt.hist(df_red_retro_selected['Retro'], bins,histtype='bar',color='r',alpha=0.3, rwidth=0.8)

plt.xlabel('x')
plt.ylabel('y')
plt.title('Spatial Distribution')

plt.show()
