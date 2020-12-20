import paho.mqtt.client as paho
import socket
import ssl
import json
import base64
from imutils import paths
from pyimagesearch import config
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

mqtt_topic = "/firedetection/image"

awshost = "aqx8tvt4tgo70-ats.iot.eu-west-2.amazonaws.com"      # Endpoint
    
awsport = 8883                                              # Port no.   
clientId = "ObjectPWA"                                     # Thing_Name
thingName = "ObjectPWA"                                    # Thing_Name
caPath = "./certificates/AmazonRootCA1.pem"                                      # Root_CA_Certificate_Name
certPath = "./certificates/a3199d5ead-certificate.pem.crt"                            # <Thing_Name>.cert.pem
keyPath = "./certificates/a3199d5ead-private.pem.key"                          # <Thing_Name>.private.key

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  # pass parameters

mqttc.connect(awshost, awsport, keepalive=60)               # connect to aws server               # connect to aws server

mqttc.loop_start()                                          # Start the loop

INTERVAL=10
count = 1
imagePaths = list(paths.list_images(config.OUTPUT_IMAGE_PATH))

def getBinaryImage(img):
    f= open(img,'rb')
    filecontent = f.read()
    byteArr = bytearray(filecontent)
    return byteArr

while True:
    for img in imagePaths:
        payloadmsg = getBinaryImage(img)
        if connflag == True:
            mqttc.publish(mqtt_topic, payloadmsg , qos=1)        # topic: temperature # Publishing Temperature values
            print(f"msg {count} sent") # Print sent temperature msg on console
            count += 1
            sleep(INTERVAL)
    
    
