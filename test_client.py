#!/usr/bin/env python
#-*- coding: utf-8 -*-

import __init__ as aesgearman

gm_client = aesgearman.AESJSON_GearmanClient( ['localhost'], aeskey='123456781234567812345678' )
s = gm_client.submit_job( 'aesjsontest', ('Testing the complex data by AES',True,), background=False  )

print s.result

