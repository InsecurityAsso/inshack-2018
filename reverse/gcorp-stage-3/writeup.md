# G-Corp - stage 3: easy reverse and easy decryption (rev/crypto)

Once the archive is extracted, you see 3 files:
 + `key.bin`
 + `crypt`
 + `emergency_override.enc`

You can clearly understand how `crypt` works, what `key.bin` was used for and what
you want to do with this unreadable file named `emergency_override.enc`.

Just reverse crypt and find out that it is using XTEA algorithm and CBC chaining mode.

Code the decryption program (an example is provided in `exploit/exploit`).

Decrypt the file.

