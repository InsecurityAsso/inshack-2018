### Tricky 1 - WriteUp

You were given an ELF64 binary which used a Ptrace to check for debugger presence.

- Fire-up GDB
- Dissasemble main function

Here is what we get :

```
...
0x0000000000400ee0 <+34>:	callq  0x400c20 <ptrace@plt>
0x0000000000400ee5 <+39>:	shr    $0x3f,%rax
0x0000000000400ee9 <+43>:	test   %al,%al
0x0000000000400eeb <+45>:	je     0x400f06 <main+72>
...
```

You now have 2 easy options :
 - (EASY) Patch the binary with an Hex Editor by replacing the `je` instruction (`0x74` in hex) by `jne` (`0x75` in hex)
 - (MEDIUM) Set a breakpoint at the `test` and modify the EFLAGS

Now we can debug. Here is the crucial test :
```
...
0x0000000000400f5a <+156>:	callq  0x400c00 <_ZNSsD1Ev@plt>
0x0000000000400f5f <+161>:	test   %bl,%bl
0x0000000000400f61 <+163>:	je     0x400f81 <main+195>
...
```

Let's break on `0x0000000000400f5f`
Run it and input `AAAA` or whatever as the flag and check what our input is compared with : `INSA{CXX_1s_h4rd3r_f0r_st4t1c_4n4l1sys_wh3n_d3bugg3r_f41ls}`
