Another Readme?! Another one.

When I building (`docker compose up`) the main project on the Pi Zero, it was taking ~90 minutes.
I decided to separate the build process in two:

Install dependencies and setup. (Takes long)

Copy code. (Fast)

All dependencies (python, bluez, pip) are installed here (the code in this folder). In the main project, the application code is copied to the image created here. This speeds up development and deploy time.

## Creating multi architecture images:
Docker has support though the use of the [manifest](https://developer.ibm.com/linuxonpower/2017/07/27/create-multi-architecture-docker-image/) for multi architecture images.  I developed using Ubuntu (amd64) and deploy on a Pi (arm). When `docker manifest` is added into a [release](https://github.com/moby/moby/pull/27455), building will be easier.

This is how multi architecture images work:

    Image A <--- tag

        - Image B (arm) <----- actual image
    
        - Image C (amd64) <----- actual image
    

Image A is a pointer to Image B and Image C. Through the use of the docker manifest, when a client requests an image on their machine using the name "Image A". The client pulls down the correct (Image B or Image C) for the platform.

`paris-MacBook-Pro:restswitchmate parisbutterfield$ docker inspect parisbutterfield/restswitch:statusserver | grep Architecture
"Architecture": "amd64"`

`pi@raspberrypi:~/restswitchmate $ sudo docker inspect parisbutterfield/restswitch:statusserver | grep Architecture
"Architecture": "arm"`

Depending on the architecture you are targeting. You run:

`docker-compose -f docker-compose.amd64.yml` OR `docker-compose -f docker-compose.arm.yml`


And:
`./manifest-tool --username <> --password <> push from-spec mainfestyml/switchserver.yml
./manifest-tool --username <> --password <> push from-spec mainfestyml/authserver.yml
./manifest-tool --username <> --password <> push from-spec mainfestyml/statusserver.yml`
