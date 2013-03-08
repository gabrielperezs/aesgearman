aesgearman
==========

Python classmethod to use JSON + AES an Gearman client/server at easy way.

How it works
============

#Example code for worker:

	import aesgearman
	
	def hello( gearman_worker, gearman_job ):
		print "The data:"
		print gearman_job.data
		return "Hello works!"
		
	gm_worker = aesgearman.AESJSON_GearmanWorker( ['127.0.0.1:4730'] )
	gm_worker.register_task( 'hello', hello )
  

#Example code for client:

	import aesgearman
	
	gm_client = aesgearman.AESJSON_GearmanClient( ['127.0.0.1:4730'] )
	
	data_to_send = {
		'key1': 'Value 1',
		'key2': 'Value 2',
	}
	
	gm_client.submit_job( 'hello', data_to_send )
  
