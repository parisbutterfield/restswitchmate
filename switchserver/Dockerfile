FROM parisbutterfield/restswitch:switchserver
RUN mkdir /db
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
RUN chmod +x run.sh
CMD ["/code/run.sh"]
