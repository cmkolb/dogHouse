from pylab import *
from sklearn.neighbors.kde import KernelDensity
from matplotlib import path
import random
from mpl_toolkits.basemap import Basemap
import numpy as np
import pandas as pd
import pickle
import psycopg2
from math import pi
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import LeaveOneOut

dbname = 'dogApts_db'
username = 'chelseakolb'

# Connect to make queries using psycopg2
con = None
con = psycopg2.connect(database = dbname, user = username)

def pnpoly(x, y, xyverts):
    """
    Included code for this matplotlib method directly in file b/c some versions don't have it.
    inside = pnpoly(x, y, xyverts)
    Return 1 if x,y is inside the polygon, 0 otherwise.
    *xyverts*
        a sequence of x,y vertices.
    A point on the boundary may be treated as inside or outside.
    .. deprecated:: 1.2.0
        Use :meth:`~matplotlib.path.Path.contains_point` instead.
    """
    p = path.Path(xyverts)
    return p.contains_point([x, y])


def points_inside_poly(xypoints, xyverts):
    """
    Included code for this matplotlib method directly in file b/c some versions don't have it.
    mask = points_inside_poly(xypoints, xyverts)
    Returns a boolean ndarray, True for points inside the polygon.
    *xypoints*
        a sequence of N x,y pairs.
    *xyverts*
        sequence of x,y vertices of the polygon.
    A point on the boundary may be treated as inside or outside.
    .. deprecated:: 1.2.0
        Use :meth:`~matplotlib.path.Path.contains_points` instead.
    """
    p = path.Path(xyverts)
    return p.contains_points(xypoints)


def points_in_polys(points, polys):
    """
    This method masks off the water (where data will be unreliable).
    """
    result = []
    for i, poly in enumerate(polys):
        if i == 0:
            mask = points_inside_poly(points, poly)
        else:
            mask = mask | points_inside_poly(points, poly)
    return np.array(mask)

def developDensityModel(filename, name=None, title_string=None, min_lat=38, max_lat=42, min_lon=-82, max_lon=-78, res=.01):
    d = pd.read_csv(filename)
    if not (('latitude' in d.columns) and ('longitude' in d.columns)):
        raise Exception('Error: dataset must contain lat and lon')

    #Filter for events with locations.
    geolocated = d.dropna(subset = ['latitude', 'longitude'])
    idxs = (geolocated['latitude'] > min_lat) & (geolocated['latitude'] < max_lat)
    idxs = idxs & (geolocated['longitude'] > min_lon) & (geolocated['longitude'] < max_lon)
    geolocated = geolocated.loc[idxs]
    geolocated['lat_rad'] = geolocated.apply (lambda row: radians(row['latitude']),axis=1)
    geolocated['long_rad'] = geolocated.apply (lambda row: radians(row['longitude']),axis=1)
    print(geolocated.shape)

    #Fit the appropriate model: Kernel Density Estimation.
    print('Total number of points', len(geolocated))
    bandwidths = np.linspace(0., 1., 1000)

    grid = GridSearchCV(KernelDensity(kernel='gaussian', metric="haversine", algorithm="ball_tree"),
                    {'bandwidth': bandwidths},
                    cv=5)

    grid.fit(geolocated[['lat_rad', 'long_rad']])
    bandwidth = grid.best_params_

    model = KernelDensity(kernel='gaussian', metric="haversine", bandwidth = bandwidth["bandwidth"], algorithm="ball_tree").fit(geolocated[['lat_rad', 'long_rad']])
    ## save the model to disk
    filename = 'finalized_model_'+name+'.sav'
    pickle.dump(model, open(filename, 'wb'))
    return bandwidth

developDensityModel(filename="pghDogParksGeocode.csv", name='parks')
developDensityModel(filename="pghDogRestaurantsGeocode.csv", name='restaurants')
developDensityModel(filename="pghDogServicesGeocode.csv", name='services')
