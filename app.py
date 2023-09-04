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

recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
active_stations = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()
most_active_station = active_stations[0][0]

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """List all available API routes."""
    return (
        f"Hawaii Climate API - Module 10 Challenge <br/>"
        f"-----------------------------------------<br/>"
        f"Available routes: <br/>"
        f"<br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/start-date <br/>"
        f"/api/v1.0/start-date/end-date <br/>"
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
    data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= one_year_ago).\
    filter(Measurement.station == most_active_station).all()
    
    session.close()

    temp_data = []
    for date, temp in data:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["temperature"] = temp
        temp_dict["station"] = most_active_station
        temp_data.append(temp_dict)
    
    return (jsonify(temp_data))

@app.route("/api/v1.0/<start>")
def start():
    return (
        "STILL TO DO"
    )

@app.route("/api/v1.0/<start>/<end>")
def start_end():
    return (
        "STILL TO DO"
    )

if __name__ == '__main__':
    app.run(debug=True) 


#QUESTIONS FOR LAS
# What does .all() do and why is it important for turning an object address into an array?
# What does the automapper do?