import geopy
import pandas as pd
from geopy.geocoders import Nominatim, GoogleV3

aptDF = pd.read_csv('pghDogApts.csv', na_values = ['NA']) # change csv file to file to geocode
aptDF.head(5)

#google_locator = GoogleV3(api_key="AIzaSyB7NeqCj7vorkZjEESq-y62hXshEiEzdYg")
nominatim_locator = Nominatim(user_agent="dogHouse")

def geocode_address(address, geolocator):
    """Google Maps v3 API: https://developers.google.com/maps/documentation/geocoding/"""
    # https://stackoverflow.com/questions/27914648/geopy-catch-timeout-error
    try:
        location = geolocator.geocode(address, exactly_one=True, timeout=5)
    except GeocoderTimedOut as e:
        print("GeocoderTimedOut: geocode failed on input %s with message %s" % (address, e.msg))
    except AttributeError as e:
        print("AttributeError: geocode failed on input %s with message %s" % (address, e.msg))
    if location:
        address_geo = location.address
        latitude = location.latitude
        longitude = location.longitude
        return address_geo, latitude, longitude
    else:
        print("Geocoder couldn't geocode the following address: %s" % address)

geo_results = []
for index, row in aptDF.iterrows():
    try:
        result = geocode_address(row.loc['address'], nominatim_locator)
        d = {'index': index, 'address_geo': result[0], 'latitude': result[1], 'longitude': result[2]}
        if d['address_geo'] is not None:
            geo_results.append(d)
            print(d)
    except:
        print(row.loc['address'])
        continue

geo = pd.DataFrame(geo_results)
geo.head(5)
geo.shape
aptDF.shape
geo.set_index('index', inplace=True)
pghDogAptsGeocode = aptDF.merge(geo, how='inner', left_index=True, right_index=True)
pghDogAptsGeocode.to_csv('pghDogAptsGeocode.csv')

## dog parks
parksDF = pd.read_csv('pghDogParks.csv', na_values = ['NA']) # change csv file to file to geocode
parksDF.head(5)

parksDF.index

geo_results = []
for index, row in parksDF.iterrows():
    try:
        result = geocode_address(row.loc['address'], nominatim_locator)
        d = {'index': index, 'address_geo': result[0], 'latitude': result[1], 'longitude': result[2]}
        if d['address_geo'] is not None:
            geo_results.append(d)
            print(d)
    except:
        print(row.loc['name'])
        continue

geo = pd.DataFrame(geo_results)
geo.head(5)
geo.shape
parksDF.shape
geo.set_index('index', inplace=True)
pghDogParksGeocode = parksDF.merge(geo, how='inner', left_index=True, right_index=True)
pghDogParksGeocode.to_csv('pghDogParksGeocode.csv')


## dog restaurants
restaurantsDF = pd.read_csv('pghDogRestaurants.csv', na_values = ['NA']) # change csv file to file to geocode
restaurantsDF.head(5)
restaurantsDF.index

geo_results = []
for index, row in restaurantsDF.iterrows():
    try:
        result = geocode_address(row.loc['name']+', '+row.loc['city'], nominatim_locator)
        d = {'index': index, 'address_geo': result[0], 'latitude': result[1], 'longitude': result[2]}
        if d['address_geo'] is not None:
            geo_results.append(d)
            print(d)
    except:
        print(row.loc['name'])
        continue

geo = pd.DataFrame(geo_results)
geo.head(5)
geo.shape
restaurantsDF.shape
geo.set_index('index', inplace=True)
pghDogRestaurantsGeocode = restaurantsDF.merge(geo, how='inner', left_index=True, right_index=True)
pghDogRestaurantsGeocode.to_csv('pghDogRestaurantsGeocode.csv')


## dog services
servicesDF = pd.read_csv('pghDogServices.csv', na_values = ['NA']) # change csv file to file to geocode
servicesDF.head(5)
servicesDF.index

geo_results = []
for index, row in servicesDF.iterrows():
    try:
        result = geocode_address(row.loc['address'], nominatim_locator)
        d = {'index': index, 'address_geo': result[0], 'latitude': result[1], 'longitude': result[2]}
        if d['address_geo'] is not None:
            geo_results.append(d)
            print(d)
    except:
        print(row.loc['name'])
        continue

geo = pd.DataFrame(geo_results)
geo.head(5)
geo.shape
servicesDF.shape
geo.set_index('index', inplace=True)
pghDogServicesGeocode = servicesDF.merge(geo, how='inner', left_index=True, right_index=True)
pghDogServicesGeocode.to_csv('pghDogServicesGeocode.csv')
