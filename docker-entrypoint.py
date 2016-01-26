#!/usr/bin/python

import tutum
import os
import requests
import subprocess
import netifaces
import time
import sys

# fetch live cluster nodes
print 'fetching live cluster nodes'
svc = tutum.Utils.fetch_remote_service(os.environ.get('TUTUM_SERVICE_FQDN'))
stk = tutum.Utils.fetch_by_resource_uri(svc.stack)
nodes = []
for ctr in svc.containers:
    ctr = tutum.Utils.fetch_by_resource_uri(ctr)
    if ctr.state == 'Running':
        ctr_hostname = ctr.name + '.' + stk.name
        ctr_url = 'http://%s:9200/' % (ctr_hostname,)
        try:
            r = requests.get(ctr_url)
        except:
            continue
        if r.status_code == 200:  # healthy
            nodes.append(ctr_hostname)

print 'found live nodes: '
print nodes

cmd = [
    '/docker-entrypoint.sh',

    '--cluster.name=' + os.environ.get('ELASTICSEARCH_CLUSTER_NAME'),

    '--discovery.zen.ping.multicast.enabled=false',
    '--discovery.zen.ping.timeout=3s',
    '--discovery.zen.minimum_master_nodes=1',
]

if nodes:
    cmd.append('--discovery.zen.ping.unicast.hosts=' + ','.join(nodes) if nodes else '')

# wait for ethwe to appear

slept = 0
print 'waiting for ethwe interface to appear'
while not 'ethwe' in netifaces.interfaces():
    time.sleep(1)
    slept += 1
    print '  .'
    if slept >= 30:
        print 'interface ethwe did not appear timely'
        sys.exit(1)

print cmd

subprocess.call(cmd)
