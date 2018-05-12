FROM parisbutterfield/restswitch:switchserver2
RUN mkdir /db
ADD . /code
ADD supervisord.conf /etc/supervisord.conf
WORKDIR /code
RUN chmod +x -R *.sh
RUN chmod +x -R *.py
CMD ["supervisord", "-c", "/etc/supervisord.conf"]
