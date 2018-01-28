FROM parisbutterfield/restswitch:switchserver
RUN mkdir /db
ADD . /code
WORKDIR /code
RUN chmod +x run.sh
CMD ["/code/run.sh"]
