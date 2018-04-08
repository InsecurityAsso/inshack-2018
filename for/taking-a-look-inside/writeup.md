# Forensics | Taking a look inside

First, you use Wireshark on the packet capture to identify an exchange
between two computers on a LAN.

The RAM dump can be successfully parsed using Volatility from this
[repository](https://github.com/bneuburg/volatility) and branch
`Linux4_8_kaslr_support_take2`.

Generate a kernel profile on a Debian Stretch 9 using linux kernel
`4.9.0-6-amd64`.

You can solve this challenge using multiple methods :

1. As I made an error creating this challenge, many of you were able to 
   extract the **plaintext source code and AES key from nano process 
   address space** using *strings*/*grep*,
2. **retrieve and reverse python bytecode** from the RAM dump then decrypt 
   network packets using the key, I expected you to work on 
   [pyrasite](https://github.com/lmacken/pyrasite) 
   to perform the same task on a RAM dump instead of live RAM,
3. but you could also try to **break the AES-ECB encryption** of the 
   network capture (the hardest way though, because you didn't know 
   it was AES-ECB).

If you're interested in solving the real challenge try solving it using the second method and publish your solution on Github! I think it's worth trying ;)
