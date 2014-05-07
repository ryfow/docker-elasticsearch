FROM ubuntu:12.04
MAINTAINER Ryan Fowler <ryan.fowler@singlewire.com>

RUN apt-get update -y
RUN apt-get install -y --no-install-recommends openjdk-7-jdk openjdk-7-jre
RUN apt-get install -y curl vim python-pip libssl-dev
RUN apt-get install -y python-openssl python-dev unzip
RUN pip install python-etcd

RUN curl -O "https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.1.1.zip"
RUN unzip elasticsearch-1.1.1.zip
RUN mv elasticsearch-1.1.1 elasticsearch
ADD ./elasticsearch.yml.template /elasticsearch/conf/elasticsearch.yml.template
ADD ./elasticsearch.py /elasticsearch.py
CMD ["/elasticsearch.py"]
