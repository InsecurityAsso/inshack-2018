#G-Corp Write-Up

This challenge is quite hard to solve because you need to solve 4 consecutive 
sub-challenges to finally get the flag. These 4 stages will be described bellow 
and a solution will be provided to solve these challenges.

##Stage 1: Find and extract (forensics)

You get a description and a Wireshark capture file `exfil.pcap`. According to 
the description you need to find info in this capture and extract it for further 
analysis.

When opened with Wireshark, the file shows a TCP connection with a lot of data 
going through it. Some of this data consists of a plaintext which seems to be a 
message from a hacker to another hacker. It actually gives a clue on the content 
of the data tranferred.

Use follow TCP stream functionnality and save the raw data stream into a file. 

Run `binwalk -e` on the file you saved. It should be able extract an executable 
file that you can run. 

##Stage 2: Reverse and exploit (rev/pwn) 

The file you extracted before should be easy to reverse and you know that it 
contains a backdoor. Therefore you should find a vulnerability inside and write 
an exploit.

Once you've got a working exploit, which means a DNA-encoded payload containing 

`128 * NOP + ASCII bash command + \0`

You will quickly find that you can only execute some commands including ls and hexdump.

You can find a file named `stage_3_storage.zip` using `ls` then retrieving its 
content using `hexdump`.

##Stage 3: Easy reverse and easy decryption (rev/crypto)

Once the Zip archive retrieved is extracted, you see 3 files:
 + `key.bin`
 + `crypt`
 + `emergency_override.enc`

You can clearly understand how `crypt` works, what `key.bin` was used for and what 
you want to do with this unreadable file named `emergency_override.enc`.

Just reverse crypt and find out that its using XTEA algorithm and CBC chaining mode.

Code the decryption program (an example is provided in `exploit/exploit_stage_3`).

Decrypt the file.

##Stage 4: Source code analysis and crack (rev/cracking)

Now that you have the code source of the emergency override and the value of the 
port on which the service is running you can try to find a key satisfying the 
test.

You have to solve the following problem: find a 3D matrice of 4*4*4 resulting in 
64 unknown values which once passed to the algorithm validates the result vector.
