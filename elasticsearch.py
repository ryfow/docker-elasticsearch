#!/usr/bin/python
from string import Template
import socket
import os
import subprocess
import etcd
import json
import time
import signal
import string
def go():
    f = open('/elasticsearch/config/elasticsearch.yml.template', 'r')
    s = Template(f.read())
    f.close()
    submap = os.environ.copy()
    public_ip = socket.gethostbyname(submap['COREOS_PUBLIC_IPV4'])
    client = etcd.Client(host=submap['COREOS_PUBLIC_IPV4'])
    submap['CLUSTER_NAME'] = 'elasticsearch'
    # stick this node in the elasticsearch nodelist
    r = client.write("/services/elasticsearch", public_ip, append=True, ttl=30)
    es_node = r.value
    time.sleep(1)
    es_all_nodes = client.get("/services/elasticsearch")
    # lets consider the first elastsearch node a master
    masta = es_all_nodes.children.next().value

    submap['DISCOVERY_HOSTS'] = str([str(n.value) for n in es_all_nodes.children])
    submap['PUBLIC_IP'] = public_ip
    f = open('/elasticsearch/config/elasticsearch.yml', 'w')

    f.write(s.substitute(submap))
    f.close()
    proc = subprocess.Popen(["/elasticsearch/bin/elasticsearch"])

    signal.signal(signal.SIGINT, lambda s, f: proc.send_signal(signal.SIGINT))
    signal.signal(signal.SIGTERM, lambda s, f: proc.send_signal(signal.SIGTERM))

    while not proc.returncode:
      es_node = client.write(r.key, public_ip, append=False, ttl=30).value
      time.sleep(20)
      proc.poll()

if __name__ == '__main__':
    go()
