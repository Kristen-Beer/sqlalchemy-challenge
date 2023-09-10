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
        f"<p>'start' and 'end' date should be in the format MMDDYYYY.</p>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Climate app precipitation page requested by server...")


    # --- create a session from Python to the database ---
    session = Session(engine)

    # --- query to retrieve all date and precipitation data ---
    prcp_data = session.query(measurement.date, measurement.prcp).all()

    # --- close the session ---
    session.close()

    # --- convert the query results to a dictionary using date as the key and prcp as the value ---
    prcp_dict = {} 
    for date, prcp in prcp_data:
        prcp_dict[date] = prcp
    
    # Return the JSON representation of your dictionary.
    return jsonify(prcp_dict)

