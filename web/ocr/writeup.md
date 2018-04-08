# OCR
This is a basic code injection. The only unusual factor is the input vector.
Through the source code, you notice the `/debug` url that give you the server source code.
You can notice the `x = open("private/flag.txt").read()` that is an obvious help.
The next obstacle is the cast to int of the eval result, thus the simpler is to get each char one by one by using the `ord` function.
Example text payload is `ord(x[0]) = 4`, notice the second part to respect the conditions.
It's a pain to generate and submit all the pictures, but nothing complicated. Finally you get the flag.
