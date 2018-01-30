Another Readme?!

Another one. While I was building (docker compose up) the main project on the Pi Zero, it was taking about 90 minutes.
I decided to separate the build process in two:

Install dependencies and setup. (Takes long)
Copy code. (Fast)

Essentially, all dependencies (python, bluez, pip) are installed here (the code in this folder). In the main project, the application code is copied to the image created here. This speeds up development and deploy time.

Creating multi architecture images:
This is topic that isn't solved in the docker world yet. I develop on a Mac (amd64) and deploy on a Pi (arm). So we There's a PR which should make things a lot easier.

This is how multi architecture images work:

Image A
    - Image B (arm) <----- actual image
    - Image C (amd64) <----- actual image

Image A is a pointer to Image B and Image C. Through the use of the docker manifest, when a client requests an image on their machine using the name "Image A". The client pulls down the correct (Image B or Image C) for the platform.

paris-MacBook-Pro:restswitchmate parisbutterfield$ docker inspect parisbutterfield/restswitch:statusserver | grep Architecture
"Architecture": "amd64",

pi@raspberrypi:~/restswitchmate $ sudo docker inspect parisbutterfield/restswitch:statusserver | grep Architecture
"Architecture": "arm",

Depending on the architecture you are targeting. You run:

docker-compose -f docker-compose.amd64.yml OR docker-compose -f docker-compose.arm.yml


And then:
./manifest-tool --username <> --password <> push from-spec mainfestyml/switchserver.yml
./manifest-tool --username <> --password <> push from-spec mainfestyml/authserver.yml
./manifest-tool --username <> --password <> push from-spec mainfestyml/statusserver.yml
