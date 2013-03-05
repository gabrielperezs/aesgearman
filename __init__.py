import gearman
import json
from Crypto import Random
from Crypto.Cipher import AES
import json
import base64
import hashlib


AESKEY = ''

class AESCipher:
        def __init__( self, key ):
                self.BS = 16
                self.pad = lambda s: s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)
                self.unpad = lambda s : s[0:-ord(s[-1])]
                self.key = key[0:16]

        def encrypt( self, raw ):
                raw = self.pad( json.dumps(raw) )
                iv = Random.new().read( AES.block_size )
                cipher = AES.new( self.key, AES.MODE_CBC, iv )
                return base64.b64encode( iv + cipher.encrypt( raw ) )

        def decrypt( self, enc ):
		try:
			enc = base64.b64decode(enc)
			iv = enc[:16]
			cipher = AES.new(self.key, AES.MODE_CBC, iv )
			return json.loads( self.unpad(cipher.decrypt( enc[16:] )) )
		except:
			return False
			raise NameError('Hola')


class AESDataEncoder(gearman.DataEncoder):
        @classmethod
        def encode(cls, encodable_object):
                return AESCipher( AESKEY ).encrypt( encodable_object )

        @classmethod
        def decode(cls, decodable_string):
                return AESCipher( AESKEY ).decrypt(decodable_string)


class AESJSON_GearmanClient(gearman.GearmanClient):
        data_encoder = AESDataEncoder

class AESJSON_GearmanWorker(gearman.GearmanWorker):
        data_encoder = AESDataEncoder


