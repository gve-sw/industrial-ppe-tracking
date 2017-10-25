from flask import Flask, render_template, request, session, redirect 
from flask_wtf import Form
from wtforms import RadioField, SelectField
import requests
import json
import pymongo
from pymongo import MongoClient
import settings

#Requirement for WTForms. Only used for dev. 
SECRET_KEY = 'development'

#location of MongoDB
mongoAddr = settings.mongoAddr

#Address of ngrok tunnel for Dev. Used as destination for CMX notifications
ngrokTunnel = settings.ngrokTunnel

#initialise the MongoDB tables
client = MongoClient(mongoAddr)
locationDB = client.locationDB
locationTable = locationDB.locationTable
groupsTable = locationDB.groupsTable

#Find out what zones are predefined in CMX. Will be used to populate Web form
zones = requests.request("GET", "http://cmxlocationsandbox.cisco.com/api/config/v1/zoneCountParams/1", auth=('learning','learning'))
zonesFormat = json.loads(zones.text)
zoneNames = zonesFormat['zoneDetails']
zoneList = []

#MAC Hardcoded while testing - will eventually be pulled from CMX / App
mac1 = '00:00:2a:01:00:40'
mac2 = '00:00:2a:01:00:3e'
mac3 = '00:00:2a:01:00:15'
mac4 = '00:00:2a:01:00:08'
mac5 = '00:00:2a:01:00:09'
mac6 = '00:00:2a:01:00:0a'


#Function to create a push service from CMX. 
def createNotification(zone, macAddress):
    #Data for creating notification. Note at the moment getting error from CMX - further troubleshooting required
    cmxData = {
        "name": "MovementClient",
        "userId": "learning",
        "rules": [
            {
                "conditions": [
                    {
                        "condition": "movement.distance > 2"
                    },
                    {
                        "condition": "movement.hierarchy == " + zone
                    },
                    {
                        "condition": "movement.macAddressList == "+macAddress+";"
                    }
                ]
            }
        ],
        "subscribers": [
            {
                "receivers": [
                    {
                        "uri": ngrokTunnel,
                        "messageFormat": "JSON",
                        "qos": "AT_MOST_ONCE"
                    }
                ]
            }
        ],
        "enabled": True,
        "enableMacScrambling": False,
        "macScramblingSalt": "",
        "notificationType": "Movement"
    }

    cmxJSON = json.dumps(cmxData)

    try:
        print ('Im about to do something')

        response = requests.request("PUT" , "http://cmxlocationsandbox.cisco.com/api/config/v1/notification" , auth=('learning','learning') , data = cmxJSON , verify=False )
        status_code = response.status_code
        print (status_code)
        if (status_code == 201):
            return 'OK'
        else:
            response.raise_for_status()
            print("Error occured in POST -->"+(response.text))
    except requests.exceptions.HTTPError as err:
        print ("Error in connection -->"+str(err))
    finally:
        if response : response.close()

# Used to get location of any tracked client from CMX using Mac Address
def GetLocation(macAddress):
    try:
        response = requests.request("GET" , "http://cmxlocationsandbox.cisco.com/api/location/v2/clients?macAddress="+macAddress , auth=('learning','learning'), verify=False )
        status_code = response.status_code
        if (status_code == 201):
            clientJSON = response.text
            clientDetail = json.loads(clientJSON)
            return clientDetail
        else:
            response.raise_for_status()
            print("Error occured in POST -->"+(response.text))
    except requests.exceptions.HTTPError as err:
        print ("Error in connection -->"+str(err))
    finally:
        if response : response.close()


# Flask App provides Web form for Admins to define the tracking policy, is also a listener for notifications from CMX
app = Flask(__name__)
app.config.from_object(__name__)

# WTForm used to create inputs, validate and bring back to Python
class SimpleForm(Form):
    
    #Grab available Zones from CMX, create drop down based on those zones
    for oneZone in zoneNames:
        zoneList.append((oneZone['hierarchy'] , oneZone['name']))
    zone = SelectField(u'Zone', choices=zoneList)
    # Define users and PPE, some hardcoding here for Dev simplicity
    user1 = SelectField(u'User1', choices=[(mac1, 'John'), (mac2, 'Adam'), (mac3, 'Sarah')])
    ppe1 = SelectField(u'Ppe1', choices=[(mac4, 'Helmet'), (mac5, 'Vest'), (mac6, 'Goggles')])
    user2 = SelectField(u'User2', choices=[('None','None'), ('John', 'John'), ('Adam', 'Adam'), ('Sarah', 'Sarah')])
    ppe2 = SelectField(u'Ppe2', choices=[('None','None'), ('Helmet', 'Helmet'), ('Vest', 'Vest'), ('Goggles', 'Goggles')])


#Root is the web form used to define tracking policy
@app.route('/',methods=['post','get'])
def defineGroups():
    form = SimpleForm()
    if form.validate_on_submit():

        #Zone data from CMX must be transformed to be used for queries.
        zoneFormat = (form.zone.data).replace('/','>')
        #Define the datatype that will populate MongoDB and define the tracking policy
        data = {'zone': zoneFormat , 'user1' : form.user1.data , 'ppe1' : form.ppe1.data, 'user2' : form.user2.data , 'ppe2' : form.ppe2.data}
        #For Dev environment - only allow one definition at a time.
        #Before allowing a new definition, delete all others. 
        groupsTable.delete_many({})
        groupsTable.insert_one(data)
        #Create a CMX notification for movements on the user in the specified zone
        createNotification(zoneFormat , form.user1.data)
    else:
        print (form.errors)
    return render_template('defineGroups.html',form=form)


#/location is used as the listener for notifications generated by CMX
@app.route('/location',methods=['POST'])
def listener():
	#Load data coming from CMX, insert it into MongoDB
    data = json.loads(request.data)
    locationTable.insert_one(data)

    #Grab the tracking policy from Mongo
    personCheck = groupsTable.find_one()
    #Check the tracking data coming in against the first person defined in policy
    if data['macAddress'] == personCheck['user1']:
        #If there was a match for the person, ask CMX about the location of the first PPE
        ppeDetail = GetLocation(data['macAddress'])
        ppeCoordinates = clientDetail[0]['mapCoordinate']
        #Print both sets of coordinates. In future our tracking logic will go here
        print (ppeCoordinates)
        print (data[0]['mapCoordinate'])

    return 'OK'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)