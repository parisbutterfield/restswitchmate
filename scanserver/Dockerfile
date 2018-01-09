FROM amd64/python:2
ADD . /code
WORKDIR /code
RUN apt-get update && apt-get install -y bluetooth bluez \
libbluetooth-dev \
libudev-dev \
libperl-dev \
libglib2.0-dev
RUN pip2 install -r requirements.txt
WORKDIR /usr/local/lib/python2.7/site-packages/bluepy
RUN make
WORKDIR /code
RUN chmod +x run.sh
CMD ["/code/run.sh"]



