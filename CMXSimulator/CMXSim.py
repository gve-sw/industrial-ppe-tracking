import requests
import json
from random import uniform
from flask import Flask
import pymongo
from pymongo import MongoClient
import time


mongoAddr = "database:27017"

client = MongoClient(mongoAddr)
locationDB = client.locationDB
groupsTable = locationDB.groupsTable




def movementGenerator(name, zone, deviceId, destinationURL):
	
	notifications = 200

	x = 0
	y = 0

	while notifications > 1:
	
		x = round((x + uniform(-3, 3)), 2)
		y = round((y + uniform(-3, 3)), 2)


		data = {
			    "notifications": [
			        {
			            "notificationType": "movement",
			            "subscriptionName": name,
			            "eventId": 61172,
			            "locationMapHierarchy": zone,
			            "locationCoordinate": {
			                "x": x,
			                "y": y,
			                "z": 0,
			                "unit": "FEET"
			            },
			            "geoCoordinate": {
			                "latitude": -999,
			                "longitude": -999,
			                "unit": "DEGREES"
			            },
			            "confidenceFactor": 144,
			            "apMacAddress": "00:2b:01:00:0a:00",
			            "associated": True,
			            "username": "",
			            "ipAddress": [
			                "10.10.20.230"
			            ],
			            "ssid": "test",
			            "band": "IEEE_802_11_B",
			            "floorId": 723413320329068700,
			            "floorRefId": "Null",
			            "entity": "WIRELESS_CLIENTS",
			            "deviceId": deviceId,
			            "lastSeen": "2017-10-23T06:16:29.239+0100",
			            "moveDistanceInFt": 32.898212,
			            "timestamp": 1508735789239
			        }
			    ]
			}

		dataJSON = json.dumps(data)
		
		headers = {'content-type' : 'application/json'}
		response = requests.request("POST" , destinationURL , headers=headers , data=dataJSON)

		notifications = notifications - 1

		time.sleep(5)



def InOutGenerator(name, zone, deviceId, destinationURL):
	
	notifications = 50

	while notifications > 1:



		time.sleep(15)

		data = {
			    "notifications": [
			        {
			            "notificationType": "InOut",
			            "subscriptionName": name,
			            "eventId": 61172,
			            "locationMapHierarchy": zone,
			            "locationCoordinate": {
			                "x": 34,
			                "y": 27,
			                "z": 0,
			                "unit": "FEET"
			            },
			            "geoCoordinate": {
			                "latitude": -999,
			                "longitude": -999,
			                "unit": "DEGREES"
			            },
			            "confidenceFactor": 144,
			            "apMacAddress": "00:2b:01:00:0a:00",
			            "associated": True,
			            "username": "",
			            "ipAddress": [
			                "10.10.20.230"
			            ],
			            "ssid": "test",
			            "band": "IEEE_802_11_B",
			            "floorId": 723413320329068700,
			            "floorRefId": "Null",
			            "entity": "WIRELESS_CLIENTS",
			            "deviceId": deviceId,
			        }
			    ]
			}

		dataJSON = json.dumps(data)
		
		headers = {'content-type' : 'application/json'}
		response = requests.request("POST" , destinationURL , headers=headers , data=dataJSON)

		notifications  = notifications - 1

app = Flask(__name__)

@app.route('/inout',methods=['POST'])
def listener():
	#print ("I received something")
	data = groupsTable.find_one()
	InOutGenerator(data['name'] , data['zone'] , data['user1'] , data['destinationURL'])
	return "OK"


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True)

