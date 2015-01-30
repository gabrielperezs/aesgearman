#!/usr/bin/env python
#-*- coding: utf-8 -*-

import __init__ as aesgearman
import datetime;
import sys

def aesjsontest( gearman_worker, gearman_job ):

    response = {
        'data_from_client': gearman_job.data,
        'hola': 'bon dia!',
        'chao': ('bye','adios','adeu'),
        'date': str( datetime.datetime.now() ),
    };

    return response

server = 'localhost'
if len(sys.argv) > 1:
    server = sys.argv[1]

gm_worker = aesgearman.AESJSON_GearmanWorker( [server], aeskey='12345678123456781234567812345678' )
s = gm_worker.register_task( 'aesjsontest', aesjsontest )
gm_worker.work()

