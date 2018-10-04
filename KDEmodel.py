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
from sklearn.cross_validation import LeaveOneOut

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


def calculateDensityScore(filenames, title_string = None, min_lat = 38, max_lat = 42, min_lon = -82, max_lon = -78, res = .001):
    frameFiles = pd.DataFrame()
    listFiles = []
    for file in filenames:
        df = pd.read_csv(file)
        listFiles.append(df)
    d = pd.concat(listFiles, ignore_index = True, sort = True)

    if not (('latitude' in d.columns) and ('longitude' in d.columns)):
        raise Exception('Error: dataset must contain lat and lon')

    #Filter for events with locations.
    geolocated = d.dropna(subset = ['latitude', 'longitude'])
    idxs = (geolocated['latitude'] > min_lat) & (geolocated['latitude'] < max_lat)
    idxs = idxs &  (geolocated['longitude'] > min_lon) & (geolocated['longitude'] < max_lon)
    geolocated = geolocated.loc[idxs]
    geolocated['lat_rad'] = geolocated.apply (lambda row: pi/180*row['latitude'],axis=1)
    geolocated['long_rad'] = geolocated.apply (lambda row: pi/180*row['longitude'],axis=1)
    print(geolocated.shape)

    #Fit the appropriate model: Kernel Density Estimation.
    print('Total number of points', len(geolocated))
    bandwidths = 10 ** np.linspace(-1, 1, 100)
    grid = GridSearchCV(KernelDensity(kernel='gaussian', metric="haversine", algorithm="ball_tree"),
                    {'bandwidth': bandwidths},
                    cv=LeaveOneOut(len(d)))
    model = grid.fit(geolocated[['lat_rad', 'long_rad']])

    #Create a grid of points at which to predict.
    x = np.arange(min_lat, max_lat, res)
    y = np.arange(min_lon, max_lon, res)
    X, Y = meshgrid(x, y)
    numel = len(X) * len(X[0, :])
    Z = np.zeros(X.shape)
    unraveled_x = X.reshape([numel, 1])
    unraveled_y = Y.reshape([numel, 1])
    data_to_eval = np.hstack([unraveled_x, unraveled_y])

    #Make predictions using appropriate model.
    density = np.exp(model.score_samples(data_to_eval))

    ## save the model to disk
    filename = 'finalized_model.sav'
    pickle.dump(model, open(filename, 'wb'))
    return density

filenames = ("pghDogParksGeocode.csv", "pghDogRestaurantsGeocode.csv", "pghDogServicesGeocode.csv")
densityScores = calculateDensityScore(filenames=filenames)
min(densityScores)
max(densityScores)
