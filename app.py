# Import the dependencies.
import numpy as np

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

#Variables here (Andrew comment)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
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
    return (
        "STILL TO DO"
    )

@app.route("/api/v1.0/stations")
def stations():
    return (
        "STILL TO DO"
    )

@app.route("/api/v1.0/tobs")
def tobs():
    return (
        "STILL TO DO"
    )

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
    app.run() 