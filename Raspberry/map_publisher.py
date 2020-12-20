import paho.mqtt.client as paho
import socket
import ssl
import json
from time import sleep
 
connflag = False
 
def on_connect(client, userdata, flags, rc):                # func for making connection
    global connflag
    print("Connected to AWS")
    connflag = True
    print("Connection returned result: " + str(rc) )
 
def on_message(client, userdata, msg):                      # Func for Sending msg
    print(msg.topic+" "+str(msg.payload))
    

mqttc = paho.Client()                                       # mqttc object
mqttc.on_connect = on_connect                               # assign on_connect func
mqttc.on_message = on_message  

mqtt_topic = "/firedetection/folium" 
INTERVAL = 4
#data_file = "sensor_data.csv"

awshost = "aqx8tvt4tgo70-ats.iot.eu-west-2.amazonaws.com"      # Endpoint
    
awsport = 8883                                              # Port no.   
clientId = "ObjectPWA"                                     # Thing_Name
thingName = "ObjectPWA"                                    # Thing_Name
caPath = "./certificates/AmazonRootCA1.pem"                                      # Root_CA_Certificate_Name
certPath = "./certificates/a3199d5ead-certificate.pem.crt"                            # <Thing_Name>.cert.pem
keyPath = "./certificates/a3199d5ead-private.pem.key"                          # <Thing_Name>.private.key

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  # pass parameters

mqttc.connect(awshost, awsport, keepalive=60)               # connect to aws server               # connect to aws server


#mqttc.connect("localhost")
mqttc.loop_start()                                          # Start the loop

while True:
    with open('sensor_data.json') as json_file:
        json_data = json.load(json_file)

    for sensordata in json_data:
 
        if connflag == True:
            paylodmsg = json.dumps(sensordata)       
            mqttc.publish(mqtt_topic, paylodmsg , qos=0)        # topic: temperature # Publishing Temperature values
            print("msg sent: " ) # Print sent temperature msg on console

        else:
            print("waiting for connection...") 
        
        sleep(INTERVAL)