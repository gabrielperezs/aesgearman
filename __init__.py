import gearman
import json
from Crypto import Random
from Crypto.Cipher import AES
import json
import base64
import hashlib
import pdb


class AESCipher:
    key = False

    def __init__( self, key ):
        self.key = key
        self.BS = len(self.key)

    def pad(self, s):
        return s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)
    
    def unpad(self, s):
        return s[0:-ord(s[-1])]

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
        except (RuntimeError, TypeError, NameError):
            raise ValueError('Imposible to decrypt')


class AESDataEncoder(gearman.DataEncoder):

    aeskey = None

    @classmethod
    def encode(cls, encodable_object):
        return AESCipher( cls.aeskey ).encrypt( encodable_object )

    @classmethod
    def decode(cls, decodable_string):
        return AESCipher( cls.aeskey ).decrypt( decodable_string )


class AESJSON_GearmanClient(gearman.GearmanClient):

    def __init__(self, host_list=None, aeskey=None):
        if aeskey:
            self.data_encoder = AESDataEncoder
            self.data_encoder.aeskey = aeskey
            if ( len(aeskey) != 16 and len(aeskey) != 32 ):
                raise NameError('AES key must be either 16 or 32 bytes long');

        super(AESJSON_GearmanClient, self).__init__(host_list=host_list)
        


class AESJSON_GearmanWorker(gearman.GearmanWorker):
    
    def __init__(self, host_list=None, aeskey=None):
        if aeskey:
            self.data_encoder = AESDataEncoder
            self.data_encoder.aeskey = aeskey
            if ( len(aeskey) != 16 and len(aeskey) != 32 ):
                raise NameError('AES key must be either 16 or 32 bytes long');

        super(AESJSON_GearmanWorker, self).__init__(host_list=host_list)



