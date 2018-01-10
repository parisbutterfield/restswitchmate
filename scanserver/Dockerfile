FROM alpine:3.6
ADD . /code
WORKDIR /code
RUN apk add --no-cache \
bluez-libs eudev-libs glib-dev python py-pip\
&& apk add --no-cache gcc musl-dev cmake make
RUN pip install -r requirements.txt
RUN apk del cmake make
RUN chmod +x run.sh
CMD ["/code/run.sh"]
