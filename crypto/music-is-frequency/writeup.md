#Musis is frequency

Because of the known format of the rsa private key, it is possible to xor the start of the key with the classic `-----BEGIN RSA PRIVATE KEY-----`.
This give the first x char of the mask, it appears that this mask is in binary and seems to be 16 bits longs. Grouping the 16 first bits and putting it in decimal give `349` which is the rounded frquency of a 'fa' (F). The second part confirm this behavior.
Thus the key is composed from the frequency derived from the given sheet.
See exploit for full decryption.
