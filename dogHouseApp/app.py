from flask import Flask, render_template, request
import numpy as np
import googlemaps
import os
import pickle
from math import pi

filename = '/Users/chelseakolb/Box Sync/InsightProject/dogHouse/dogHouseApp/finalized_model.sav'
KDEmodel = pickle.load(open(filename, 'rb'))

app = Flask(__name__)

f = open('/Users/chelseakolb/Box Sync/InsightProject/dogHouse/dogHouseApp/gmaps_key.txt', 'r')
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
    lat_rad = lat*pi/180
    long_rad = lng*pi/180

    eval_data = np.hstack([lat_rad, long_rad])
    eval_data = eval_data.reshape(1,-1)
    z = KDEmodel.score(eval_data)
    the_result = int(z)

    return render_template("output.html", latcnt=lat, lngcnt=lng, the_result=the_result)


if __name__ == '__main__':
    app.run(debug=True)
