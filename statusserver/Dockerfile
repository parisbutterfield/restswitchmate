FROM parisbutterfield/restswitch:statusserver2
RUN mkdir /db
RUN mkdir -p /run/nginx

ADD . /code
ADD supervisord.conf /etc/supervisord.conf
WORKDIR /code
RUN chmod -R +x *
#RUN pip install -r requirements.txt


USER root
CMD ["supervisord", "-c", "/etc/supervisord.conf"]

