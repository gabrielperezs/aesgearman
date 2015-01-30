#!/usr/bin/env python
#-*- coding: utf-8 -*-

import __init__ as aesgearman
import string
import random
import base64
import zlib
import sys

datatosend = {
    'sfirts_1': 'param '+''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(256)),
    'sfirts_2': 'param '+''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(256)),
    'base64_1': base64.encodestring(''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(1024))),
    'gzip_1': base64.encodestring(zlib.compress(''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(256)))),
}

print datatosend

server = 'localhost'
if len(sys.argv) > 1:
    server = sys.argv[1]

gm_client = aesgearman.AESJSON_GearmanClient( [server], aeskey='12345678123456781234567812345678' )
s = gm_client.submit_job( 'aesjsontest', datatosend, background=False  )
print s.result
