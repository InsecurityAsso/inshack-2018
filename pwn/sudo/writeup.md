# pwn | Sudo

The binary provided has the sticky bit set on the server:

```bash
$ ls -la sudo

```

Which means that we will get the `sudo-pwned` permissions while running the program.

What a chance! You need this account to read the `flag.txt` file :D. Let's hack this binary.

The program lets you launch a defined set of binaries based on their a sha256 whitelist. After decompiling the program and extracting the hashes, you can find that these binaries are `ls` and `id`. Nothing really interesting..

The exploit is really straight-forward: there is a race condition in the way the whitelist is checked:

1. the binary given as an argument is opened and read
2. the sha256 sum is computed
3. the computed sum is checked against the whitelist
4. if the sha256 is in the whitelist, the binary is launched

The issue is that the binary can change between step `3` and `4` and you can provide a fake binary to the program :)

```bash
mkdir /tmp/temp
(while true; do ln -fs /bin/cat /tmp/temp/fake_ls; ln -fs /bin/ls /tmp/temp/fake_ls; done;) &
while true; do ./sudo /tmp/temp/fake_ls flag.txt | grep -v flag.txt; done;
```

Please see *exploit/exploit* for the full automated exploit.
