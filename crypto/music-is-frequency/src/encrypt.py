#!/usr/bin/python3
from Crypto.PublicKey import RSA
import base64
key = RSA.generate(2048)

binPrivKey = key.exportKey()


msg = open('flag.txt').readline()
notes = ['fa','sol','la','fa','fa','sol','la','fa','la','si','do','la','si','do','do','re','do','si','la','fa','do','re','do','si','la','fa','fa','do1','fa','fa','do1','fa']
frequency = {'do1':262,'fa':349,'sol':392,'la':440,'si':466,'do':523,'re':587}
association_dec = [frequency[i] for i in notes]
association_binary_str = "".join(['{0:016b}'.format(i) for i in association_dec])

with open('privatekey.bin','w') as f:
    f.write(''.join(chr(ord(j) ^ ord(association_binary_str[i % len(association_binary_str)])) for i,j in enumerate(binPrivKey.decode())))

with open('flag.enc','wb') as f:
    f.write(base64.b64encode(key.publickey().encrypt(msg.encode('utf-8'), 32)[0]))
