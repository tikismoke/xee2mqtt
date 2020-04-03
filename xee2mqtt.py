from xee import Xee
import xee.entities as xee_entities
import sys
import os
import pickle
import pytz
#import datetime
import json
import paho.mqtt.client as paho

broker="YOUR MQTT BROKER IP OR NAME"
port=YOUR MQTT PORT

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

client1= paho.Client("xee2mqtt")                           #create client object
client1.on_publish = on_publish                          #assign function to callback
client1.connect(broker,port)                                 #establish connection


xee = Xee(client_id="YOUR XEE CLIENT ID API V3", 
        client_secret="YOUR XEE CLIENT SECRET API V3", 
        redirect_uri="http://localhost")

login_url = xee.get_authentication_url()+"&redirect_uri=http://localhost"
xee_config_file = os.path.join(os.path.dirname(__file__), 'xee.json')

try:
    with open(xee_config_file, 'rb') as xee_token_file:
        print ("Opening File")
        token = pickle.load(xee_token_file)
    print ("Getting user")
    user ,error = xee.get_user(token.access_token)
    print (error)
    if error is not None :
        print ("Error getting user, try refreshing with token_refresh from file")
        print (error)
        token,error = xee.get_token_from_refresh_token(token.refresh_token)
        if error != None :
            print (error)
            sys.exit("refreshing token failed from refresh_token")

except:
    print ("Error with file saved or no file saved")
    print("Go to %s allow the app and copy your oauth_verifier" %login_url)
    authorization_code = input('Please enter your authorization_code: ')
    token,error = xee.get_token_from_code(authorization_code)
    if error is not None :
        print ("Error getting token from code")
        print (error)
        print ("Exiting")
        sys.exit("refresh Error")

with open(xee_config_file, 'wb') as xee_token_file:
    pickle.dump(token, xee_token_file)

user ,error = xee.get_user(token.access_token)
#print user
#cars ,error = xee.get_cars(token.access_token)
#print cars

#get user cars
cars, err = xee.get_cars(token.access_token)
#print cars
#list cars
for car in cars:
#    print car
    try:
        client1.publish("/XEE/" + str(car.id) + "/carname/", str(car.name))
    except:
        print ("error publishing carname")
        #print (car)
#Get status for each cars
    Status  ,error = xee.get_status(car.id,token.access_token)
    #print (Status)
    if error is None:
        for statu in Status:
            #print status
            if statu is not None:
                for signals in statu:
                    try:
                        print (signals)
                        client1.publish("/XEE/" + str(car.id) + "/" + str(signals.name)  + "", str(signals.value))
                    except:
                        print ("error publishing this value")
                        #print (signals)
    Locations ,error = xee.get_locations(car.id,token.access_token,limit=1)
    #print (Locations)
    if error is None:
        for location in Locations:
            try:
                lat=location.latitude
                lon=location.longitude
                print (location)
#                client1.publish("/XEE/" + str(car.id) + "/location/", json.dumps(location, default=str))
#                client1.publish("/XEE/" + str(car.id) + "/location/", json.dumps(locations, indent=4, sort_keys=True, default=str))
                client1.publish("/XEE/" + str(car.id) + "/location/", json.dumps({"longitude": lon,"latitude": lat}))
            except:
                print ("error publishing location")
                #print (location)
