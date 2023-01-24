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
    client.subscribe("Agriculture/watering")
    client.subscribe("Agriculture/feeding")

["temp","humidity","solar","ph","moist","npk","pressure","feeding","watering"] #add Val or Timestamp
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
    "feedingVal":None,
    "feedingTimestamp": None,
    "wateringVal":None,
    "wateringTimestamp": None
}

def on_message(client, userdata, msg):
    global json_thing
    data = msg.payload.decode("utf-8")
    [val,time1] = str(data).split(",")
    time1 = int(float(time1))

    if(str(msg.topic)=="Agriculture/solar"):
        myObj = {"solarVal": float(val), "solarTimestamp": time1}
        response = requests.post("https://iotsegd.herokuapp.com/persist/solar", json = myObj)
        print(f"{msg.topic}: {response.status_code}")
    elif(str(msg.topic)=="Agriculture/pressure"):
        myObj = {"pressureVal": float(val), "pressureTimestamp": time1}
        response = requests.post("https://iotsegd.herokuapp.com/persist/pressure", json = myObj)
        print(f"{msg.topic}: {response.status_code}")
    elif(str(msg.topic)=="Agriculture/temp"):
        myObj = {"tempVal": float(val), "tempTimestamp": time1}
        response = requests.post("https://iotsegd.herokuapp.com/persist/temperature", json = myObj)
        print(f"{msg.topic}: {response.status_code}")
    elif(str(msg.topic)=="Agriculture/humidity"):
        myObj = {"humidityVal": float(val), "humidityTimestamp": time1}
        response = requests.post("https://iotsegd.herokuapp.com/persist/humidity", json = myObj)
        print(f"{msg.topic}: {response.status_code}")
    elif(str(msg.topic)=="Agriculture/npk_val"):
        myObj = {"npkVal": float(val), "npkTimestamp": time1}
        response = requests.post("https://iotsegd.herokuapp.com/persist/npk", json = myObj)
        print(f"{msg.topic}: {response.status_code}")
    elif(str(msg.topic)=="Agriculture/soil_moist"):
        myObj = {"moistVal": float(val), "moistTimestamp": time1}
        response = requests.post("https://iotsegd.herokuapp.com/persist/moisture", json = myObj)
        print(f"{msg.topic}: {response.status_code}")
    elif(str(msg.topic)=="Agriculture/ph"):
        myObj = {"phVal": float(val), "phTimestamp": time1}
        response = requests.post("https://iotsegd.herokuapp.com/persist/ph", json = myObj)
        print(f"{msg.topic}: {response.status_code}")
    if(str(msg.topic)=="Agriculture/watering"):
        myObj = {"wateringVal": float(val), "wateringTimestamp": time1}
        response = requests.post("https://iotsegd.herokuapp.com/persist/watering", json = myObj)
        print(f"{msg.topic}: {response.status_code}")
    elif(str(msg.topic)=="Agriculture/feeding"):
        myObj = {"feedingVal": float(val), "feedingTimestamp": time1}
        response = requests.post("https://iotsegd.herokuapp.com/persist/feeding", json = myObj)
        print(f"{msg.topic}: {response.status_code}")
            
                

def main():
    global json_thing
    adress = "157.24.104.89"
    username = 'mosquittoBroker'
    password = 'se4gd'
    client = paho.Client("solar_fetcher") # client ID "mqtt-test"
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username, password)
    client.connect(adress, 1883)
    client.loop_forever() 
main()