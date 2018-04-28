FROM parisbutterfield/restswitch:statusserver
RUN apk update && apk add --no-cache supervisor nginx linux-headers python-dev


RUN mkdir /db
RUN mkdir -p /run/nginx

COPY /nginx/nginx.conf /etc/nginx/nginx.conf
COPY /nginx/nginx.vh.default.conf /etc/nginx/conf.d/default.conf

ADD . /code
ADD supervisord.conf /etc/supervisord.conf
WORKDIR /code
RUN chmod +x *.py
RUN chmod +x nginx/*.sh
RUN ls -ltr
RUN pip install -r requirements.txt


USER root
CMD ["supervisord", "-c", "/etc/supervisord.conf"]

#RUN chmod +x run.sh
#CMD ["/code/run.sh"]
