# Geodata-visualisation-and-distribution
In this project we use plotly, flask, kafka and USB-serial to display and manipulate geospatial data
*** ***
# obtaining_data.py
*** ***
In this project we aim to collect geospatial data form an external device ( in this project an arduino Mega ) connected with an USB-cabel. 
The data-package needs to be as small as possible, so we extrapolate the data.
To make the project scalable, we use the kafka broker on the local computer to distrubate the data.

*** ***
# app.py
*** ***
We use the kafka broker to get our data that we want to feed to plotly and leaflet. This data is displayed using the idex.html file.
We also use subsequent pages to push data to the javaScipt inside the index.html file.
The entire framework is supported by the flask library.
*** ***
# Note
*** ***
Index.html needs to be in the folder 'templates'. This map also needs to be in the same folder as app.py. Otherwise flask won't know where to find the html file.
