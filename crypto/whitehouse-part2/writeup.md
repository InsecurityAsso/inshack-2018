Please read the writeup for part 1 first.

So after flagging part 1 locally, now we have to exploit something on the remote server because the secret is only available there.

Usually, PKCS7 pads data up to a multiple of the block size, and the padding must have length >0 (which means we can possibly add a whole block of padding if the data length is already a multiple of the block size). However, in our application no padding is applied if the data length is already a multiple of the block size.

If we were to encrypt the data "administrator", it would look like this right before the encryption phase :

`01 61 64 6d 69 6e 69 73 74 72 61 74 6f 72 02 02`

The first byte is the number of blocks encrypted (only a single 16-byte block here), used as a basic check for integrity. The last two bytes have value 2 to indicate padding has length 2.

Now, if we were to encrypt the string "administrator[02][02]" where [02] is the character with code 2 (not printable), the processed string before encryption would look like this on a non-vulnerable server :

`02 61 64 6d 69 6e 69 73 74 72 61 74 6f 72 02 02 0f 0f 0f 0f 0f 0f 0f 0f 0f 0f 0f 0f 0f 0f 0f 0f`

However, the vulnerable server sees a multiple of 16 bytes so it doesn't add any padding :

`01 61 64 6d 69 6e 69 73 74 72 61 74 6f 72 02 02`

Which means we can manage to get the token for "administrator" without registering the "administrator" user, but instead "administrator[02][02]" which passes the check.

This also means that most of the times, registering a user of length 15, 31, 47, ... will lead to an invalid token because unpadding will not see any valid padding.

With "administrator[02][02]"'s token, we can now ask for the nuclear code, and the token will decrypt as "administrator" so we get the master key.
