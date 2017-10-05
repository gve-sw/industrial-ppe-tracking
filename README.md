# Using the WiFi to reduce risk in industrial envinronments



### Problem
Industrial environments can be dangerous. 

Implementing and monitoring safety policies to keep employees safe in these environments is traditionally costly and time-intensive. 


### Solution
Our solution targets Personal Protective Equipment (PPE) safety policies in the workplace. Using this solution, Operations Managers can easily define the PPE requirements for specific areas, for example ear protection on the manufacturing floor, or a vest and hat in the warehouse.

Once this policy is defined, existing WiFi infrastructure can be used to track individual employees as they enter a high-risk area. The previously defined PPE can also be tracked to ensure it is present on the employee. 

If the employee has not brought their PPE into the area or if they remove it for a significant amount of time, operations will be alerted. 


### How?
Cisco Connected Mobile Experiences (CMX) is at the centre of this solution. CMX uses WiFi infrastructure to give precise location data of wireless devices (Phones, laptops, RFID tags etc) within 1 to 3 metres.

The application is built in Python with Flask and MongoDB. 
Flask is used to serve the Operations webpage, where operations staff can define their Employee and PPE policy. 
Flask also serves as a listener for events pushed from CMX. 
MongoDB keeps a record of all the defined policies.

Once a policy has been defined by the Operations team, it is sent to CMX in the form of a notification definition. Notifications are used by CMX to PUSH data back to the application only when the predefined conditions are fulfilled. 


### Environment
This WIP implementation uses the CMX Location Sandbox for test data. 
Ngrok is used to give CMX a destination for notifications. Note that the Ngrok tunnel address will be different every time you load Ngrok and must be input in the webserver/settings.py file.

The other applications are containerised and the container environment is managed by Docker Compose. Ensure you have Docker and Compose installed, and ```docker-compose up``` can be used to bring up the environment.


