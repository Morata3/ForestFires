import paho.mqtt.client as paho
import socket
import ssl
import json
import map_module
from time import sleep
import conf
 
connflag = False
map_topic = "/firedetection/folium" 
image_topic = "/firedetection/image"
 
def on_connect(client, userdata, flags, rc):                # func for making connection
    global connflag
    print("Connected to AWS")
    connflag = True
    print("Connection returned result: " + str(rc) )


def on_message(client, userdata, msg):                      # Func for Sending msg
    print("New MQTT message", msg.topic)
    if msg.topic == map_topic:
        print(str(msg.payload))
        sensor_data = json.loads(str(msg.payload)[2:-1])
        map_module.updateMap(sensor_data)
        conf.map_version += 1
        print("**********MAP VERSION = "+str(conf.map_version))
    elif msg.topic == image_topic:
        f = open('detected_fire.jpg','wb')
        f.write(msg.payload)
        f.close()
        conf.image_version +=1
        return

def startMqttClient():
    mqttc = paho.Client()                                       # mqttc object
    mqttc.on_connect = on_connect                               # assign on_connect func
    mqttc.on_message = on_message  

    awshost = "aqx8tvt4tgo70-ats.iot.eu-west-2.amazonaws.com"      # Endpoint
    
    awsport = 8883                                              # Port no.   
    clientId = "ObjectPWA"                                     # Thing_Name
    thingName = "ObjectPWA"                                    # Thing_Name
    caPath = "./certificates/AmazonRootCA1.pem"                                      # Root_CA_Certificate_Name
    certPath = "./certificates/a3199d5ead-certificate.pem.crt"                            # <Thing_Name>.cert.pem
    keyPath = "./certificates/a3199d5ead-private.pem.key"                          # <Thing_Name>.private.key
    
    mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  # pass parameters
    
    mqttc.connect(awshost, awsport, keepalive=60)               # connect to aws server
    mqttc.subscribe(map_topic)
    mqttc.subscribe(image_topic)

    mqttc.loop_start()                                          # Start the loop

def startMqttClientLocal():
    mqttc = paho.Client()                                       # mqttc object
    mqttc.on_connect = on_connect                               # assign on_connect func
    mqttc.on_message = on_message  

    myhost = "localhost"
    mqttc.connect(myhost, keepalive=60)               # connect to aws server
    mqttc.subscribe(map_topic)
    mqttc.subscribe(image_topic)

    mqttc.loop_start()    

if __name__ == "__main__":
    startMqttClient()