# restswitchmate 
This project allows users to control Switchmate devices via REST. 

The supported device for this project is a Raspberry Pi Zero W. Three bluetooth radios are required for each service, described below. The Pi Zero W has bluetooth built in and two USB Bluetooth adapters are added. 

Docker is used to create containers that run [Flask](http://flask.pocoo.org) applications for switching, status, and authentication. The containers are multi architecture, supporting ARM and AMD64 hosts. The Switchmate device must be running a firmware lower than 2.99.9. Hopefully additional firmwares will be added in the future.

## Setup
From a Raspberry Pi Zero W
---------------------------------------------
Install [Raspbian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/)

Install docker

Install docker-compose

Install git and clone this repo:
`sudo apt-get install git && git clone https://github.com/parisbutterfield/restswitchmate.git`

Run `docker-compose build`

Run `docker-compose start`


Three services are created in the docker-compose file. StatusServer, AuthServer, and SwitchServer. Each service has it's own bluetooth hardware attached to it. This prevents [problems](https://github.com/IanHarvey/bluepy/issues/57) with multiple connections on the same hardware.

#### StatusServer 
is responsible for getting the status of your Switchmate(s). It runs every few seconds and stores the status of all devices to a SQLite3 database. 

GET `/devices`

GET `/device/<macaddress>`

PUT `/device/<macaddress>` via proxy (needed for Home-Assistant [RESTful Switch](https://home-assistant.io/components/switch.rest/) )
  
GET `/device/<macaddress>/status`

<a href="https://s3.amazonaws.com/parisbutterfield.com/images/status.png"> <img src="https://s3.amazonaws.com/parisbutterfield.com/images/status.png" width="500"> </a>

StatusServer listens on port 5000. There is also a status page that can be reached at /status.


#### AuthServer 
is responsible for getting the authentication token from the device. A SocketIO Flask application will walk the user through getting the auth token. SocketIO is used because the auth process is async and REST wouldn't fit. If you have stored all auth keys, you can disable auth server. It is not need to run for status and switching.
You can start auth by visiting `/auth?macaddress=<macaddress>` or clicking "Authenticate" from the /status page of the StatusServer. Only one SocketIO client can be connected at a given time. Please close the window when authenticating multiple devices.

<a href="https://s3.amazonaws.com/parisbutterfield.com/images/auth.png"> <img src="https://s3.amazonaws.com/parisbutterfield.com/images/auth.png" width="500"> </a>

AuthServer listens on 5001. A URL is generated from the /status page from the Status Server.


#### SwitchServer 
is responsible for handling requests to turn on and off devices. The PUT request takes a JSON payload. 

PUT `/device/<macaddress>`

Payload:
`{on: false}` or `{on: true}`

SwitchServer server listens on 5002.

### Docker 
View the [Readme](https://github.com/parisbutterfield/restswitchmate/tree/master/docker)

### Using with Home-Assistant
Add the following to your configuration.yaml. This integration is a [RESTful Switch](https://home-assistant.io/components/switch.rest/). Adding [emulated_hue](https://home-assistant.io/components/emulated_hue/) will allow control via Alexa and Google Home.

```
switch:
  - platform: rest
     resource: http://<deviceip>:5000/device/<macaddress>
     method: 'put'
     body_on: '{"on": true}'
     body_off: '{"on": false}'
     is_on_template: '{{value_json.status}}'
``` 
### BOM (Bill of Materials)
1 Raspberry Pi Zero W

1 [USB Hub](https://www.amazon.com/MakerSpot-Stackable-Raspberry-Connector-Bluetooth/dp/B01IT1TLFQ/ref=sr_1_3?ie=UTF8&qid=1516586918&sr=8-3&keywords=raspberry+zero+w+hub)

2 IOGear Bluetooth Adapters

1 "Fast" MicroSD card

<a href="https://s3.amazonaws.com/parisbutterfield.com/images/pi2.jpg"> <img src="https://s3.amazonaws.com/parisbutterfield.com/images/pi2.jpg"> </a>

### Contributing
Pull requests are welcomed. :)

The development environment used for this project was a Mac running Ubuntu via VirtualBox.

You need to install BluePy and any prerequisites.

To get the bluetooth adapter(s) running on macOS in VirtualBox you need run the following command in terminal.

`sudo nvram bluetoothHostControllerSwitchBehavior="never"`

This will tell macOS not to use the adapter(s) and they'll be available to use in VirtualBox.
Confirm this by running `hcitool dev`

<a href="https://s3.amazonaws.com/parisbutterfield.com/images/ubuntu_vbox.png"> <img src="https://s3.amazonaws.com/parisbutterfield.com/images/ubuntu_vbox.png" width="500"> </a>

### Thanks
A portion of this code is from https://github.com/brianpeiris/switchmate. Many thanks for figuring out the interaction between the Switchmate.
