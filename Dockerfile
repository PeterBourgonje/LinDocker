FROM python:3.6-stretch
LABEL maintainer="bourgonje@uni-potsdam.de"

RUN apt-get -y update &&\
    apt-get upgrade -y &&\
    apt-get install -y openjdk-8-jdk && \
    apt-get install -y python3-dev &&\
    apt-get update -y

ADD requirements.txt .
RUN pip3 install -r requirements.txt

ADD aux_data /aux_data
ADD config.properties .
ADD convert.py .
ADD flaskApp.py .
ADD logs /logs
ADD models /models
ADD parser.jar .

RUN mkdir inputoutput

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

EXPOSE 5000

ENTRYPOINT FLASK_APP=flaskApp.py flask run --host=0.0.0.0 --port=5000
#CMD ["/bin/bash"]