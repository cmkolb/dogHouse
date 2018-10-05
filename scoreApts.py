import os
from pylab import *
from sklearn.neighbors.kde import KernelDensity
from sklearn.model_selection import GridSearchCV
from mpl_toolkits.basemap import Basemap
from math import pi
import numpy as np
import pandas as pd
import pickle
import psycopg2
from math import radians

filename = '/Users/chelseakolb/Box Sync/InsightProject/dogHouse/finalized_model_parks.sav'
parksKDEmodel = pickle.load(open(filename, 'rb'))

filename = '/Users/chelseakolb/Box Sync/InsightProject/dogHouse/finalized_model_restaurants.sav'
restaurantsKDEmodel = pickle.load(open(filename, 'rb'))

filename = '/Users/chelseakolb/Box Sync/InsightProject/dogHouse/finalized_model_services.sav'
servicesKDEmodel = pickle.load(open(filename, 'rb'))

dbname = 'dogApts_db'
username = 'chelseakolb'

# Connect to make queries using psycopg2
con = None
con = psycopg2.connect(database = dbname, user = username)

# query:
sql_query = """
SELECT * FROM apartment_table;
"""
apartments_data_from_sql = pd.read_sql_query(sql_query,con)
apartments_data_from_sql.head()
apartments_data_from_sql.shape

# convert to radians
apartments_data_from_sql['lat_rad'] = apartments_data_from_sql['latitude'].apply(lambda x: radians(x))
apartments_data_from_sql['long_rad'] = apartments_data_from_sql['longitude'].apply(lambda x: radians(x))

def calcParkScore(lat_rad, long_rad):
    eval_data = np.hstack([lat_rad, long_rad])
    eval_data = eval_data.reshape(1,-1)
    park_result = parksKDEmodel.score_samples(eval_data)
    return park_result

def calcRestaurantScore(lat_rad, long_rad):
    eval_data = np.hstack([lat_rad, long_rad])
    eval_data = eval_data.reshape(1,-1)
    restaurant_result = restaurantsKDEmodel.score_samples(eval_data)
    return restaurant_result

def calcServiceScore(lat_rad, long_rad):
    eval_data = np.hstack([lat_rad, long_rad])
    eval_data = eval_data.reshape(1,-1)
    service_result = servicesKDEmodel.score_samples(eval_data)
    return service_result

apartments_data_from_sql['parkScore'] = apartments_data_from_sql.apply(lambda x: calcParkScore(x['lat_rad'], x['long_rad']), axis=1)
apartments_data_from_sql['restaurantScore'] = apartments_data_from_sql.apply(lambda x: calcRestaurantScore(x['lat_rad'], x['long_rad']), axis=1)
apartments_data_from_sql['serviceScore'] = apartments_data_from_sql.apply(lambda x: calcServiceScore(x['lat_rad'], x['long_rad']), axis=1)

apartments_data_from_sql.head

max(apartments_data_from_sql['parkScore'])
min(apartments_data_from_sql['parkScore'])

max(apartments_data_from_sql['restaurantScore'])
min(apartments_data_from_sql['restaurantScore'])


def updateParkScore(parkScore, minParkScore, maxParkScore):
    z = (parkScore - minParkScore) / (maxParkScore - minParkScore) * 100
    newParkScore = int(z)
    return newParkScore

minParkScore = min(apartments_data_from_sql['parkScore'])
min(apartments_data_from_sql['parkScore'])
maxParkScore = max(apartments_data_from_sql['parkScore'])
max(apartments_data_from_sql['parkScore'])

def updateRestaurantScore(restaurantScore, minRestaurantScore, maxRestaurantScore):
    z = (restaurantScore - minRestaurantScore) / (maxRestaurantScore - minRestaurantScore) * 100
    newRestaurantScore = int(z)
    return newRestaurantScore

minRestaurantScore = min(apartments_data_from_sql['restaurantScore'])
maxRestaurantScore = max(apartments_data_from_sql['restaurantScore'])

def updateServiceScore(serviceScore, minServiceScore, maxServiceScore):
    z = (serviceScore - minServiceScore) / (maxServiceScore - minServiceScore) * 100
    newServiceScore = int(z)
    return newServiceScore

minServiceScore = min(apartments_data_from_sql['serviceScore'])
maxServiceScore = max(apartments_data_from_sql['serviceScore'])

apartments_data_from_sql['newParkScore'] = apartments_data_from_sql.apply(lambda x: updateParkScore(x['parkScore'], minParkScore, maxParkScore), axis=1)
apartments_data_from_sql['newRestaurantScore'] = apartments_data_from_sql.apply(lambda x: updateRestaurantScore(x['restaurantScore'], minRestaurantScore, maxRestaurantScore), axis=1)
apartments_data_from_sql['newServiceScore'] = apartments_data_from_sql.apply(lambda x: updateServiceScore(x['serviceScore'], minServiceScore, maxServiceScore), axis=1)

apartments_data_from_sql.head()
max(apartments_data_from_sql['newParkScore'])
min(apartments_data_from_sql['newParkScore'])
mean(apartments_data_from_sql['newParkScore'])
median(apartments_data_from_sql['newParkScore'])

max(apartments_data_from_sql['newRestaurantScore'])
min(apartments_data_from_sql['newRestaurantScore'])
mean(apartments_data_from_sql['newRestaurantScore'])
median(apartments_data_from_sql['newRestaurantScore'])

max(apartments_data_from_sql['newServiceScore'])
min(apartments_data_from_sql['newServiceScore'])
mean(apartments_data_from_sql['newServiceScore'])
median(apartments_data_from_sql['newServiceScore'])

apartments_data_from_sql.dtypes

list(apartments_data_from_sql)
apartments_data_from_sql = apartments_data_from_sql.drop(['index', 'Unnamed: 0', 'Unnamed: 0.1'], axis=1)
apartments_data_from_sql.to_csv('scoredApartments.csv')
