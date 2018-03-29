# Not so random
After reading the source code, you can notice that the jackpot number is generated with the secrets module
while the other number is generated with classic Mersenne Twister random.
Mersenne Twister is known to be easily predictable with enough previous states but you can statistically play only twice
before loosing the game.

However, the information of the random state is also given when a non int is given as parameter, therefore you can request as much as needed the program in order to deduce the current state of the generator.

Because there are only 1024 possibilities for the jackpot value, it is easy to bruteforce the md5 hash knowing the random state.
