FROM python:alpine
ADD . /code
WORKDIR /code
RUN apk add --no-cache \
bluez-libs eudev-libs glib-dev \
&& apk add --no-cache gcc g++ musl-dev cmake make linux-headers
RUN pip install -r requirements.txt
dockerRUN chmod +x run.sh
CMD ["/code/run.sh"]
