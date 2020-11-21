
#%% Adding dependencies
import datetime as dt
import numpy as np
import pandas as pd

#%% Get the dependencies we need for SQLAlchemy, 
# which will help us access our data in the SQLite database
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#%%import the dependencies that we need for Flask
from flask import Flask, jsonify

#%% set up our database engine for the Flask application
#% allows us to access and query our SQLite database file
engine = create_engine("sqlite:///hawaii.sqlite")

#%%
Base = automap_base()

#%% Add the following code to reflect the database:
Base.prepare(engine, reflect=True)

#%% With the database reflected, we can save our references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#%% creating a session link from Python to our database
session = Session(engine)

###%% SETTING UP FLASK APP 
#%%
app = Flask(__name__)

#%% Defining the welcome route using the code below
@app.route("/")

#%%  When creating routes, we follow the naming convention /api/v1.0/ followed by the name of 
# the route. This convention signifies that this is version 1 of our application. 
# This line can be updated to support future versions of the app as well
def welcome():
	return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# %%
# Create the route for the percipitation analysis
@app.route("/api/v1.0/precipitation")
# Create the precipitation() function.
def precipitation():
    # Calculates the date one year ago from the most recent date in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Write a query to get the date and precipitation for the previous year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    # Use jsonify() to format our results into a JSON structured file.
    return jsonify(precip)

# %%
#Create the route for the stations
@app.route("/api/v1.0/stations")
# Create the stations() function.
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# %%
#Create the route for the tobs
@app.route("/api/v1.0/tobs")
#Create the tobs() function.
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# %%
# %%
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
# %%
