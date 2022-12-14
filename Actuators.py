import sys
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
    if client.connect("localhost",1883,60)!=0:
        print("Could not connect to MQTT Broker!")
        sys.exit(-1)
    else:
        print("connected")
    return client
    #client.disconnect()

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

def on_message(client, userdata, msg):
        payloar = msg.payload.decode()
        topic = msg.topic

def subscribe(client,topic):
    client.subscribe(topic)
    client.on_message = on_message


# For Activation of Nutrition Actuator
lastFeeding = Nutrition_Actuator(npk_val,lastFeeding)
# For Activation of Water Actuator
lastWatering = Water_Actuator(soil_moist,lastWatering)