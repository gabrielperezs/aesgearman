#!/usr/bin/env python
# encoding: UTF-8
# ----------------------------------------------------------------------------

"""
Python class metod to use JSON + AES

Modify this file to include AESKYEY

"""

import gearman
from Crypto import Random
from Crypto.Cipher import AES
import json
import base64
import logging

log = logging.getLevelName(__name__)

class AESCipher:
    """
    AESCipher
    """

    def __init__(self, key):
        if len(key) < 16:
            raise ValueError(u"Key must be al lest 16 chars long")
        self.BS = 16
        self.key = key[:16]

    def pad(self, s):
        return s + (self.BS - len(s) % self.BS) *\
            chr(self.BS - len(s) % self.BS)

    def unpad(self, s):
        return s[0:-ord(s[-1])]

    def encrypt(self, raw):
        raw = self.pad(json.dumps(raw))
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return json.loads(self.unpad(cipher.decrypt(enc[16:])))


class AESDataEncoder(gearman.DataEncoder):
    @classmethod
    def encode(cls, encodable_object):
        log.debug('AES Encoder')
        return AESCipher(AESKEY).encrypt(encodable_object)

    @classmethod
    def decode(cls, decodable_string):
        log.debug('AES encoder')
        return AESCipher(AESKEY).decrypt(decodable_string)


class AESJSON_GearmanClient(gearman.GearmanClient):
    data_encoder = AESDataEncoder


class AESJSON_GearmanWorker(gearman.GearmanWorker):
    data_encoder = AESDataEncoder

if __name__ == '__main__':
    cipher = AESCipher(key='12345678790123456')
    s = cipher.encrypt('hello world')
    print s
    d = cipher.decrypt(s)
    print d
