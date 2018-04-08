You're given a simple auth server which is a x64 ELF compiled with -O3 and stripped. Not the funniest to reverse engineer, even with Hex Rays.

The server also runs on a CTF machine, and its two arguments are the only secrets : The nuclear master key and the encryption key.

It offers two features : register and generate.

The register function allows to register a new president, its business logic works as such :

- Ask for the new president's name

- Check that it is not "admin" or any of the previous US president's full name

- Make the new president take the oath of office (repeat a small text), there is a neat override as you can just skip this part by typing "yeah sure whatever"

- Count the number of 16-byte blocks that would be encrypted after we pad the president's name, and prepend this number to the president's name

- Pad the data with a custom PKCS7 padding. The padding function has a flaw which can be exploited in part 2, it can also get us the flag for part 1 but there's an easier way.

- Encrypt the data with a homemade Feistel network scheme operating with CBC. The Feistel network is probably easy to break too, but other ways make it easier.

- Give the encrypted data back to the user.

- Generate a nuclear code from the president's name (it's a CRC which depends only on the president's name).


The generate function takes an encrypted token, decrypts it and check that it is valid (correct padding and number of blocks stored in the 1st byte).

- If the decrypted username is "administrator", we show the nuclear master key (useful for part 2)

- Otherwise, we generate the password for the decrypted president's name.

By studying how the passcode generation works, we can observe that it does not depend on any of the secret parameters. Thus, we can simply patch the first check in the registration function, so we can actually register as "Bill Clinton" locally and get his nuclear code.

This does not work for part 2 with administrator, for which the passcode is not generated : it's one of the two secrets passed as an argument to the server. That means we will need to do some practical work on the remote server instead of patching the executable locally.