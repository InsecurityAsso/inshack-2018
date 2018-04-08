#!/usr/bin/env python2
import numpy as np
from param import K1,K2,IV,flag
import base64

from Crypto.Util import strxor
def xor(a,b):
    return strxor.strxor(a,b)

#K51 and K52 are secrets invertible matrix in Z_2^(64*64), i.e. 64*64 matrix with only 0 and 1
# IV is a binary number incremented for each new message, it is here represented as a column vector of 64 bits
# l is the length of our message and the length of the keystream
def secure_custom(K51,K52,IV,l):
    k=""
    i=0
    S_2=IV
    while i*8<l:
        if i%2 == 0:
            S_2 = K51.dot(S_2)%2
        else :
            S_2 = K52.dot(S_2)%2
        sf = "".join([str(j) for j in S_2])
        sfl = [sf[j:j+8] for j in range(0, len(sf), 8)]
        sfa = "".join(list(map(lambda x : chr(int(x,2)),sfl)))
        k+=sfa
        i+=1
    return k[:l]

## First message is just here to prove that everything works well..
test_message = "Walder Frey eventually holds a hand up to cue the musicians to cease playing, addressing Robb and claiming that he has been negligent in his duties as a host by failing to present his king with a proper wedding gift. At this moment, Roose Bolton gives Catelyn a knowing look and glances towards his arm. Her eyes follow his gaze and she sees a bit of chain mail peaking out from his sleeve. She then lifts up his sleeve which reveals the chain mail he is wearing underneath. Roose smiles ominously and Catelyn realizes that they have been led into a trap: she slaps Roose across the face and then shouts to warn Robb, but it is too late. At Walder Frey's signal, Frey approaches Talisa Stark from behind and begins to repeatedly stab her in the abdomen with a dagger, killing her unborn child instantly and causing her to quickly succumb to her wounds. The musicians hired for the wedding reveal themselves to be a group of assassins, brandishing crossbows and firing on Robb Stark and the Northern leadership gathered in the hall.."
test_cipher='P8t1d0rMgqt/f4uGAg4dpyLxMyIR+JJ4hT8DOVAMX54gBVBwuZvZc0Z5LU+Gz/PHRVoWf+8GCsXaOFdVcY7jnXcQFxjqOOnLOo79TvJywdUw1ceM58fPE3Yso97c8DaKzLzf/lXgMn9AJymOjU6239PWGYn5kHjZ/vTGvIIeP4QGk7pxiD8S00LlyRK5+YWw7i435CfQqpIum8zBJXWGvUOtDADrwXD44Fo3TMOdzJaRiLaElTSPrbpXY8d8y1oFT+bC5jgqME38wesLgcc3JNOQO17hg414WXoNtmLMFw7I8pll1zYzMz4/C8uBUZ+g2MRFjtwWffS1S8DwsFq+9vfJNDXAETUsY+lVY2Ng1yEkRSl/xRuJkkNt0A9G5hi0gkoe3cDDLV6pqdCSBKwBwz7+ywb7TbitEybS5u/qkmOdsfoRfEXHYbclbDpwmd2MQ6HQoJi7jI7tEEz4vGw66gI3YSxx0c8NHTx+mSKgxzZnp270crRy8pU4Azvq/IqiDJyqEV0TLZquJ1DcmaWD4GluUGnK9s63ttuQqsghErR/j+NnPQrg5HjkTxlNVZk0xoTTg7q0uh55HloMs7YUQFizXM1pK9k0Uldu09jslAAQSw63yu0rbqHZuUAzG1jNl8x3nPfz9GjwJDcUVSn3hEz4Edc4iu48P3CBTf/4ZADmzjywMCDdxLn4LUjOao0PbUaeWYOjVwlcaxB6zRdfPalwolwCPcu+FoTi77NuJLyr4sSnS962IhJKGM7zeHkP9obk5dps1Ps9BnjsJYDF2CyC7Qplcf/iB2uW/RnjQnyuK72gIx8tBlYz7Qh1Kn2U03FESlfxk5Y3iaL0oq2P1oHkPeAIa7IEY5YLdMLyn7BNYJiXKdnTT4oOENcmHjteLen+lANqMb3wqj7GLjy6B32Vo8cM046+AEAm0mbNZZcQvBUZtbSTue1+8hg4N3s1MIxmAVwBkJQF32beWzw+QKPgaGyOMv84K43ZsOlOZq6gYx5O9PIfzcDCfIxmlhf83TSj5GCcC18tvyIfFBHWVHdj7l2u65X0M9MRN+/2ttnHVVZ7grUon4wseQGHfV4PDiY2LOk5LKw0t+qLsxHzQ0IodSX0QJH09lXxgDsTuIdY7c7f2nb1DiDiMdCMPPmW/aL7c6EwHJZq5O2OsHeZXLHi3WlxhJ+VAI+qOze1cYspwRncYSGsDJL8YrDtTBC841ngSqAHS/OXOEs8Ui2v2vlprvRjf17Bk/JzulSEvJkrweKO7bI29AdnaEzfWB1afaaxFctqBy/IdVjRaC84ajgUdYApyteFGi767rVTgjWjKTACR49hBmj3DIzKidQOYx3M+Fz8FoLujVK4g5fmGWWvh0eoiaaU'
print(xor(test_message,secure_custom(K1,K2,IV,len(test_message)))==base64.b64decode(test_cipher))

## Now let's encrypt really important content..

IV = np.asarray(list("{0:b}".format(int(reduce(lambda x,y: x+str(y), IV, ''), base=2)+1)),dtype="int")
print base64.b64encode(xor(flag,secure_custom(K1,K2,IV,len(flag))))
# Result : BXkOb8rYcnNpR3db/Ly5cD+EyBJnm8sorjHZTx/yAhUi
