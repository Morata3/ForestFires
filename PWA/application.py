import ssl
import mqtt_subscriber as Mqtt
from flask import Flask, render_template, Response, request, jsonify
import json
import conf
import base64
import sys

def create_app():
    application = Flask(__name__)
    return application

application = create_app()

application.config['TEMPLATES_AUTO_RELOAD'] = True

Mqtt.startMqttClient()

def getB64Image():
    img_path='detected_fire.jpg'
    f = open(img_path,'rb')
    img_base64 = base64.b64encode(f.read())
    return img_base64

@application.route('/image', methods = ['GET'])
def getImage():
    current_v = conf.image_version
    v = request.args.get('v', type=int)
    print("Current image version: ", current_v, ", request version: ", v)
    if v != current_v:
        image = getB64Image()
        print("GET /image with version ", v, " replying with version ",current_v)
        return jsonify({'image': str(image)[2:-1], 'version': current_v})
    else:
        print("GET /image error: ",v," already latest version")
        return jsonify({"error": "Already latest version"}),500


@application.route('/folium', methods = ['GET'])
def getFoliumMap():
    current_v = conf.map_version
    v = request.args.get('v', type=int)
    print("Current map version: ", current_v)
    if v != current_v:
        print("GET Request with version ", v, " replying with version ",current_v)
        folium_html = render_template('/dist/folium_map.html')
        return jsonify({'html': folium_html, 'version': current_v})
    else:
        print("GET Request error: ",v," already latest version")
        return jsonify({"error": "Already latest version"})


@application.route('/dist/<file>')
def dist(file):
    return render_template('/dist/'+file)

@application.route('/cache/<file>')
def cache(file):
    return render_template('/cache/'+file)

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/offline.html')
def offline():
    return application.send_static_file('offline.html')


@application.route('/service-worker.js')
def sw():
    return application.send_static_file('service-worker.js')


if __name__ == '__main__':
    application.run(debug=True)
