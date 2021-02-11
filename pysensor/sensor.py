import socket
import time
import random
import json
import paho.mqtt.client as mqtt

UDP_IP = "zentrale"
server_address="mosquitto"
server_port=1883
UDP_PORT = 5005
value =0
sensordaten = {
	"id": 10,
	"name": "windsensor1",
	"value": 0 
}

print("starting wind sensor")

#MQTT callback connect
def on_connect(client, userdata, flags, rc):
    print("Connected with Result code: " +str(rc) )



#MQTT connect
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
connected = False
for _i in range(3):
    try:
        print(f"connect to mqtt broker at {server_address} on port {server_port}")
        mqttc.connect(server_address, server_port, 60)
        connected = True
        mqttc.loop_start()
        break
    except ConnectionRefusedError:
        print("Could not connect to mqtt broker. Try again in 10 seconds")
    time.sleep(10)
if not connected:
    print("Could not connect to mqtt broker. Aborting.")
    exit(1)

time.sleep(2)
while True:
    #MESSAGE = input()
    #if MESSAGE == '0':
    #   break
    diff = random.randint(-10, 10)
    if value > 100 and diff > 0:
        value = value/2
    elif (value - diff) > 0:
        value = value - diff
    sensordaten["value"]=int(value)
    #sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #sock.sendto((json.dumps(sensordaten,separators=(",", ":"))).encode(), (UDP_IP, UDP_PORT))
    print((sensordaten["value"]))
    mqttc.publish("smarthome/windsensor", json.dumps(sensordaten,separators=(",", ":")).encode())
    time.sleep(2)
    
