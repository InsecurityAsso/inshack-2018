### Tricky 2 - WriteUp

You were given an ELF64 binary which used a debugger trap to send the debugged program nowhere.

```
...
0x0000000000401667 <+9> :	mov    esi,0x401586
0x000000000040166c <+14>:	mov    edi,0x5
0x0000000000401671 <+19>:	call   0x401000 <signal@plt>
0x0000000000401676 <+24>:	int3
...
```

We can see a debugger trap `int3` which send a SIGTRAP will lead the program with the debugger attached to some junk section.

Instead we have to look at the function at `0x401586`
```
...
0x00000000004015d8 <+82> :	call   0x401369 <_Z5checkSs>
0x00000000004015dd <+87> :	mov    ebx,eax
0x00000000004015df <+89> :	lea    rax,[rbp-0x20]
0x00000000004015e3 <+93> :	mov    rdi,rax
0x00000000004015e6 <+96> :	call   0x401060 <_ZNSsD1Ev@plt>
0x00000000004015eb <+101>:	test   bl,bl
0x00000000004015ed <+103>:	je     0x40160d <_Z10abort_trapi+135>
...
```

it is calling for a function at `0x401369` and this last one is quite interesting :

```
...
0x00000000004014c8 <+351>:	mov    DWORD PTR [rbp-0x34],0x30
0x00000000004014cf <+358>:	mov    DWORD PTR [rbp-0x30],0x75
0x00000000004014d6 <+365>:	mov    DWORD PTR [rbp-0x2c],0x72
0x00000000004014dd <+372>:	mov    DWORD PTR [rbp-0x28],0x5f
0x00000000004014e4 <+379>:	mov    DWORD PTR [rbp-0x24],0x64
0x00000000004014eb <+386>:	mov    DWORD PTR [rbp-0x20],0x33
0x00000000004014f2 <+393>:	mov    DWORD PTR [rbp-0x1c],0x62
0x00000000004014f9 <+400>:	mov    DWORD PTR [rbp-0x18],0x75
0x0000000000401500 <+407>:	mov    DWORD PTR [rbp-0x14],0x67
0x0000000000401507 <+414>:	mov    DWORD PTR [rbp-0x10],0x67
0x000000000040150e <+421>:	mov    DWORD PTR [rbp-0xc],0x33
0x0000000000401515 <+428>:	mov    DWORD PTR [rbp-0x8],0x72
0x000000000040151c <+435>:	mov    DWORD PTR [rbp-0x4],0x7d
0x0000000000401523 <+442>:	mov    DWORD PTR [rbp-0xd4],0x0
...
```

It is first filling an array with hex values and then checking if each one corresponds to another array.

```
...
0x000000000040152d <+452>:	jmp    0x401576 <_Z5checkSs+525>
0x000000000040152f <+454>:	mov    eax,DWORD PTR [rbp-0xd4]
0x0000000000401535 <+460>:	movsxd rdx,eax
0x0000000000401538 <+463>:	mov    rax,QWORD PTR [rbp-0xe8]
0x000000000040153f <+470>:	mov    rsi,rdx
0x0000000000401542 <+473>:	mov    rdi,rax
0x0000000000401545 <+476>:	call   0x400f30 <_ZNSsixEm@plt>
0x000000000040154a <+481>:	movzx  eax,BYTE PTR [rax]
0x000000000040154d <+484>:	movsx  edx,al
0x0000000000401550 <+487>:	mov    eax,DWORD PTR [rbp-0xd4]
0x0000000000401556 <+493>:	cdqe   
0x0000000000401558 <+495>:	mov    eax,DWORD PTR [rbp+rax*4-0xd0]
0x000000000040155f <+502>:	cmp    edx,eax
0x0000000000401561 <+504>:	setne  al
0x0000000000401564 <+507>:	test   al,al
0x0000000000401566 <+509>:	je     0x40156f <_Z5checkSs+518>
0x0000000000401568 <+511>:	mov    eax,0x0
0x000000000040156d <+516>:	jmp    0x401584 <_Z5checkSs+539>
0x000000000040156f <+518>:	add    DWORD PTR [rbp-0xd4],0x1
0x0000000000401576 <+525>:	cmp    DWORD PTR [rbp-0xd4],0x33
0x000000000040157d <+532>:	jle    0x40152f <_Z5checkSs+454>
0x000000000040157f <+534>:	mov    eax,0x1
...
```

If we construct a string from the hex values, we get the flag.
`INSA{Y0u_sh0uld_kn0w_th4t_1_c4n_tr1ck_y0ur_d3bugg3r}`

You could also have used GDB but for this chall but it was a bit harder
