#!/usr/bin/env python3

import sys
import json
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

data = {}
data['as'] = [{ 'asn': n.decode('utf-8') } for n in r.smembers('dn42wp-as')]
rawPeerings = [p.decode('utf-8').split(',') for p in r.smembers('dn42wp-peerings')]
data['peerings'] = [{ 'source': rp[0], 'target': rp[1] } for rp in rawPeerings]

print(json.dumps(data))

