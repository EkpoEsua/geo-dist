# syntax=docker/dockerfile:1

FROM python:3.8-alpine

# install geos package dependency needed by geopy python library
RUN apk add geos

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

# run unit tests
RUN python3 -m unittest

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
