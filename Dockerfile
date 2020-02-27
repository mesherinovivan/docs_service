FROM ubuntu:18.04 
ARG proxy
ARG sproxy
ARG noproxy

ENV PYTHONUNBUFFERED 1
ENV http_proxy="$proxy"
ENV https_proxy="$sproxy"
ENV no_proxy="$noproxy"

RUN apt-get update && apt-get install -y pandoc python3.8 python-pip

RUN mkdir /api
WORKDIR /api
COPY requirements.txt /api/
RUN pip install -r requirements.txt
COPY . /api/