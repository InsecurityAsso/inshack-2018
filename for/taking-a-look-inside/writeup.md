# Forensics | Taking a look inside

The RAM dump can be successfully parsed using Volatility from this
[repository](https://github.com/bneuburg/volatility) and branch
`Linux4_8_kaslr_support_take2`.

Generate a kernel profile on a Debian Stretch 9 using linux kernel
`4.9.0-6-amd64`.

You can also use Wireshark on the packet capture to identify an exchange
between two computers on a LAN.

You can solve this challenge using multiple methods :

1. **break the AES-ECB encryption** of the network capture,
2. **retrieve and reverse python bytecode** from the RAM dump then decrypt network packets,
3. and maybe other methods I cannot think of right now.
