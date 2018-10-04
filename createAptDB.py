from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2
import pandas as pd

# Define a database name & set  postgres username
dbname = 'dogApts_db'
username = 'chelseakolb'

## 'engine' is a connection to a database
## Here, we're using postgres, but sqlalchemy can connect to other things too.
engine = create_engine('postgres://%s@localhost/%s'%(username,dbname))
print(engine.url)

## create a database (if it doesn't exist)
if not database_exists(engine.url):
    create_database(engine.url)
print(database_exists(engine.url))

# read a database from CSV and load it into a pandas dataframe
apt_data = pd.read_csv('pghDogAptsGeocode.csv')
parks_data = pd.read_csv('pghDogParksGeocode.csv')
restaurants_data = pd.read_csv('pghDogRestaurantsGeocode.csv')
services_data = pd.read_csv('pghDogServicesGeocode.csv')

## insert data into database from Python
apt_data.to_sql('apartment_table', engine, if_exists='replace')
parks_data.to_sql('parks_table', engine, if_exists='replace')
restaurants_data.to_sql('restaurants_table', engine, if_exists='replace')
services_data.to_sql('services_table', engine, if_exists='replace')

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

sql_query = """
SELECT * FROM parks_table;
"""
parks_data_from_sql = pd.read_sql_query(sql_query,con)
parks_data_from_sql.head()
parks_data_from_sql.shape
