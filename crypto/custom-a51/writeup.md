# Custom A51

Full exploit is available as exploit.sage (it is just made with sage for simpler matrix equation and general syntax).
Basically all you have to do is solve K1 * X1 = Y1 and K2 * X2 = Y2, with K1 and K2 the secret keys.
We can solve these equations since we know the first message and its cipher test, a simple xor between those will give us missing information.
Also consider the fact that we should start with the second block, as the first one is also impacted by the IV, and that you should use 1 over 2 following blocks to respect the algorithm construction.
Once K1 and K2 are computed, it is easy to find the original IV , thus the IV use for the flag encryption.
Just run the algorithm with, K1,K2 and IV to generate the stream that you xor with the base64 decoded encrypted flag to obtain the clear one.
