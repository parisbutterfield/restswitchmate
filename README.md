# restswitchmate 
Allows users to control Switchmate devices via REST. 

The supported device for this project is a Raspberry Pi Zero W. Three bluetooth radios are required for each service. The Pi Zero W has bluetooth built in and two USB Bluetooth adapters are added. 

Docker containers run [Flask](http://flask.pocoo.org) applications for switching, status, and authentication. Containers are multi architecture, supporting ARM and AMD64 hosts. The Switchmate device must be running firmware 2.99.9 or lower. Hopefully additional firmwares will be added in the future.

## Setup
From a Raspberry Pi Zero W
---------------------------------------------
Install [Raspbian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/)

Install docker

Install docker-compose

Clone this repo 

Run `"docker-compose build"`

Run `"docker-compose start"`


### Using
There are three services that get created in the docker-compose file. StatusServer, AuthServer, and SwitchServer.

#### StatusServer 
is responsible for getting the status of your Switchmate(s). It runs every few seconds and stores the status of all devices to a SQLite3 database. 


GET `/devices`

GET `/device/<macaddress>`

PUT `/device/<macaddress>` via proxy (needed for Home-Assistant [RESTful Switch](https://home-assistant.io/components/switch.rest/) )
  
GET `/device/<macaddress>/status`
  
The server listens on port 5000. There is also a status page that can be reached at /status.


#### AuthServer 
is responsible for getting the authentication token from the device. A SocketIO Flask application will walk the user through getting the auth token. SocketIO is used because the auth process is async and REST wouldn't fit. If you have stored all auth keys, you can disable auth server. It does not need to run for status and switching.
You can also start auth by visiting 

`/auth?macaddress=<macaddress>`

The server listens on 5001. A URL is generated from the /status page from the Status Server.


#### SwitchServer 
is responsible for handling requests to turn on and off devices. The PUT request takes a JSON payload. 

PUT `/device/<macaddress>`

Payload:
`{on: false}`

The server listens on 5002.


### Using with Home-Assistant
Coming soon.

### BOM (Bill of Materials)
1 Raspberry Pi Zero W

1 [USB Hub](https://www.amazon.com/MakerSpot-Stackable-Raspberry-Connector-Bluetooth/dp/B01IT1TLFQ/ref=sr_1_3?ie=UTF8&qid=1516586918&sr=8-3&keywords=raspberry+zero+w+hub)

2 IOGear Bluetooth Adapters

1 "Fast" MicroSD card

[![IMG_0119.jpg](https://s17.postimg.org/z3an2uwvj/IMG_0119.jpg)](https://postimg.org/image/6dnr67svf/)


### Contributing
Pull requests are welcomed. :)

My dev environment was an macOS machine running Ubuntu via VirtualBox.

You need to install BluePy and any prerequites, 

To get the bluetooth adapter(s) running on macOS in VirtualBox you need run the following command in terminal.

`sudo nvram bluetoothHostControllerSwitchBehavior="never"`

This will tell macOS not to use the adapter(s) and they'll be available to use in VirtualBox.
Confirm this by running "hcitool dev"

### Thanks
A portion of this code is from https://github.com/brianpeiris/switchmate. Many thanks for figuring out the interaction between the Switchmate.
