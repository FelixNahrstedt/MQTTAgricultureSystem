## IOT AGRICULTURE

In our Software Architecture we majorly want to focus on having a clean outline of the system while still keeping enough functionality to make it reusable. The Technology food above presents not only the major technologies as an overview but also the connections between them. 
We have a large set of simulated sensors including Solar, Pressure, Temperature, Humidity, NPK, Soil Moisture and PH Sensors together with actuators for Water and Nutrition which are connected with the sensors through MQTT as well. 
The output values are being sent over a Paho-Client through MQTT (also using the MQTT Explorer) to a gateway where they are ordered and sent via API Connection to a deployed Cloud Server Endpoint. 
The server uses Node.js as a programming language together with libraries like mongoose or express.js to handle database connections easier. 
For database and visualisation purposes, we are using both mongoDB and InfluxDB - while focussing on the usage of Influx because of Influx’s possibilities for Visualisations on the admin side as well.

## Sensors

The Simulations are based on a kaggle dataset that includes weather and solar information for a particular time frame in Spain. We decided to use this database because it includes most of the sensor information that we needed for the simulation part. However, because our project is very dependent on soil values, some code had to be implemented to simulate a crop based scenario. 
These include not only both actuators (water and nutrition), that were used to get more fluctuation into the dataset to make it appear more realistic. The first of the self implemented simulated sensors is the N-P-K-Sensor. 
These three numbers form what is called the fertilizer's N-P-K ratio — the proportion of three plant nutrients in order: nitrogen (N), phosphorus (P) and potassium (K). The N-P-K numbers reflect each nutrient's percentage by weight. They are strongly based on the last time that nutrients have been added. Hence, the more time has passed since the last “feeding” of the plants - more nutrients need to be added by the actuators because of a lower NPK number. 
The ph value of the soil is also based on the nutrients in the soil. Because the npk value is generally in ppm with an optimum between 40 and 60 and a simulated minimum of 0 and maximum of 70, the following formula has been designed for simulating the ph with optimal value of 7 and slightly base or acidic probabilities as well: 
- ph = 0.05*npk+5
Regarding the soil moisture, it is (in a high level of abstraction) influenced by the temperature because of vaporisation, the air humidity that is sensed and the last time the water sensors have been activated. The humidity has been min-max normalised and randomly fluctuates because of different soil composition (random.uniform(0.8,0.9)).



The units for our simulation are as follows: 
Solar irradiance in percent (min-max normalised values out of a large kaggle dataset)
Pressure - converted from Pascal into Percentages
Temperature in °C 
Humidity of the air in Percentages
NPK values in parts per million (ppm)
Soil Moisture in percent
Ph values in the ph scale 
Nutrition Actuators in ppm
Water actuator in percent (just for simulation purposes)


