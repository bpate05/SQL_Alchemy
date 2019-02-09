# import dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt
import time

# Database setup
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect database into python
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# reference to the measurement table
Measurement = Base.classes.measurement
Station = Base.classes.station

# create session from python to the DB
session = Session(engine)
# session_2 = Session(engine)

# measurement_results = session.query(Measurement.date, Measurement.prcp, Measurement.tobs).all()
# station_results = session.query(Station.station, Station.name).all()
# start_date_results = session.query(Measurement.date).filter(Measurement.date >= 2018-8-10)

# flask setup
app = Flask(__name__)

# Flask routes

# create welcome route
@app.route("/")
def welcome():
    return(
        f"Aloha!<br/>"
        f"Welcome to historical Hawaii weather data API!!!! <br/><br/><br/>"
        f"Available Routes: <br/><br/>"
        f"/api/v1.0/precipitation <br/>"
        f"--Shows all precipitation data<br/><br/>"
        f"/api/v1.0/stations <br/>"
        f"--Shows a list of all of the recording stations <br/><br/>"
        f"/api/v1.0/tobs <br/>"
        f"--Shows all temperature observations from the past year of data <br/><br/>"
        f"/api/v1.0/<start> <br/>"
        f"--Shows the temperature minimum, average, and maximum on and after the entered date <br/><br/>"
        f"/api/v1.0/<start>/<end> <br/>"
        f"--Shows the temperature minimun, average, and maximum between the two dates selected"
    )

# flask route for precipitation data
@app.route("/api/v1.0/precipitation")
def get_precipitation():
    results = session.query(Measurement.date, Measurement.prcp).all()
    prcp_data = []
    for data in results:
        prcp_dict = {}
        prcp_dict['Date'] = data.date
        prcp_dict['Precipitation']:data.prcp
        prcp_data.append(prcp_dict)
        session.commit()    
    return jsonify(prcp_data)


# flask route for list of stations
@app.route("/api/v1.0/stations")
def get_stations():
    results = session.query(Station.station, Station.name).all()
    station_list = []

    for data in results:
        station_dict= {}
        station_dict["Station_ID"]= data[0]
        station_dict["Station_Name"]= data[1]
        station_list.append(station_dict)
        session.commit()

    return jsonify(station_list)



# flask route for temperature data
@app.route("/api/v1.0/tobs")
def get_tobs():
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-8-23').order_by(Measurement.date).all()
    session.commit()
    temp_data = []

    for data in results:
        temp_dict = {}
        temp_dict["Date"]= data[0]
        temp_dict["Temperature"] = data[1]
        temp_data.append(temp_dict)
        session.commit()

    return jsonify(temp_data)



# flask route for temperature data greater than or equal to a given date
@app.route("/api/v1.0/<start>/")
def get_start_date(start):
    results = session.query(Measurement.date, func.avg(Measurement.tobs), func.max(Measurement.tobs),\
         func.min(Measurement.tobs)).filter(Measurement.date == start).all()

    temp_data = []
    for data in results:
        temp_dict = {}
        temp_dict["Date"] = data[0]
        temp_dict["Average Temperature"] = float(data[1])
        temp_dict["Max Temperature"] = float(data[2])
        temp_dict["Min Temperature"] = float(data[3])
        temp_data.append(temp_dict)
        session.commit()

    return jsonify(temp_data)

# # flask route for temperature data within a given period
@app.route("/api/v1.0/<start>/<end>")
def get_date_range(start, end):
    results = session.query(Measurement.date, func.avg(Measurement.tobs), func.max(Measurement.tobs),\
        func.min(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end).all()

    temp_data = []
    for data in results:
        temp_dict = {}
        temp_dict["Start Date"] = start
        temp_dict["End Date"] = end
        temp_dict["Average Temperature"] = float(data[1])
        temp_dict["Max Temperature"] = float(data[2])
        temp_dict["Min Temperature"] = float(data[3])
        temp_data.append(temp_dict)
        session.commit()

    return jsonify(temp_data)

if __name__ == '__main__':
    app.run(debug=True)