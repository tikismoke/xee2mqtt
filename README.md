# xee2mqtt
Simple Xee api V4 script to mqtt it automatically parse all cars, signals for each cars and location for each cars of user to mqtt.

You need to register and create an apps on the xee dev site (https://dev.xee.com/) it's free :)

Select at least those scope:
 
-vehicles.read

-vehicles.management

-vehicles.signals.read

-vehicles.locations.read

-vehicles.accelerometers.read

-account.read

-vehicles.devices-data.read

-vehicles.events.read

Redirect_url is important be sure it's the same as used in the code here:
https://github.com/tikismoke/xee2mqtt/blob/a2b60b27b9fc95f6626a2d7274b642a03437ebf9/xee2mqtt.py#L29

`When patch will be available you will need to install https://github.com/quentin7b/xee-sdk-python`

For the moment follow this procedure:

```
git clone https://github.com/tikismoke/xee-sdk-python
cd xee-sdk-python
git checkout patch-1
python setup.py install
```

install requirements if not already done (pytz, arrow, oauth2, oauthlib, oauth_requests)


```
pip3 install pytz
pip3 install arrow
pip3 install oauth2
pip3 install oauthlib
pip3 install requests_oauthlib
```

Adapt somes row to your needs:

```
broker="YOUR MQTT BROKER IP OR NAME"
port=YOUR MQTT PORT
AND
client_id="YOUR XEE CLIENT Key API V4", 
client_secret="YOUR XEE CLIENT Secret API V4", 
```


Run at least in console once to generate the auth code needed (follow the link to allow your account access) it will generate a code that you need to paste back in the console.

It will the create a xee.json file contain token and refresh token for next calls.

You can now create a cron rules to call this script every 5/10/20/30/60 minutes as you want.


NOTE
----

Indeed you need also an mqt server and lib to communicate with.
