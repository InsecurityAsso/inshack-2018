# Crypt0r - Part 3

`You did a very good job until now. To be sure no one is going to be trapped again, could you find a way to protect the whole company?`
`To do so, you can use the binary located on the website of part 2, our expert told us that is was safe to run. `
  
`_Note: you need to solve part 2 before attempting this part_`


We start downloading the malware following the given link: `http://kx4hdh2zo5rstcuj.onion/super-secret-location-that-you-cant-find-without-help/W32.Cryptor.exe`

This is a Win32 binary. It seems to be safe to run so give a try to see what happen. A dialog is displayed containing the same kind of text that what we just decode in the first part of the challenge. However, the personal key is slightly different.

![First run](https://github.com/HugoDelval/inshack-2018/raw/master/reverse/crypt0r-part-3/img/first_run.png)

What happen if we just disconnect the network? Let's try.

![Offline](https://github.com/HugoDelval/inshack-2018/raw/master/reverse/crypt0r-part-3/img/no_network.png)

Ok, it seems the binary detects there is a connectivity issue and is not deactivated. However, this string can't be retrieved from the C&C.

Time to reverse the binary. Quickly, we can see `UPX` segments of code which means the binary has been packed with UPX. Try to unpack it first.

```powershell
U:\cryptor\part 3> dir
08/04/2018  15:38    <REP>          .
08/04/2018  15:35    <REP>          ..
08:04/2018  13:06            60 928 W32.Cryptor.exe
               1 fichier(s)          60 928 octets
U:\cryptor\part 3>U:\upx394w\upx.exe -d W32.Cryptor.exe
                       Ultimate Packer for eXecutables
                          Copyright (C) 1996 - 2017
UPX 3.94w       Markus Oberhumer, Laszlo Molnar & John Reiser   May 12th 2017

        File size         Ratio      Format      Name
   --------------------   ------   -----------   -----------
    150528 <-     60928   40.48%    win32/pe     W32.Cryptor.exe

Unpacked 1 file.

U:\cryptor\part 3>dir
08/04/2018  15:40    <REP>          .
08/04/2018  15:40    <REP>          ..
08/04/2018  13:06           150 528 W32.Cryptor.exe
               1 fichier(s)          150 528 octets
```

Now, load it (once again) in your favorite disassembler and this is far better. We see that some functions have been exported, which is quite curious. We do not see the previous offline string which means that the strings are probably encrypted.

When we look at the main function, it seems that the binary prevents any debugger to be attached. And indeed, when you try to attach a debugger, you get an error.

![Debugger](https://github.com/HugoDelval/inshack-2018/raw/master/reverse/crypt0r-part-3/img/debugger_test.png)

But we can understand the flow without any debugger:
1. The malware tries to connect to the C&C
2. It performs some checks on the VictimID
3. It checks whether the victim is imune
4. The flow is split whether the victim is imune or not
    - if the victim is not, then an encryption is performed.
5. Cleanup the socket

It's quite interesting to see that the victim can be `imune`.

![Imune](https://github.com/HugoDelval/inshack-2018/raw/master/reverse/crypt0r-part-3/img/imune_flow.png)

The code of the `IsVictimImune` is very short and looks like a `getter`:
```asm
; bool __thiscall CEncryptionService::IsVictimImune(CEncryptionService *__hidden this) public ?IsVictimImune@CEncryptionService@@QBE?B_NXZ
?IsVictimImune@CEntryptionService@@QBE?B_NXZ proc near
mov al, [ecx]
retn
?IsVictimImune@CEncryptionService@@QBE?B_NXZ endp
```

So, the attribute is probably set while performing the checks on the `victimID` which is probably the key to solve the challenge.

The method `LookAtVictimID` is a big mess and the flow is broken several times by jumping on computed addresses. However, at the beginning of the function, these lines are quite interesting:

```asm
xor edx, edx
mov eax, [ebp+arg_4]        ; mov victimID in eax
mov ecx, 10
div ecx                     ; divide victimID by 10
test eax, eax
jz __end_of_LookAtVictimID  ; leave if eax == 0
cmp eax, 25
jg __end_of_LookAtVictimID  ; leave if eax > 25
```

This code means that the function is only ran when `victimID >= 10 && victimID < 260`.
When we quickly browse the other labels, we see that there are a lot of call (28) to `sub_B09EA0` with a use of `ecx`, a register often used as the `this` pointer . Every call to this function takes `[ebp+arg_0]` as parameter which is initialized at the beginning and returned at the end of the function. And by looking to the signature of the method `LookAtVictimID`, it seems to return a `std::string`. 
So `sub_B09EA0` is a method of `std::string` which seems to be involved in the flag generation process.

The challenge aims to `find a way to protected the whole company`. So it seems we can't patch the binary and we have to find another way to inject the right `victimID` that unlocks the flag.

What we can do now is importing the symbol in a custom app to bruteforce every `victimID` between 10 and 259. Well, actually we do not have any header and it could take days to find how to import a class member... So let bruteforce the victimID by emulating a server and see what happens.

To do this, we need to understand how the malware communicates with the C&C and intercept the packets (rogue DNS or packet mangling). We have already written the decode function in the first part of the challenge so it should be quite easy now.

When looking at the `Connect` method, we see that the malware resolves a domain and makes some `xor` on the IPs.

Flush the DNS cache then run Wireshark to understand what is done.

```powershell
U:\cryptor\part 3> ipconfig /flushdns
Configuration IP de Windows

Cache de résolution DNS vidé.
```

We can see that the malware tries to resolve `cnc.crypt0r.challenge-by.ovh` which has 2 A entries:
- 161.134.160.91
- 32.103.210.252

The address of the C&C is `167.114.225.129`. The function `decryptAddress` has some `xor` between the bytes of these 2 addresses:
```asm
mov edx, [ebp+arg_0]
mov al, [edx+7]
xor al, [edx+3]
mov cl, [edx+6]
xor cl, [edx+2]
```

Try to `xor` manually these 2 addresses to since if we can get 
- 161 ^ 32 = 129
- 134 ^ 103 = 225
- 160 ^ 210 = 114
- 91 ^ 252 = 167

Ok, we know how the IP address is retrieved. Since I don't know how to forward the packets under Windows, I will try to setup a fake DNS entry that will answer a fake IP for the domain `cnc.crypt0r.challenge-by.ovh`.  To do so, I edit the `C:\Windows\System32\drivers\etc\hosts` file and add the following entries:
```
23.1.168.192    cnc.crypt0r.challenge-by.ovh
0.0.0.0         cnc.crypt0r.challenge-by.ovh
```

I then bind on port 7143 on `192.168.1.23` and here what I get:


![Traffic interception](https://github.com/HugoDelval/inshack-2018/raw/master/reverse/crypt0r-part-3/img/dns.png)

Now, we just need to write a dummy C&C to inject the `victimID` we want.  As we saw in the first part, the server sends the encryption key right after the `CRYPT0R_SEED` packet. So, I decided to remove the encryption by returning `ABCDEFGHIJKLMNOPQRSTUVWXYZ` as a key.

Here is the (dirty) code:
```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("0.0.0.0", 7143))
sock.listen(0)

i = 0
while 1:
        (conn, addr) = sock.accept()
        print("New conn:", addr)

        # Recv seed
        print("Recv: ", conn.recv(1024))
        conn.send("CRYPT0R:ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        print("Recv: ", conn.recv(1024))
        conn.send("CRYPT0R:ALL_GOOD")
        print("Recv: ", conn.recv(1024))

        print("Try ID ", i)

        # Encode i on 4 bytes and only take the 256 first values
        b = bytearray()
        b.append(i & 0xff)
        b.append(0)
        b.append(0)
        b.append(0)
        conn.send(b"CRYPT0R:VICTIM_ID_IS>" + b)
        print("Recv: ", conn.recv(1024))

        conn.close()

        i = i + 1
```

And now, run the malware until the good victimID is reached...
We see that the process is stuck with high CPU consumption once we get to id 100 until 109:

```
('Try ID ', 99)
('Recv: ', 'CRYPT0R:GET_FINAL_MSG\r\n')
('New conn:', ('192.168.1.24', 14441))
('Recv: ', 'CRYPT0R_SEED:110\r\n')
('Recv: ', 'CRYPT0R_ACK\r\n')
('Recv: ', 'CRYPT0R:GET_VICTIM_ID>{8CA2CE9C-5DAA-4E07-A18D-51FBF33C9268}\r\n')
('Try ID ', 100)
Traceback (most recent call last):
  File "cnc.py", line 29, in <module>
    print("Recv: ", conn.recv(1024))
socket.error: [Errno 104] Connection reset by peer
```

And once we reach `victimID = 144`, we get the flag !

![Flag](https://github.com/HugoDelval/inshack-2018/raw/master/reverse/crypt0r-part-3/img/flag.png)

Challenge solved !
