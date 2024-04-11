import time
from tb_gateway_mqtt import TBDeviceMqttClient
import paho.mqtt.client as mqtt

# Thingsboard cloud env
ACCESS_TOKEN = "aW9G954Seh9qMXMLsbUj"
THINGSBOARD_SERVER = "thingsboard.cloud"
THINGSBOARD_PORT = 1883

# create a mqtt client thingsboard
global client_tb
client_tb = TBDeviceMqttClient(THINGSBOARD_SERVER, THINGSBOARD_PORT, ACCESS_TOKEN)
client_tb.connect()
# wait for connection
while not client_tb.is_connected():
    time.sleep(0.1)

#Set auto mode
def setMode(value):
    global autoMode
    autoMode = value
setMode(False)

# on_message function for send telemetry to thingsboard
def on_message(client, userdata, msg):
    print("topic: ", msg.topic, "message: ", str(msg.payload.decode("utf-8")))
    message = str(msg.payload.decode("utf-8"))
    message = message.split("/")
    telemetry = {
        "temperature": message[0],
        "humidity": message[1],
        "intensity": message[2],
        }
    # telemetry including temperature and humidity
    print(type(message[0]))

    client_tb.send_telemetry(telemetry)

    if(autoMode):



# callback function for led status
def callback_led1(result, _):
    status = result["Led1_state"]
    client_pc.publish("control/led/1", status)
def callback_led2(result, _):
    status = result["Led2_state"]
    client_pc.publish("control/led/2", status)
def callback_fan1(result, _):
    status = result["Fan1_state"]
    client_pc.publish("control/fan/1", status)
def callback_fan2(result, _):
    status = result["Fan2_state"]
    client_pc.publish("control/fan/2", status)


def callback_autoMode(result, _):
    if result["autoMode"] == b'True':
        client_tb.clean_device_sub_dict()
        setMode(True)
    else:
        setMode(False)
        # subscribe to control topic
        client_tb.subscribe_to_attribute("Led1_state", callback_led1)
        client_tb.subscribe_to_attribute("Led2_state", callback_led2)
        client_tb.subscribe_to_attribute("Fan1_state", callback_fan1)
        client_tb.subscribe_to_attribute("Fan2_state", callback_fan2)


# other ...


# main function
if __name__ == "__main__":
    # create a mqtt client for pc
    client_pc = mqtt.Client()
    # broker_address = "192.168.137.57"
    broker_address = "10.42.0.1"
    port = 1883
    client_pc.connect(broker_address, port)
    client_pc.on_message = on_message
    # subscribe to sensor/dht22 topic
    client_pc.subscribe("sensor/dht22")


    # subscribe to control topic
    client_tb.subscribe_to_attribute("Led1_state", callback_led1)
    client_tb.subscribe_to_attribute("Led2_state", callback_led2)
    client_tb.subscribe_to_attribute("Fan1_state", callback_fan1)
    client_tb.subscribe_to_attribute("Fan2_state", callback_fan2)

    client_tb.subscribe_to_attribute("autoMode", callback_autoMode)

    # loop forever
    client_pc.loop_forever()
