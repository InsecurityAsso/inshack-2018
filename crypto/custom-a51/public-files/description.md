# Custom A5/1

As crypto expert we designed our own streamcipher that combines two linear elements into a secure design.
It works as follows. The secret key of NONSENSE consists of two invertible matrices K 51 , K 52 ∈ Z 64×64.

To encrypt a plaintext M of l bits, our algorithl takes a 64-bit IV, generates an l-bit key stream k and computes the ciphertext C = M ⊕ k. The keystream is generated in 64-bit blocks as implemented in our open source file.
To enforce a bit more the security, we decided to include IV into the secret key as well, it is incremented after every encryption
query by 1, i.e. IV  = (int(IV) + 1 mod 2^64 i) with limited 64 bits.
You can find here our implementation and here is our incrackable test : `BXkOb8rYcnNpR3db/Ly5cD+EyBJnm8sorjHZTx/yAhUi`
