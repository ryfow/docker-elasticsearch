#!/usr/bin/python
from string import Template
import socket
import os
import etcd
import json
def go():
    print("Starting Elasticsearch")
    f = open('/elasticsearch/conf/elasticsearch.yml.template', 'r')
    s = Template(f.read())
    f.close()

    f = open('/elasticsearch/conf/elasticsearch.yml', 'w')
    submap = os.environ.copy()
    f.write(s.substitute(submap))
    f.close()
    os.system("/elasticsearch/bin/elasticsearch")

if __name__ == '__main__':
    go()
