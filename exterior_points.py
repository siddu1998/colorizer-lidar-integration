import pandas as pd
import numpy as np
import os, sys
import argparse
import math
from sklearn.cluster import KMeans, DBSCAN


def KMeansMethod(rows):
	pts = rows[["x_cart", "y_cart", "z_cart"]].values

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
def DBSCANMethod(rows):
	"""
	Uses the DBSCAN algorithm to cluster the points and remove outliers.

	Params:
	--------------
		rows: pandas dataframe containing the rows that belong to a particular sign

	Returns:
	--------------
		keep_rows: a subset of rows to keep

	"""
	pts = rows[["x_cart", "y_cart", "z_cart"]].values

	dbscan = DBSCAN(eps = DBSCAN_EPS, min_samples = HITCOUNT, metric = 'l1')
	dbscan.fit(pts)

	keep_indices = (dbscan.labels_ != -1) # noisy samples are labelled -1
	keep_rows = rows[keep_indices]

	return keep_rows

