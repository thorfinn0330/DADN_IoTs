import paho.mqtt.client as mqttclient
import json

BROKER_ADDRESS = "thingsboard.cloud"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "NxAIkfI1fXsyBy67KTcy"
entry_dict = {
    "amperage": "",
    "energy": "",
    "frequency": "",
    "power":"",
    "voltage":""
}
print("here")

def setMode(value):
    global autoMode
    autoMode = value

def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")

def on_message(client, userdata, msg):
    print("topic: ", msg.topic, " message: ", str(msg.payload) )


def recv_message(client, userdata, message):
    
    print(message)
   

    
        

            
        
    # if(jsonobj['autoMode'] == True):
    #     
    # elif(jsonobj['autoMode'] == False):
    #     autoMode = False
    #     print("!!!")
    # elif(jsonobj['Fan1_state'] == True):
    #     print("True")
    # elif(jsonobj['Fan1_state'] == False):
    #     print("False")

   
def connected(client, usedata, flags, rc):
    if rc == 0:
        client.subscribe("v1/devices/me/attributes")
        print("Connected to Thingsboard successfully")

    else:
        print("Connection is failed")
def Esend(client, i, e, f, p, v):

    entry_dict["amperage"] = i
    entry_dict["energy"] = e
    entry_dict["frequency"] = f
    entry_dict["power"] = p
    entry_dict["voltage"] = v
    
    message = json.dumps(entry_dict)
    print(message)
    client.publish("v1/devices/me/telemetry", message)
    return message


def energy_connect():
    client = mqttclient.Client("Gateway_Thingsboard")
    client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)

    client.on_connect = connected
    client.connect(BROKER_ADDRESS, 1883)
    return client

