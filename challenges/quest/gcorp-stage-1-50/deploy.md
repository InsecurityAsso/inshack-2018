# G-Corp - stage 1

## Deploy

+ Provide files given in `public-files/` to challengers.
+ See `writeup.md` for resolution.

## Rebuild

This must be done each time stage 2 is built again.

+ Create a VM and inside it start a wireshark capture
+ Start a listener using netcat on port 4242 of the VM
+ Then call `cd src/ && ./send.sh` from here in the host
+ Stop the capture, save it as exfil.pcap and add it to the repo.

