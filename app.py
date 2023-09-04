# Import the dependencies.
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """List all available API routes."""
    return (
        f"<b>Hawaii Climate API - Module 10 Challenge</b> <br/>"
        f"-----------------------------------------<br/>"
        f"<i>Available routes:</i> <br/>"
        f"<br/>"
        f"To return a JSON dictionary of the last 12 months of precipitation data, use this path:<br/>"
        f"/api/v1.0/precipitation <br/>"
        f"<br/>"
        f"To return a JSON dictionary of all the stations included in the data set, use this path:<br/>"
        f"/api/v1.0/stations <br/>"
        f"<br/>"
        f"To return a JSON list of temperature observations for the previous year for the most-active station, use this path:<br/>"
        f"/api/v1.0/tobs <br/>"
        f"<br/>"
        f"The following paths will return the minimum, maximum, and average temperature over the given interval, \
            through the end of the dataset if a specified end-date is not included.<br/>"
        f"<br/>"
        f"/api/v1.0/start-date (Enter as format YYYY-MM-DD) <br/>"
        f"/api/v1.0/start-date/end-date (Enter as format YYYY-MM-DD/YYYY-MM-DD) <br/>"
        f"<br/>"
        f"<br/>"
        f"API by Andrew Prozorovsky"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a JSON dictionary of the last 12 months of precipitation data"""
    data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()

    session.close()

    prcp_year = []
    for date, prcp in data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["inches"] = prcp
        prcp_year.append(prcp_dict)

    return (jsonify(prcp_year))

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset"""
    data = session.query(Station.name, Station.station).all()

    session.close()
    
    all_stations = []
    for name, station in data:
        station_dict = {}
        station_dict["name"] = name
        station_dict["station"] = station
        all_stations.append(station_dict)

    return (jsonify(all_stations))

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of temperature observations for the previous year for the most-active station."""
    data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= one_year_ago).all()
    
    session.close()

    temp_data = []
    for date, temp in data:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["temperature"] = temp
        temp_dict["station"] = 'USC00519281'
        temp_data.append(temp_dict)
    
    return (jsonify(temp_data))

@app.route("/api/v1.0/<start>")
def temps_start(start):
    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range."""
    data = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    session.close()

    temp_data = []
    for min, max, avg in data:
        temp_dict = {}
        temp_dict["date start"] = start
        temp_dict["min temp"] = min
        temp_dict["max temp"] = max
        temp_dict["average temp"] = avg
        temp_data.append(temp_dict)

    return (jsonify(temp_data))

@app.route("/api/v1.0/<start>/<end>")
def temps_start_end(start, end):
    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range."""
    data = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    session.close()

    temp_data = []
    for min, max, avg in data:
        temp_dict = {}
        temp_dict["date start"] = start
        temp_dict["date end"] = end
        temp_dict["min temp"] = min
        temp_dict["max temp"] = max
        temp_dict["average temp"] = avg
        temp_data.append(temp_dict)

    return (jsonify(temp_data))

if __name__ == '__main__':
    app.run(debug=True) 

#END OF CODE

#QUESTIONS FOR LAS
# What does .all() do and why is it important for turning an object address into an array?
# What does the automapper do?
# Why can't I return an f string before the jsonified data? If I wanted to make the page look somewhat pretty?