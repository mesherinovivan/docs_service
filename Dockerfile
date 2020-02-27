FROM ubuntu:18.04 
ARG proxy
ARG sproxy
ARG noproxy

ENV PYTHONUNBUFFERED 1
ENV http_proxy="$proxy"
ENV https_proxy="$sproxy"
ENV no_proxy="$noproxy"

RUN apt-get update && apt-get install -y pandoc python3.8 python3-pip
RUN update-alternatives --remove python /usr/bin/python2
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1

RUN mkdir /api
WORKDIR /api
COPY requirements.txt /api/
RUN pip3 install -r requirements.txt
COPY . /api/