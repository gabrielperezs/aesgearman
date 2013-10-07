aesgearman
==========

Python classmethod to use JSON + AES an Gearman client/server at easy way.

How it works
============

#Example code for worker (AES-256):

    import __init__ as aesgearman
    import datetime;

    def aesjsontest( gearman_worker, gearman_job ):

        response = { 
            'data_from_client': gearman_job.data,
            'hola': 'bon dia!',
            'chao': ('bye','adios','adeu'),
            'date': str( datetime.datetime.now() ),
        };

        return response

    gm_worker = aesgearman.AESJSON_GearmanWorker( ['localhost'], aeskey='12345678123456781234567812345678' )
    s = gm_worker.register_task( 'aesjsontest', aesjsontest )
    gm_worker.work()

  

#Example code for client (AES-256):

    import aesgearman

    gm_client = aesgearman.AESJSON_GearmanClient( ['localhost'], aeskey='12345678123456781234567812345678' )
    s = gm_client.submit_job( 'aesjsontest', ('Testing the complex data by AES',True,), background=False )

    print s

FAQ
===

*What encryption used?*
[AES symmetric cipher](https://www.dlitz.net/software/pycrypto/api/current/Crypto.Cipher.AES-module.html)

*What should be the key length?*
The secret key to use in the symmetric cipher. It must be 16 (AES-128) or 32 (AES-256) bytes long.
    
Author
------

Gabriel Pérez Salzar [@gabrielperezs](https://twitter.com/gabrielperezs)


