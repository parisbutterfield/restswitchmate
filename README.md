# Setup
From a Raspberry Pi Zero W
---------------------------------------------
Install Raspbian Stretch Lite

Install Docker

Install Docker-Compose

Git clone this repo 

Run `"docker-compose build"` (This might take some time)

Run `"docker-compose start"`



# Using
There are three services that get created in the docker-compose file. StatusServer, AuthServer, and SwitchServer.

## StatusServer 
is responsible for getting the status of your Switchmate(s). It runs ever few seconds and stores the status of all devices to a SQLite3 database. There is a Flask application running to get the values from the database.


/devices

/device/\<macaddress\>
  
/device/\<macaddress\>/status
  
The server listens on port 5000. There is also a status page that can be reached at /status.


## AuthServer 
is responsible for getting the authentication token from the device. A SocketIO Flask application will walk the user through getting the auth token.
SocketIO is used because the auth process is async and REST wouldn't fit here. If you have stored all auth keys, you can disable auth server. It does not need to run for status and switching.
The server listens on 5001. A URL is generated from the /status page from the Status Server.
You can also start auth by visiting 

:5001/auth?macaddress=\<insert_macaddress\>


## SwitchServer 
is TBD. It will handle switching via HTTP POST. Reading from the SQLite3 DB for the Auth Key.

# Using with Home-Assistant
Coming soon.

# BOM (Bill of Materials)
1 Raspberry Pi Zero W

1 [USB Hub] (https://www.amazon.com/MakerSpot-Stackable-Raspberry-Connector-Bluetooth/dp/B01IT1TLFQ/ref=sr_1_3?ie=UTF8&qid=1516586918&sr=8-3&keywords=raspberry+zero+w+hub)


2 IOGear Bluetooth Adapters

1 "Fast" MicroSD card


# Contributing
Pull requests are welcomed. :)

My dev environment was an macOS machine running Ubuntu via VirtualBox.

You need to install BluePy and any prerequites, 

To get the bluetooth adapter(s) running on macOS in VirtualBox you need run the following command in terminal.

`sudo nvram bluetoothHostControllerSwitchBehavior="never"`

This will tell macOS not to use the adapter(s) and they'll be available to use in VirtualBox.
Confirm this by running "hcitool dev"

# Thanks
A large portion of this code is a fork of https://github.com/brianpeiris/switchmate. So many thanks for figuring out the interaction between the Switchmate.
