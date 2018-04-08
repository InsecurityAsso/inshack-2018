# G-Corp - stage 2: reverse and exploit (rev/pwn) 

The file you extracted before should be easy to reverse and you know that it
contains a backdoor. Therefore you should find a vulnerability inside and write
an exploit.

Once you've got a working exploit, which means a DNA-encoded payload containing

`128 * NOP + ASCII bash command + \0`

You will quickly find that you can only execute some commands including ls and hexdump.

You can find a file named `stage_3_storage.zip` using `ls` then retrieving its
content using `hexdump`.
