# Build from root directory, not docker folder

FROM ubuntu:20.04

RUN apt-get update -qq && apt-get install -qq -y git libatlas-base-dev swig python3-dev python3-pip && ln -s /usr/bin/python3 python

# Create a working directory called /app
WORKDIR /app
ADD . /app

RUN pip3 install -r requirements.txt
