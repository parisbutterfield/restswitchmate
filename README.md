# restswitchmate


cd scanserver

sudo docker build -f Dockerfile .

sudo docker run -p 127.0.0.1:5000:5000 --privileged
 -v /dev/bus/usb:/dev/bus/usb 
--cap-add=SYS_ADMIN -v /sys/fs/cgroup:/sys/fs/cgroup:ro 
-v /tmp/$(mktemp -d):/run --net=host -e SCAN_HCI='0' <image_id>
