import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"

    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    date_max = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    query_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    sel = [Measurement.date, Measurement.prcp]
    year_data = session.query(*sel).filter(Measurement.date >= query_date)
    session.close()
    prcp_dict = {}
    for date, prcp in year_data:
        prcp_dict[date] = prcp
    return jsonify(prcp_dict)



@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(Station.station).all()

    session.close()
    stat = list(np.ravel('stations'))

    return jsonify(stat)

@app.route("/api/v1.0/tobs")
def stations():
    session = Session(engine)
    stuff2 = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count(Measurement.id).desc())
    active = stuff2.first()
    active_id = active[0]
    date_max = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    query_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    temps_active = session.query(Measurement.tobs).filter(Measurement.date >= query_date).filter(Measurement.station == active_id).all()
    temps = list(np.ravel('temps_active'))
    return jsonify(temps)


@app.route("/api/v1.0/<start>")


@app.route("/api/v1.0/<start>/<end>")
def start_end(start = None, end = None):
    session = Session(engine)

    if not end:
        temp_data = session.query(measurement.station, func.min(measurement.tobs),\
                func.max(measurement.tobs), func.avg(measurement.tobs)).\
                filter(measurement.date >= start).\
                group_by(measurement.station).all()

        all_temps = list(np.ravel(temp_data))

        return jsonify(all_temps)
    temp_data = session.query(measurement.station, func.min(measurement.tobs),\
                func.max(measurement.tobs), func.avg(measurement.tobs)).\
                filter(measurement.date >= start).\
                filter(measurement.date <= end).\
                group_by(measurement.station).all()

    session.close()

    all_temps = list(np.ravel(temp_data))

    return jsonify(all_temps)    

if __name__ == '__main__':
    app.run(debug=True)
