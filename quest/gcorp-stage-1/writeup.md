# G-Corp - stage 1: find and extract (forensics)

You get a description and a Wireshark capture file `exfil.pcap`. According to
the description you need to find info in this capture and extract it for further
analysis.

When opened with Wireshark, the file shows a TCP connection with a lot of data
going through it. Some of this data consists of a plaintext which seems to be a
message from a hacker to another hacker. It actually gives a clue on the content
of the data transferred.

Use follow TCP stream functionality and save the raw data stream into a file.

Run `binwalk -e` on the file you saved. It should be able extract an executable
file that you can run.

