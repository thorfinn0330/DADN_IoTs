from sensors import *
from enery_meter import*
from water_meter import*
import time
import paho.mqtt.client as mqttclient
import json
import random

BROKER_ADDRESS = "thingsboard.cloud"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "8nx36nkj1djnq57qdu9k"
def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")

def on_message(client, userdata, msg):
    print("topic: ", msg.topic, " message: ", str(msg.payload) )


def recv_message(client, userdata, message):
    # print("Received: ", message.payload.decode("utf-8"))
    jsonobj = json.loads(message.payload)
    print(jsonobj)

    
        
   
def connected(client, usedata, flags, rc):
    if rc == 0:
        client.subscribe("v1/devices/me/telemetry")
        print("Connected to Thingsboard successfully")

    else:
        print("Connection is failed")


client = mqttclient.Client("Gateway_Thingsboard")
client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)

client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)

client.on_subscribe = subscribed
client.on_message = recv_message
# List of sensor scripts (replace with actual file names)
sensor_scripts = ["devices.py"]
control= {
    "Fan_1": "true",
    "Fan_2": "",
    "Led_1":"false",
    "Led_2":""
}

client_ss = sensors_connect()
client_enery = energy_connect()
client_water = water_connect()
# Run all sensor scripts
while True:
    temp = random.randint(100,200)/10
    hum = random.randint(0,100)
    lux = random.randint(0,100)
    
    Ssend(client_ss, temp, hum, lux)
    Esend(client_enery, 1.5+temp/10, temp*100, 50+temp/4, temp*100+hum, 220+temp/2)
    Wsend(client_water, temp/5, hum/30)
   
    time.sleep(10)

print("All sensor scripts executed.")