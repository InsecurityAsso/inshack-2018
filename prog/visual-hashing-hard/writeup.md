# Visual hashing - hard mode

Download the source code of the extension (.crx file), there are online tools to do that. 

Then, find the function that corresponds to applying visual hashing. 

```javascript
passwordHash = randomizeHash(passwordHash);

for (var hashBandX = 0; hashBandX < 4; hashBandX++) {
	context.fillStyle='#' + passwordHash.substr(hashBandX*6,6);
	context.fillRect(hashBandX/4*inputWidth,0,inputWidth/4,inputHeight);
	
	context.fillStyle='#000000';
	context.fillRect(((hashBandX+1)/4*inputWidth)-1,0,2,inputHeight);
}
```

passwordHash is simply the SHA1 of the password in the input field.

We can see the hash is "randomized", while actually every byte of it is just shifted randomly by a value between -3 and +3.

My guess is that it's made so the hash is visually identical every time, but you can't get exactly the password's SHA1 if you have the precise color values (and run it through a rainbow table).

```javascript
function randomizeHash(passwordHash) {
    // Add a little bit of randomness to each byte
    for (var byteIdx = 0; byteIdx < passwordHash.length/2; byteIdx++) {
        var byte = parseInt(passwordHash.substr(byteIdx*2,2),16);
        // +/- 3, within 0-255
        byte = Math.min(Math.max(byte + parseInt(Math.random()*6)-3,0),255);
        var hexStr = byte.toString(16).length == 2 ? byte.toString(16) : '0' + byte.toString(16);
        passwordHash = passwordHash.substr(0,byteIdx*2) + hexStr + passwordHash.substr(byteIdx*2+2);
    }
    return passwordHash;
}
```

The visual hash image is corrupted pretty hard, but no need to restore it as the four colors of the hash are still there.

On the image, we see 11 dots, so the password must be 5 lowercase letters encapsulated by INSA{}. That makes it 26^5 different values, which is bruteforcable.

We have to allow for a bit of variation on the values on every hash byte since the randomizeHash function modifies it a bit.

```python
import hashlib
import time

pwd=[29,156,13,181,88,85,188,100,120,160,71,201] #Hash bytes in order (RGBRGBRGBRGB)

starter=time.time()
sid=-1
while True:
    sid+=1
    stmp = sid
    flag=''
    while stmp:
        flag+=chr(ord('a')+stmp%26)
        stmp/=26
    while len(flag)!=5:
        flag+='a'
    flag=flag[::-1]
    h=hashlib.sha1('INSA{%s}'%flag).hexdigest()
    for pair in zip(pwd,[int(h[x:x+2],16) for x in range(0,6*4,2)]):
        if abs(pair[0]-pair[1])>3:
            break
    else:
        print 'INSA{%s}'%flag
        break
    
print time.time()-starter
```

After 212 seconds (I have a toaster PC), the script finds a match for the password, `INSA{hctib}`.

Alternatively, you can run the bruteforce in a browser using Selenium or JS.