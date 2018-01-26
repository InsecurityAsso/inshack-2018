# INS'hAck 2018 - The G-Corp Quest

This "quest"-type challenge consists of 4 consecutive challenges to finally 
obtain the flag.

This is how this challenge with sub-challenges must be set-up :

## Stage 1

+ Provide files given in `public-files/` to challengers (description.md + exfil.pcap)
+ See `writeup.md` for resolution. 

## Stage 2

+ Use `server-files/stage_2/dna_decoder_wrapper.py` to start the DNA decoder service.
+ Ensure that `exploit/exploit_stage_2` successfully runs on the service.
+ Security info:
    + Each challenger shall have a unique instance running for him.
    + Each instance shall run in an isolated environnement with limited commands available (whitelisted bellow): 
        + hexdump
        + ls
        + cd
        + pwd
        + echo
    + Each instance *shall be considered fully compromised* by the challenger once 
      the challenge is solved as the vulnerability exploited results in 
      *Arbitrary Command Execution*
 + See `writeup.md` for resolution. 

## Stage 3

 + Nothing needs to be setup on the server side for this stage which consists in decrypting an encoded file.
 + See `writeup.md` for resolution. 

## Stage 4

 + Use `server-files/stage_4/emergency_override_wrapper.py` to start the Emergency Override service.
 + Ensure that `exploit/exploit_stage_4` successfully runs on the service.
 + Security info:
    + There is no need for a unique instance for this stage
 + See `writeup.md` for resolution. 
