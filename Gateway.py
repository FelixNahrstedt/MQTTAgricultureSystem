import datetime
import sys
import time
import paho.mqtt.client as paho
import requests

def on_connect(client, userdata, flags, rc):
    # This will be called once the client connects
    client.subscribe("Agriculture/solar")
    client.subscribe("Agriculture/pressure")
    client.subscribe("Agriculture/temp")
    client.subscribe("Agriculture/humidity")
    client.subscribe("Agriculture/npk_val")
    client.subscribe("Agriculture/soil_moist")
    client.subscribe("Agriculture/ph")
    client.subscribe("Agriculture/Nutrition_Actuator")
    client.subscribe("Agriculture/Water_Actuator")
    client.subscribe("Agriculture/timeStamp")

["temp","humidity","solar","ph","moist","npk","pressure","lastfeeding","watering"] #add Val or Timestamp
json_thing = {
    "tempVal":None,
    "tempTimestamp": None,
    "humidityVal":None,
    "humidityTimestamp": None,
    "solarVal":None,
    "solarTimestamp": None,
    "phVal":None,
    "phTimestamp": None,
    "moistVal":None,
    "moistTimestamp": None,
    "npkVal":None,
    "npkTimestamp": None,
    "pressureVal":None,
    "pressureTimestamp": None,
    "lastfeeingVal":None,
    "lastfeedingTimestamp": None,
    "wateringVal":None,
    "wateringTimestamp": None
}

def on_message(client, userdata, msg):
    global json_thing
    data = msg.payload.decode("utf-8")
    [val,time1,time2] = str(data).split(",")

    if(str(msg.topic)=="Agriculture/solar"):
        myObj = {"solarVal": float(val), "solarTimestamp": time1+time2}
        response = requests.post("https://se4gdiot.herokuapp.com/persist/solar", json = myObj)
        print(f"{msg.topic}: {response.status_code}")
    elif(str(msg.topic)=="Agriculture/pressure"):
        myObj = {"pressureVal": float(val), "pressureTimestamp": time1+time2}
        response = requests.post("https://se4gdiot.herokuapp.com/persist/pressure", json = myObj)
        print(f"{msg.topic}: {response.status_code}")
    elif(str(msg.topic)=="Agriculture/temp"):
        myObj = {"tempVal": float(val), "tempTimestamp": time1+time2}
        response = requests.post("https://se4gdiot.herokuapp.com/persist/temperature", json = myObj)
        print(f"{msg.topic}: {response.status_code}")
    elif(str(msg.topic)=="Agriculture/humidity"):
        myObj = {"humidityVal": float(val), "humidityTimestamp": time1+time2}
        response = requests.post("https://se4gdiot.herokuapp.com/persist/humidity", json = myObj)
        print(f"{msg.topic}: {response.status_code}")
    elif(str(msg.topic)=="Agriculture/npk_val"):
        myObj = {"npkVal": float(val), "npkTimestamp": time1+time2}
        response = requests.post("https://se4gdiot.herokuapp.com/persist/npk", json = myObj)
        print(f"{msg.topic}: {response.status_code}")
    elif(str(msg.topic)=="Agriculture/soil_moist"):
        myObj = {"moistVal": float(val), "moistTimestamp": time1+time2}
        response = requests.post("https://se4gdiot.herokuapp.com/persist/moisture", json = myObj)
        print(f"{msg.topic}: {response.status_code}")
    elif(str(msg.topic)=="Agriculture/ph"):
        myObj = {"phVal": float(val), "phTimestamp": time1+time2}
        response = requests.post("https://se4gdiot.herokuapp.com/persist/ph", json = myObj)
        print(f"{msg.topic}: {response.status_code}")
    if(str(msg.topic)=="Agriculture/watering"):
        myObj = {"wateringValVal": float(val), "wateringValTimestamp": time1+time2}
        response = requests.post("https://se4gdiot.herokuapp.com/persist/watering", json = myObj)
        print(f"{msg.topic}: {response.status_code}")
    elif(str(msg.topic)=="Agriculture/feeding"):
        myObj = {"feedingVal": float(val), "feedingTimestamp": time1+time2}
        response = requests.post("https://se4gdiot.herokuapp.com/persist/feeding", json = myObj)
        print(f"{msg.topic}: {response.status_code}")
            
                

def main():
    global json_thing
    username = 'agricultureLove'
    password = 'se4gd'
    client = paho.Client("solar_fetcher") # client ID "mqtt-test"
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username, password)
    client.connect('192.168.152.161', 1883)
    client.loop_forever() 
main()