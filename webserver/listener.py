
from flask import Flask, request, session, redirect 
import requests
import json
import pymongo
from pymongo import MongoClient
import settings


mongoAddr = settings.mongoAddr

client = MongoClient(mongoAddr)

locationDB = client.locationDB
locationTable = locationDB.locationTable


app = Flask(__name__)


@app.route('/',methods=['POST'])
def listener():
	data = json.loads(request.data)
	print (data)
	locationTable.insert_one(data)
	return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)