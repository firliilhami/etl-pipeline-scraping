from python:3.8-slim

RUN apt-get update && apt-get install

RUN mkdir -p /home/app
RUN apt-get update
RUN apt-get -y install libpq-dev gcc

COPY requirements.txt /home/app

RUN pip install -r /home/app/requirements.txt

COPY main.py /home/app

ENTRYPOINT python ./home/app/main.py