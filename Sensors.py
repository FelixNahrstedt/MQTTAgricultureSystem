import random
import sys
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
from csv import writer
import paho.mqtt.client as paho

def solarEval():
    # 1000 ist unsere Grenze
    Threshhold = 1000
    energy_data = pd.read_csv("Data_set.csv")
    solar = energy_data["generation solar"]
    minMaxSolar = (solar - solar.min())/(solar.max()-solar.min())
    beta = 24*7*4*5
    alpha = 24+beta
    plt.plot(solar.index[beta:alpha], solar.values[beta:alpha])
    plt.title('title name')
    plt.xlabel('x_axis name')
    plt.ylabel('y_axis name')
    plt.show()

def Pressure():
    # 1000 ist unsere Grenze
    energy_data = pd.read_csv("Data_set.csv")
    pressure = energy_data["pressure"]
    minMaxSolar = (pressure - pressure.min())/(pressure.max()-pressure.min())
    beta = 24*7*4*3
    print("PRESSURE")
    print(pressure.min(),pressure.max())
    beta = 24*7*4*8
    alpha = 24*7+beta
    plt.plot(pressure.index[beta:alpha], pressure.values[beta:alpha])
    plt.title('title name')
    plt.xlabel('x_axis name')
    plt.ylabel('y_axis name')
    plt.show()

def get_solar_irr(lastVal):
    # 1000 ist unsere Grenze
    val = lastVal+1
    MIN = 750
    MAX = 5000
    energy_data = pd.read_csv("Data_set.csv")
    solar = energy_data["generation solar"]
    if(lastVal>=len(solar)-1):
        val = 0
    returnSol = solar[val]
    if(returnSol>=MAX):
        returnSol = MAX
    elif(returnSol<=MIN):
        returnSol = MIN
    returnSol = (returnSol-MIN)/(MAX-MIN)

    return [val,returnSol*100]

def get_humidity(lastVal):
    # 1000 ist unsere Grenze
    val = lastVal+1
    energy_data = pd.read_csv("Data_set.csv")
    humidity = energy_data["humidity"]
    if(lastVal>=len(humidity)-1):
        val = 0
    returnPress = humidity[val]
    returnPress = (returnPress-humidity.min())/(humidity.max()-humidity.min())

    return returnPress*100

def get_pressure(lastVal):
    # 1000 ist unsere Grenze
    val = lastVal+1
    energy_data = pd.read_csv("Data_set.csv")
    pressure = energy_data["pressure"]
    if(lastVal>=len(pressure)-1):
        val = 0
    returnPress = pressure[val]
    returnPress = (returnPress-pressure.min())/(pressure.max()-pressure.min())

    return returnPress*100

def get_temp(lastVal):
    # 1000 ist unsere Grenze
    val = lastVal+1
    energy_data = pd.read_csv("Data_set.csv")
    temp = energy_data["temp"] - 273.15
    if(lastVal>=len(temp)-1):
        val = 0
    returnPress = temp[val]
    return returnPress

def get_npks(lastFeeding):
    ppm = 60
    factor = 1
    if(lastFeeding>5):
        factor-=0.05
    if(lastFeeding>8):
        factor-=0.1
    if(lastFeeding>15):
        factor-=0.15
    if(lastFeeding>20):
        factor-=0.2
    if(lastFeeding>30):
        factor-=0.3
    if(lastFeeding>40):
        factor -= 0.175
    return ppm*factor

def get_soil_moist(val,Temp,lastWatering):
    heat = Temp/40
    hum_sensed = 0
    energy_data = pd.read_csv("Data_set.csv")
    humidity = energy_data["humidity"]
    val -= 5
    if(val<=0):
        hum_sensed = humidity[humidity.size+val]
    else:
        hum_sensed = humidity[val]
    #0-1
    returnHum = (hum_sensed-humidity.min())/(humidity.max()-humidity.min()) 

    if(lastWatering>5 and lastWatering<10):
        returnHum = returnHum*random.uniform(0.8,0.9)
    elif(lastWatering>10 and lastWatering<20):
        returnHum = returnHum*random.uniform(0.5,0.8)
    elif(lastWatering>20 and lastWatering<30):
        returnHum = returnHum*random.uniform(0.2,0.5)
    elif(lastWatering>30 and lastWatering<40):
        returnHum = returnHum*random.uniform(0.2,0.5)
    return (returnHum - 0.1*(heat))*100


def get_ph(npk_vals):
    # here between 5 and 8
    return 0.05*npk_vals+5

def Nutrition_Actuator(npk_val,lastFeeding):
    if(npk_val<=40):
        lastFeeding-=5
    elif(npk_val>=40 and npk_val<=50):
        lastFeeding-=2
    return lastFeeding

def Water_Actuator(humidity,lastWatering):
    
    if(humidity<=45 and lastWatering>10):
        lastWatering-=10
    elif(humidity<=50 and lastWatering>10):
        lastWatering-=4
    
    return lastWatering


# CLIENT PAHO
port = 1883
broker = f'mqtt://172.23.96.1:{port}/'
username = 'agricultureLove'
password = 'se4gd'
client_id = f'Solar_Client'
client = paho.Client(client_id)
client.username_pw_set(username, password)
if client.connect("localhost",1883,60)!=0:
    print("Could not connect to MQTT Broker!")
    sys.exit(-1)
else:
    print("connected")
client.publish("test/status","Hello World from paho", 0)
client.disconnect()



# Pressure()
# solarEval()
def main():
    val = random.randint(0,35000)
    i = 0
    lastFeeding = 40
    lastWatering = 10
    Solar,Pressure,Temp,Humidity,npk_val,ph,soil_moist = 0,0,0,0,0,0,0
    while(True):
        #time.sleep(1)
        [nextVal,Solar] = get_solar_irr(val)
        if(Solar>0.0):
            # Converted from Pascal to Percent
            Pressure = get_pressure(val)
            # in °C
            Temp = get_temp(val)
            # In Percent
            Humidity = get_humidity(val)
            # in ppm (40-60 is optimum)
            npk_val = get_npks(lastFeeding)
            # In Percent
            soil_moist = get_soil_moist(val,Temp,lastWatering)
            # In ph Scale
            ph = get_ph(npk_val)
            # For Activation of Nutrition Actuator
            lastFeeding = Nutrition_Actuator(npk_val,lastFeeding)
            # For Activation of Water Actuator
            lastWatering = Water_Actuator(soil_moist,lastWatering)
        lastFeeding+=1
        if(lastWatering<100):
            lastWatering+=1
        print(i)
        val = nextVal
        arr = [Solar,Pressure,Temp,Humidity,npk_val,ph,soil_moist,lastFeeding,lastWatering]
        i+=1
        # with open('sensor_data.csv', 'a',newline='') as f_object:
        #     # Pass this file object to csv.writer()
        #     # and get a writer object
        #     writer_object = writer(f_object)
        
        #     # Pass the list as an argument into
        #     # the writerow()
        #     writer_object.writerow(arr)
        
        #     # Close the file object
        #     f_object.close()



#main()

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

headers = ["Solar","Pressure","Temp","Humidity","npk_val","ph","soil_moist","lastFeeding","lastWatering"]

df = pd.read_csv('sensor_data.csv')
df.plot()
plt.show()