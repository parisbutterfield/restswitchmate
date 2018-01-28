FROM alpine:3.6
ADD . /pip-requirements
WORKDIR /pip-requirements
RUN apk add --no-cache \
bluez-libs eudev-libs glib-dev python py-pip\
&& apk add --no-cache gcc musl-dev cmake make
RUN pip install -r requirements.txt
RUN apk del cmake make
