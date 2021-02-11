from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift import Thrift
from smart_home_thrift import SmartHome

import socket
import json
import time
import sqlite3 
import signal
from datetime import datetime
import paho.mqtt.client as mqtt


transport = TSocket.TSocket('thriftserver', 9090)
# Buffering is critical. Raw sockets are very slow
transport = TTransport.TBufferedTransport(transport)
# Wrap in a protocol
protocol = TBinaryProtocol.TBinaryProtocol(transport)
# Create a client to use the protocol encoder
client = SmartHome.Client(protocol)


transport.open()
supportedVersion = client.checkVersion('1.1')
transport.close()

print ("starting zentio")
VERSION='1.1'
server_address = "mosquitto"
UDP_PORT = 5005
server_port = 1883

sensorIDs = [10, 11, 12, 99]
receivedPackets=0
conn = sqlite3.connect('./sqlite/sqlite.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS sensordata
             (id integer, name text, value integer, vtime timestamp)''')



def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " +str(rc))
    client.subscribe("smarthome/#",0)

def rpcDaily():
    for ID in sensorIDs:
        query= """
SELECT round(avg(value)) FROM(SELECT * FROM sensordata WHERE id=%d ORDER BY vtime DESC LIMIT 5);
"""%(ID)
        dailyData = c.execute(query).fetchone()
        conn.commit()
        transport.open()
        dailyData= dailyData[0]
        client.safeDailyValues(str(ID), int(dailyData))
        transport.close()




def on_message(client, userdata, msg):
    global receivedPackets

    try:
        sensordaten = json.loads(msg.payload)
        if sensordaten["id"] in sensorIDs:
            if sensordaten["id"] == 99: #Testfall
                receivedPackets += 1
                #print(receivedPackets)
                timestamp = int(round(time.time()*1000)) - int(sensordaten["timestamp"])
                print(timestamp)
            else:
                receivedPackets+=1
                date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                print (sensordaten["name"], ": ", sensordaten["value"])
                c.execute("INSERT INTO sensordata VALUES (%d,'%s',%d,'%s')" % (sensordaten["id"], sensordaten["name"], sensordaten["value"], date_time))
                conn.commit()
            #print(receivedPackets)
        else:
            print("ID nicht regestriert")
    except Exception as e:
        print(e)
    #RPC
    if supportedVersion and receivedPackets%15==0 and receivedPackets != 0:
        rpcDaily()
    
mqttc=mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
connected = False
for _i in range(3):
    try:
        print(f"connect to mqtt broker at {server_address} on port {server_port}")
        mqttc.connect(server_address, server_port, 60)
        connected = True
        mqttc.loop_forever()
        break
    except ConnectionRefusedError:
        print("Could not connect to mqtt broker. Try again in 10 seconds")
    time.sleep(10)
if not connected:
    print("Could not connect to mqtt broker. Aborting.")
    exit(1)
           


