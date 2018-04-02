# On whose authority?

Full writeup to come on https://zoug.top

This is an on-site challenge: a raspberry pi is connected to a wireless network, and you need to get a flag out of this.

You can see that the wireless network is protected by WEP, so it's only a matter of running airmon / aircrack to get the key and connect.

Once you're in, you can listen to traffic using wireshark or a similar tool. You'll quickly see that everything is encrypted! This is not good news, you can't easily see what the raspberry is sending.

Next step is to try a MITM attack: either a tool like ethercap or using arpspoof, to trick the pi into sending you the encrypted request, and not to the gateway. And since you're lucky (and we don't want the chall to be only solvable by the NSA), the raspberry isn't checking the certificates it's getting.

So you can use something like Fiddler or Burp and give it your own certificate. You'll then be able to act as a proxy and see everything the raspberry is sending.

You'll see that it's doing a GET request with an Authorization field, "Basic k7SBjJ2qoKmqQUc5". If you try to access to the website with a normal get request you're greeted with an error message, but if you craft a get request with the same Authorization field, the server returns the flag!

