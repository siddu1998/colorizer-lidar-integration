"""
#####################################################################
Author		: Esther Ling (lingesther@gatech.edu)
Date        : June 2019
Summary     : Refines the associated signs from signFilter.py
#####################################################################

Description
---------------------------
Refines the output of signFilter.py, by performing the following:

4. Removes outliers:
	- KMEeansMethod: Estimates a centroid of the points representing the sign and points that fall beyond a radius RADIUS
	- DBSCAN: Algorithm labels outliers
5. Removes "signs" that have a hit count < HITCOUNT

Inputs
---------------------------
: path to csv file (output from signFilter.py)

Outputs
---------------------------
: csv file that has refined sign-associated lidar points. contains a 'flag' column, when set to True indicates a need for manual inspection

Example
---------------------------
run refineSign.py --signs "../../Data/i75_2018_output/signFilter_raw_nb/associatedSigns.csv" \
run refineSign.py --signs "../../Data/i75_2018_output/signFilter_raw_sb/associatedSigns.csv" \

References
---------------------------
1. "Critical Assessment of an Enhanced Traffic Sign Detection Method Using Mobile LIDAR and INS Technologies", C. Ai, Y.C Tsai, Journal of Transportation Engineering 2015, 141(5)

"""
import pandas as pd
import numpy as np
import os, sys
import argparse
import math
from sklearn.cluster import KMeans, DBSCAN
import navpy
"""
FILTER THRESHOLDS. ADJUSTABLE
"""
RADIUS = 3.5 # largest sign dimension is 108 inches (https://mutcd.fhwa.dot.gov/htm/2009/part2/part2b.htm), which is 2.74m
DBSCAN_EPS = 2.75 # the maximum distance between two samples for one to be considered in the neighbourhood of the other
HITCOUNT = 10
UPPER_BOUND_REMOVAL = 500

33.787	-84.406

LAT_REF=33.787
LON_REF=-84.406
ALT_REF=200


def KMeansMethod(rows):
	"""
	Estimates a centroid of the points representing the sign using the KMeans algorithm.
	After estimating the centroid, remove points that fall beyond a certain radius.

	Params:
	--------------
		rows: pandas dataframe containing the rows that belong to a particular sign

	Returns:
	--------------
		keep_rows: a subset of rows to keep

	"""
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


verbose=True

## Read file
df_sign = pd.read_csv("signs_4.csv")
df_save=pd.DataFrame(columns=df_sign.columns)

#this would have split the dataset into groups so all the data would be (sign_id:1,rows)(sign_id:2,rows)(sign_id:3,rows)
sign_groups = df_sign.groupby('SignId')
lon = df_sign["X"].values
lat = df_sign["Y"].values
alt = df_sign["Z"].values
cartesian = navpy.lla2ned(lat, lon, alt,
                    LAT_REF, LON_REF, ALT_REF,
                    latlon_unit='deg', alt_unit='m', model='wgs84')
df_sign['x_cart'] = cartesian[:, 0]
df_sign['y_cart'] = cartesian[:, 1]
df_sign['z_cart'] = cartesian[:, 2]



df_save['flag'] = [0 for i in range(len(df_save))]

df_save = pd.DataFrame(columns = df_sign.columns)
#now we want to iterate thru each group to remove spurious points
for (i,grp) in enumerate(sign_groups):
    #grp=[sign_id,rows_corresponding to the sign_id]
    sign_id = grp[0]
    rows = grp[1]

    keep_rows = KMeansMethod(rows)
    
    ## Filter by hitcount
    if len(keep_rows) >= HITCOUNT:
        if verbose:
            print("[INFO] Appended good sign")
        df_save = df_save.append(keep_rows)
    else:
        if verbose:
            print("[INFO] Removed bad 'sign' below HITCOUNT")

## Save output
df_save.to_csv("output.csv", index=False)
print("[INFO] Saved")
