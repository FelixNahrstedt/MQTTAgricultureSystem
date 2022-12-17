import sys
import time
import paho.mqtt.client as paho

def paho_client():
    # CLIENT PAHO
    port = 1883
    broker = f'mqtt://192.168.199.161:{port}/'
    username = 'agricultureLove'
    password = 'se4gd'
    client_id = f'Solar_Client'
    client = paho.Client(client_id)
    client.username_pw_set(username, password)
    if client.connect("localhost",1883)!=0:
        print("Could not connect to MQTT Broker!")
        sys.exit(-1)
    else:
        print("connected")
    client.publish("Agriculture/solar",1)
    return client

def Nutrition_Actuator(npk_val):
    lastFeeding = 0
    if(npk_val<=40):
        lastFeeding+=5
    elif(npk_val<=35):
        lastFeeding+=8
    elif(npk_val<=30):
        lastFeeding+=10
    return lastFeeding

def Water_Actuator(humidity):
    lastWatering = 0
    if(humidity<=45):
        lastWatering+=10
    elif(humidity<=50):
        lastWatering+=4
    elif(humidity<=30):
        lastWatering+=20
    elif(humidity<=10):
        lastWatering+=30
    return lastWatering

def on_connect(client, userdata, flags, rc):
    # This will be called once the client connects
    # Subscribe here!
    client.subscribe("Agriculture/solar")
    client.subscribe("Agriculture/soil_moist")
    client.subscribe("Agriculture/npk_val")


def on_message(client, userdata, msg):
    data = msg.payload.decode("utf-8")
    if(str(msg.topic)=="Agriculture/solar"):
        print(float(data))
    elif(str(msg.topic)=="Agriculture/soil_moist"):
        if(data != "None"):
            Watering = Water_Actuator(float(data))
            client.publish("Agriculture/Water_Actuator",Watering)


    elif(str(msg.topic)=="Agriculture/npk_val"):
        if(data != "None"):
            Feeding = Nutrition_Actuator(float(data))
            client.publish("Agriculture/Nutrition_Actuator",Feeding)

    # For Activation of Nutrition Actuator
    #lastFeeding = Nutrition_Actuator(npk_val,lastFeeding)
    # For Activation of Water Actuator
    #lastWatering = Water_Actuator(soil_moist,lastWatering)


def main():
    global data
    username = 'agricultureLove'
    password = 'se4gd'
    client = paho.Client("solar_fetcher") # client ID "mqtt-test"
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username, password)
    client.connect('192.168.152.161', 1883)
    client.loop_forever() 
    #client.loop_forever()

    # For Activation of Nutrition Actuator
    #lastFeeding = Nutrition_Actuator(npk_val,lastFeeding)
    # For Activation of Water Actuator
    #lastWatering = Water_Actuator(soil_moist,lastWatering)
main()

 # Start networking daemon