import serial.tools.list_ports
import paho.mqtt.client as mqttclient
import time
import json
import random

BROKER_ADDRESS = "thingsboard.cloud"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "xMvVEmhpVjVrDSJDWnyI"

print("here")

def setMode(value):
    global autoMode
    autoMode = value

def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")

def on_message(client, userdata, msg):
    print("topic: ", msg.topic, " message: ", str(msg.payload) )


def recv_message(client, userdata, message):
    # print("Received: ", message.payload.decode("utf-8"))
    jsonobj = json.loads(message.payload)
    keys = jsonobj.keys()
    print("Received: ", keys, " | ")
    for key in keys:
        print(key)
        if(key=="autoMode"):
            if(jsonobj[key] == True):
                setMode(True)
                cmd="OPTIMUSSSSSSSSSSSSSSSS"
            else:
                setMode(False)
                cmd="PRIMEEEEEEEEEEEEEEEEE"
        elif(key == "Fan1_state"):
            if(jsonobj[key] == True):
                #Bat quat 1
                cmd="Fan1:On"
            else:
                #Tat quat 1
                cmd="Fan1:Off"
        elif(key == "Fan2_state"):
            if(jsonobj[key] == True):
                #Bat quat 2
                cmd="Fan2:On"
            else:
                #Tat quat 2
                cmd="Fan2:Off"
        elif(key == "Led1_state"):
            if(jsonobj[key] == True):
                #Bat den 1
                cmd="Led1:On"
            else:
                #Tat den 1
                cmd="Led1:Off"
        elif(key == "Led2_state"):
            if(jsonobj[key] == True):
                #Bat den 2
                cmd="Led2:On"
            else:
                #Tat den 2
                cmd="Led2:Off"
        print("-------------------------", cmd, "-------------------------")



    
        

            
        
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


client = mqttclient.Client("Gateway_Thingsboard")
client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)

client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

client.on_subscribe = subscribed
client.on_message = recv_message

entry_dict = {
    "temperature": "",
    "humidity": "",
    "intensity": "",
}
control_dict = {
    "Led1_state": "",
    "Led2_state": "",
    "Fan1_state": "",
    "Fan2_state": "",
}
setMode(False)
print("INNIT", autoMode)
highTemp=0
while True:
    print("/------", autoMode, "------/")
    temp = random.randint(200,800)/10
    hum = random.randint(0,100)
    lux = random.randint(0,100)

    entry_dict["temperature"] = temp
    entry_dict["humidity"] = hum
    entry_dict["intensity"] = lux
    
    print(json.dumps(entry_dict))
    if(autoMode):
        #High Temperature -> turn on Fan
        if(temp > 40):
            highTemp+=1
            if(highTemp >= 3):
                control_dict["Fan1_state"] = True
            else:   
                control_dict["Fan1_state"] = False
                highTemp =0

        #Low Intensity -> turn on Led
        if(lux < 50):
            #turn on led1
            control_dict["Led1_state"] = True
        else:
            #turn off led1
            control_dict["Led1_state"] = False


    # Automatic in gateway
    client.publish("v1/devices/me/telemetry", json.dumps(entry_dict))
    client.publish("v1/devices/me/attributes", json.dumps(control_dict))

    print(temp, " | ", hum, "|", lux)

    time.sleep(5)