# Custom A5/1

As crypto expert we designed our own streamcipher that combines two linear elements into a secure design.

It works as follows. The secret key of NONSENSE consists of two invertible matrices <code>K 51 , K 52 &isin; Z 64×64</code>

To encrypt a plaintext <code>M</code> of <code>l</code> bits, our algorithm takes a 64-bit <code>IV</code>, generates an l-bit key stream <code>k</code> and computes the ciphertext <code>C = M &oplus; k</code>. The keystream is generated in 64-bit blocks as implemented in our open source file.

To enforce a bit more the security, we decided to include <code>IV</code> into the secret key as well, it is incremented after every encryption query by 1, i.e. <code>IV  = (int(IV) + 1 mod 2^64 i)</code> with limited 64 bits.

You can find attached our implementation and here is our incrackable test : <code>BXkOb8rYcnNpR3db/Ly5cD+EyBJnm8sorjHZTx/yAhUi</code>
