from flask import Flask, render_template, request
import numpy as np
import googlemaps
import os
import pickle
from math import pi, radians

# filename = 'finalized_model_parks.sav'
# KDEmodel = pickle.load(open(filename, 'rb'))

filename = '/Users/chelseakolb/Box Sync/InsightProject/dogHouse/finalized_model_parks.sav'
parksKDEmodel = pickle.load(open(filename, 'rb'))

filename = '/Users/chelseakolb/Box Sync/InsightProject/dogHouse/finalized_model_restaurants.sav'
restaurantsKDEmodel = pickle.load(open(filename, 'rb'))

filename = '/Users/chelseakolb/Box Sync/InsightProject/dogHouse/finalized_model_services.sav'
servicesKDEmodel = pickle.load(open(filename, 'rb'))

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

f = open('/Users/chelseakolb/Box Sync/InsightProject/dogHouse/gmaps.key', 'r')
gkey = f.readline()

@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/output', methods=['GET', 'POST'])
def results(gkey=str(gkey)):
    # user_input
    user_input = request.args.get('ID')

    # convert address into the long, lat format
    gmaps = googlemaps.Client(key=gkey)
    geocode_result = gmaps.geocode(address=user_input, language='python')
    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']

    # convert to radians
    lat_rad = radians(lat)
    long_rad = radians(lng)
    eval_data = np.hstack([lat_rad, long_rad])
    eval_data = eval_data.reshape(1,-1)

    p = parksKDEmodel.score_samples(eval_data)
    pmin, pmax = (9.98162084, 10.74619642)
    p = (p - pmin) / (pmax - pmin) * 100
    park_result = int(p)

    r = restaurantsKDEmodel.score_samples(eval_data)
    rmin, rmax = (9.93675578, 11.31215909)
    r = (r - rmin) / (rmax - rmin) * 100
    restaurant_result = int(r)

    s = servicesKDEmodel.score_samples(eval_data)
    smin, smax = (10.15103269, 10.88248393)
    s = (s - smin) / (smax - smin) * 100
    service_result = int(s)

    # user_parkWeight = request.args.get('parksWeight')
    # user_restaurantWeight = request.args.get('restaurantsWeight')
    # user_servicesWeight = request.args.get('servicesWeight')

    return render_template("output.html", latcnt=lat, lngcnt=lng, the_result=park_result)


if __name__ == '__main__':
    app.run(debug=True)
