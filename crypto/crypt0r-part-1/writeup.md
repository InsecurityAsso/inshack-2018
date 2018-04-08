# Crypt0r - part 1

`Our IDS detected an abnormal behavior from one of our user. We extracted this pcap, could you have a look at it?`


We start downloading the pcap file.

```bash
smeriot@smeriot:~/INSA_CTF/2018/crypt0r1$ wget http://crypt0r.challenge-by.ovh/ids_alert_24032018.pcap
--2018-04-08 12:01:08--  http://crypt0r.challenge-by.ovh/ids_alert_24032018.pcap
Resolving crypt0r.challenge-by.ovh (crypt0r.challenge-by.ovh)... 213.186.33.16
Connecting to crypt0r.challenge-by.ovh (crypt0r.challenge-by.ovh)|213.186.33.16|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 2075 (2.0K) [application/vnd.tcpdump.pcap]
Saving to: ‘ids_alert_24032018.pcap’

ids_alert_24032018.pcap                            100%[==================================================================================================================>]   2.03K  --.-KB/s   in 0.003s

2018-04-08 12:01:08 (695 KB/s) - ‘ids_alert_24032018.pcap’ saved [2075/2075]
smeriot@smeriot:~/INSA_CTF/2018/crypt0r1$ ls
ids_alert_24032018.pcap
```

Using the `tcpflow` command, we extract the packet's payloads. The flows are split into 2 files, the queries and the answers.

```bash
smeriot@smeriot:~/INSA_CTF/2018/crypt0r1$ tcpflow -r ids_alert_24032018.pcap
smeriot@smeriot:~/INSA_CTF/2018/crypt0r1$ ls -l
total 16
-rw-r--r-- 1 admin admin  115 Mar 25 14:33 010.008.014.010.49950-010.008.014.012.07143
-rw-r--r-- 1 admin admin  570 Mar 25 14:33 010.008.014.012.07143-010.008.014.010.49950
-rw-r--r-- 1 admin admin    0 Apr  8 12:01 alerts.txt
-rw-r--r-- 1 admin admin 2075 Mar 25 14:38 ids_alert_24032018.pcap
-rw-r--r-- 1 admin admin 3412 Apr  8 12:01 report.xml
```

By looking at the first file, we first see an interesting pattern. the first packet is prefixed with `CRYPT0R` and the following one are prefixed with the same string having a `0` at the same position (`SELYO0E`). We can start mapping the characters and guessing it's a kind of Vigenere with a static mapping with another charset.

```bash
smeriot@smeriot:~/INSA_CTF/2018/crypt0r1$ cat 010.008.014.010.49950-010.008.014.012.07143
CRYPT0R_SEED:58
SELYO0E_PSB
SELYO0E:NAO_HJSOJQ_JF>{A2FS3118-0399-48S7-857S-43D9528DD98F}
SELYO0E:NAO_DJCPX_QTN
```

The first naive algorithm:
```python
mapping = {
    'S': 'C',
    'E': 'R',
    'L': 'Y',
    'Y': 'P',
    'O': 'T',
    'E': 'R',
}

def decode(chain):
    result = ""
    for c in chain:
        if c >= 'A' and c <= 'Z':
            result = result + mapping[c]
        else:
            result = result + c

    return result


res = decode('SELYO0E')
print(res)
```

We can look at the second flow to see if we can infer a bit more about the mapping:

```bash
smeriot@smeriot:~/INSA_CTF/2018/crypt0r1$ cat 010.008.014.012.07143-010.008.014.010.49950
CRYPT0R:PMSFADNIJKBXQCGYWETOVHRULZSELYO0E:PXX_NGGFSELYO0E:HJSOJQ_JF_JT>�SELYO0E:DJCPX_QTN_JT>!!! PXX LGVE DJXAT IPHA MAAC ACSELYOAF !!!

Selyo0e toegba mpsb pcf lgv ngo dvsb*f mvffl. Lgv spccgo faselyo lgve fpop ausayo jd lgv ypl qa $500. #TIGRQAOIAQGCAL pcf J rjxx njha lgv mpsb lgve fpop.

Dgxxgr oiata jctoevsojgct:
- Jctopxx oia oge megrtae, pcf ng og gve yplqaco yxpodgeq: iooy://bu4ifi2zg5etosvk.gcjgc (YSJ-FTT pyyeghaf gds meg).
- Acoae lgve yaetgcpx bal: JCTP{mW9CLVlPjpUtbZFdccPioVV01jdaUeGv}

Oipcbt dge vtjcn ql epctgqrpea.

Rjoi xgha,
Selyo0qpc
```

The answers from the C&C give us a lot of precious information:
- there are lower case characters which are probably mapped the same way since `Selyo0e` is also written in lowercase (which map for `Crypt0r`);
- the string `JCTP{mW9CLVlPjpUtbZFdccPioVV01jdaUeGv}` looks like being the flag, and since the format is `INSA{}`, `JCTP` may stand for `INSA`;
- `iooy://bu4ifi2zg5etosvk.gcjgc` looks like an URL, so the prefix should be `http`, and indeed, `O` is already mapped to `T` and `Y` to `P`, so `I` stands for `H`.

We can then improve the mapping and the algorithm to support the lowercase characters.

```python
diff_lower_upper = ord('a') - ord('A')

def decode(chain):
    result = ""
    for c in chain:
        if c >= 'A' and c <= 'Z':
            if l not in mapping:
                result = result + '?'
            else:
                result = result + mapping[c]
        elif c >= 'a' and c <= 'z':
            l = chr(ord(c) - diff_lower_upper)
            if l not in mapping:
                result = result + '?'
            else:
                result = result + chr(ord(mapping[l]) + diff_lower_upper)
        else:
            result = result + c

    return result
```

Then, try the algorithm on the full flow to check if we can infer a bit more:

```python
res = decode("""
CRYPT0R:PMSFADNIJKBXQCGYWETOVHRULZSELYO0E:PXX_NGGFSELYO0E:HJSOJQ_JF_JT>SELYO0E:DJCPX_QTN_JT>!!! PXX LGVE DJXAT IPHA MAAC ACSELYOAF !!!

Selyo0e toegba mpsb pcf lgv ngo dvsb*f mvffl. Lgv spccgo faselyo lgve fpop ausayo jd lgv ypl qa $500. #TIGRQAOIAQGCAL pcf J rjxx njha lgv mpsb lgve fpop.

Dgxxgr oiata jctoevsojgct:
- Jctopxx oia oge megrtae, pcf ng og gve yplqaco yxpodgeq: iooy://bu4ifi2zg5etosvk.gcjgc (YSJ-FTT pyyeghaf gds meg).
- Acoae lgve yaetgcpx bal: JCTP{mW9CLVlPjpUtbZFdccPioVV01jdaUeGv}

Oipcbt dge vtjcn ql epctgqrpea.

Rjoi xgha,
Selyo0qpc
""")
print(res)
```

```
N?PAS0?:A?C????HI????N?P?RST????Y?CRYPT0R:A??_????CRYPT0R:?ICTI?_I?_IS>CRYPT0R:?INA?_?S?_IS>!!! A?? Y??R ?I??S HA?? ???N ?NCRYPT?? !!!

Crypt0r str??? ?ac? an? y?? ??t ??c?*? ????y. Y?? cann?t ??crypt y??r ?ata ??c?pt i? y?? pay ?? $500. #SH????TH???N?Y an? I ?i?? ?i?? y?? ?ac? y??r ?ata.

?????? th?s? instr?cti?ns:
- Insta?? th? t?r ?r??s?r, an? ?? t? ??r pay??nt p?at??r?: http://??4h?h2??5rstc??.?ni?n (PCI-?SS appr???? ??c ?r?).
- ?nt?r y??r p?rs?na? ??y: INSA{??9NY?yAia?s????nnAht??01i???r??}

Than?s ??r ?sin? ?y rans???ar?.

?ith ????,
Crypt0?an
```

We can guess some more words such as `instructions` and `cannot`, so `G` stands for `O` and `V` for `U`.
We run the algorithm once again:

```
N?PAS0?:A?C????HI????NOP?RSTU???Y?CRYPT0R:A??_?OO?CRYPT0R:?ICTI?_I?_IS>CRYPT0R:?INA?_?S?_IS>!!! A?? YOUR ?I??S HA?? ???N ?NCRYPT?? !!!

Crypt0r stro?? ?ac? an? you ?ot ?uc?*? ?u??y. You cannot ??crypt your ?ata ??c?pt i? you pay ?? $500. #SHO???TH??ON?Y an? I ?i?? ?i?? you ?ac? your ?ata.

?o??o? th?s? instructions:
- Insta?? th? tor ?ro?s?r, an? ?o to our pay??nt p?at?or?: http://??4h?h2?o5rstcu?.onion (PCI-?SS appro??? o?c ?ro).
- ?nt?r your p?rsona? ??y: INSA{??9NYUyAia?s????nnAhtUU01i???rOu}

Than?s ?or usin? ?y ranso??ar?.

?ith ?o??,
Crypt0?an
```

We can notice something really curious. The query `CRYP0R_SEED` has the following answer `PMSFADNIJKBXQCGYWETOVHRULZ`, which once we tries to decode it, looks like the alphabet: `A?C????HI????NOP?RSTU???Y?`.

So, there's a chance `PMSFADNIJKBXQCGYWETOVHRULZ` is the mapping we're looking for. Give it a try.

```python
potential_mapping = "PMSFADNIJKBXQCGYWETOVHRULZ"
mapping = dict()

for i, c in enumerate(potential_mapping):
    mapping[c] = chr(ord('A') + i)
```

Run the algorithm one more time:

```
NWPAS0W:ABCDEFGHIJKLMNOPQRSTUVWXYZCRYPT0R:ALL_GOODCRYPT0R:VICTIM_ID_IS>CRYPT0R:FINAL_MSG_IS>!!! ALL YOUR FILES HAVE BEEN ENCRYPTED !!!

Crypt0r stroke back and you got fuck*d buddy. You cannot decrypt your data except if you pay me $500. #SHOWMETHEMONEY and I will give you back your data.

Follow these instructions:
- Install the tor browser, and go to our payment platform: http://kx4hdh2zo5rstcuj.onion (PCI-DSS approved ofc bro).
- Enter your personal key: INSA{bQ9NYUyAiaXskZDfnnAhtUU01ifeXrOu}

Thanks for using my ransomware.

With love,
Crypt0man
```

Challenge solved, the flag is `INSA{bQ9NYUyAiaXskZDfnnAhtUU01ifeXrOu}`.
