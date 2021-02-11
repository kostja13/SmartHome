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
	"id": 99,
	"name": "test",
	"value": 0,
    "timestamp": 0 
}

print("starting test sensor")
time.sleep(2)


#MQTT--------------------------------------------------------------------

def on_connect(client, userdata, flags, rc):
    print("Connected with Result code: " +str(rc) )


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
           




while value<1000:
    #print(value)
    #time.sleep(1)
    value=value+1
    sensordaten["value"]=int(value)
    sensordaten["timestamp"] = int(round(time.time()*1000))
    #mqttc.publish("smarthome/test", "test",0)
    mqttc.publish("smarthome/test", json.dumps(sensordaten,separators=(",", ":")).encode())
time.sleep(60)




##UDP--------------------------------------------------------------------
##sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
##sock.sendto((json.dumps(sensordaten,separators=(",", ":"))).encode(), (UDP_IP, UDP_PORT))
##time.sleep(0.0005)
    
