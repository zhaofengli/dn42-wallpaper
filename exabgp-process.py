#!/usr/bin/env python3

import sys
import json
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

while True:
    line = input().strip()

    try:
        message = json.loads(line)
    except Exception as e:
        # log('Malformed JSON? {}'.format(e))
        continue

    if message['type'] != 'update':
        # Not an update - Ignoring
        continue

    try:
        update = message['neighbor']['message']['update']
        peerasn = message['neighbor']['asn']['peer']

        if 'announce' in update:
            # Announcement
            aspath = [peerasn] + update['attribute']['as-path']
            peerings = [
                sorted([aspath[i], aspath[i+1]])
                for i in range(len(aspath)-1)
            ]
            peeringsm = ['{},{}'.format(p[0], p[1]) for p in peerings]
            r.sadd('dn42wp-as', *aspath)
            r.sadd('dn42wp-peerings', *peeringsm)

        elif 'withdraw' in update:
            # Withdrawal
            pass

    except Exception as e:
        # log('Something happened: {}'.format(e))
        continue
