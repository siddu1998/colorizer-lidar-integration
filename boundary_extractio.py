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

RADIUS=3.5
DBSCAN_EPS=2.75
HITCOUNT=10
UPPER_BOUND_REMOVAL=500

def KMeansMethod(rows):
	pts = rows[["pX", "pY", "pZ"]].values

	## Kmeans to get centroid
	kmeans = KMeans(n_clusters = 1)
	kmeans.fit(pts)
	centroid = kmeans.cluster_centers_

	## Compute distance from all the points to the centroid
	dists = np.linalg.norm(pts - centroid, axis = 1)

	## Remove spurious points
	keep_indices = (dists < RADIUS)
	num_spurious_points = len(keep_indices) - sum(keep_indices)
	if num_spurious_points <= UPPER_BOUND_REMOVAL:
		keep_rows = rows[keep_indices]
		keep_rows['flag'] = [0 for i in range(len(keep_rows))]
		if num_spurious_points > 0:
			print("[INFO] Removed spurious %d points!" % num_spurious_points)
	else:
		## If there are many signs that are being removed; keep all the points and flag for manual inspection; perhaps the clustering has issues
		keep_rows = rows
		keep_rows['flag'] = [1 for i in range(len(keep_rows))]
	return keep_rows


df_sign = pd.read_csv("signs_1.csv")