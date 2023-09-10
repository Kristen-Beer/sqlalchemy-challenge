# Import the dependencies.
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

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



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return(
        f"Hawaii Climate App<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end<br/>"
        f"<p>'start' and 'end' date should be in the format YYYY-MM-DD'.</p>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Climate app precipitation page requested by server...")


    # --- create a session from Python to the database ---
    session = Session(engine)

    # --- query to retrieve all date and precipitation data ---
    prcp_data = session.query(measurement.date, measurement.prcp).all()

    # --- close session ---
    session.close()

    # --- convert query results to dictionary using date as the key and prcp as the value ---
    prcp_dict = {} 
    for date, prcp in prcp_data:
        prcp_dict[date] = prcp
    
    # Return the JSON representation of your dictionary.
    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():
    print("Climate app station data requested by server...")


    # --- create a session from Python to the database ---
    session = Session(engine)
    
    # --- perform a query to retrieve all the station data ---
    results = session.query(station.id, station.station, station.name).all()

    # --- close the session ---
    session.close()

    # --- create a list of dictionaries with station info using for loop---
    list_stations = []

    for st in results:
        station_dict = {}
        station_dict["id"] = st[0]
        station_dict["station"] = st[1]
        station_dict["name"] = st[2]

        list_stations.append(station_dict)

    # Return JSON list of stations from the dataset.
    return jsonify(list_stations)



@app.route("/api/v1.0/tobs")
def tobs():
    print("Climate app temp data requested by server...")

    # --- create a session from Python to the database ---
    session = Session(engine)

    # Query dates and temperature observations for the most active station for the last year of data.
    # --- identify the most active station ---
    most_active_station = session.query(measurement.station, func.count(measurement.station)).\
                                        order_by(func.count(measurement.station).desc()).\
                                        group_by(measurement.station).\
                                        first()[0]


    # --- identify the last date and calculate the start date (12 months from the last date) ---
    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    format_str = '%Y-%m-%d'
    last_dt = dt.datetime.strptime(last_date, format_str)
    date_oneyearago = last_dt - dt.timedelta(days=365)

    # --- build query for tobs with above conditions ---
    most_active_tobs = session.query(measurement.date, measurement.tobs).\
                                    filter((measurement.station == most_active_station)\
                                            & (measurement.date >= date_oneyearago)\
                                            & (measurement.date <= last_dt)).all()

    # --- close the session ---
    session.close()

    # Return a JSON list of temperature observations (TOBS) for the previous year.
    return jsonify(most_active_tobs)


@app.route("/api/v1.0/<start>")
def temps_from_start(start):
    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    print(f"Requested climate app daily normals from {start}...")

# --- create a function to calculate the daily normals given a certain start date (datetime object in the format "%Y-%m-%d") ---
def daily_normals(start_date):

    # --- create a session from Python to the database ---
    session = Session(engine)   

    sel = [measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]
    return session.query(*sel).filter(func.strftime("%Y-%m-%d", measurement.date) >= func.strftime("%Y-%m-%d", start_date)).group_by(measurement.date).all()

    # --- close the session ---
    session.close()

    try:
        # --- convert start date to datetime object for validating and errors ---
        start_date = dt.datetime.strptime(start, "%Y-%m-%d")

        # --- call the daily_normals function to calculate normals from the start date ---
        results = daily_normals(start_date)
        normals=[]

        # --- create a for loop to go through row and calculate daily normals ---
        for temp_date, tmin, tavg, tmax in results:

            # --- create an empty dictionary and store results for each row ---
            temps_dict = {}
            temps_dict["Date"] = temp_date
            temps_dict["T-Min"] = tmin
            temps_dict["T-Avg"] = tavg
            temps_dict["T-Max"] = tmax

            # --- append each result's dictionary to the normals list ---
            normals.append(temps_dict)

        # --- return the JSON list of normals ---
        return jsonify(normals)

    except ValueError:
        return "Please enter the start date in the format 'YYYY-MM-DD'"
    


@app.route("/api/v1.0/<start>/<end>")
def temps_between(start, end):
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

    print(f"Requested climate app daily normals from {start} to {end}...")

    # --- create a function to calculate the daily normals given certain start and end dates (datetime objects in the format "%Y-%m-%d") ---
    def daily_normals(start_date, end_date):

        # --- create a session from Python to the database ---
        session = Session(engine)   

        sel = [measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]
        return session.query(*sel).filter(func.strftime("%Y-%m-%d", measurement.date) >= func.strftime("%Y-%m-%d", start_date)).\
                                   filter(func.strftime("%Y-%m-%d", measurement.date) <= func.strftime("%Y-%m-%d", end_date)).\
                                    group_by(measurement.date).all()

        # --- close the session ---
        session.close()

    try:
        # --- convert the start date to a datetime object for validating and error handling ---
        start_date = dt.datetime.strptime(start, "%Y-%m-%d")
        end_date = dt.datetime.strptime(end, "%Y-%m-%d")

        # --- call the daily_normals function to calculate normals from the start date and save the result ---
        results = daily_normals(start_date, end_date)
        normals=[]

        # --- create a for loop to go through row and calculate daily normals ---
        for temp_date, tmin, tavg, tmax in results:

            # --- create an empty dictionary and store results for each row ---
            temps_dict = {}
            temps_dict["Date"] = temp_date
            temps_dict["T-Min"] = tmin
            temps_dict["T-Avg"] = tavg
            temps_dict["T-Max"] = tmax

            # --- append each result's dictionary to the normals list ---
            normals.append(temps_dict)

        # --- return the JSON list of normals ---
        return jsonify(normals)

    except ValueError:
        return "Please enter dates in the following order and format: 'start_date/end_date' i.e. 'YYYY-MM-DD'/'YYYY-MM-DD'"

if __name__ == "__main__":
    app.run(debug=True)
