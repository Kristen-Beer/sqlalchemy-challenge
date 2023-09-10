# sqlalchemy-challenge
Assignment:
    1. Climate Analysis
    2. Climate App

Breakdown:
-Analysis and charts found in climate_starter.ipynb
-data_files folder contains the 2 csv files containing the measurements and station info as well as the hawaii.sqlite database. 


Climate Analysis:
-The date 12 months prior to the last date were identified using the datetime library. Using these dates and null values, the precipitation values for the last year of data was used to plot the following graph:
![Precipitation graph](prcp.png)

-The lowest, highest, and average temperatures were calcuated using the most active station id from the previous query.
Lowest temp: 54.0
Highest temp: 85.0
Average temp: 71.66378066378067

-Temperature observations at the most active station for the last 12 months were plotted as the following histogram:
![Temperature histogram](Temp.png)

Climate App:
This web app was created using SQLalchemy and Flask API. The database can be queried for the following:

    -Precipitation
    -Station Identification information
    -Temperature observations for the last 12 months of data available
    -Daily normals from a start date onward
    -Daily normals between a start and end date


