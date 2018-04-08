# Base 65536
Each pair of char is converted to binary and concatenate to give a new number between 0 and 65536.
Then a random association is made between each number in the range and a unicode character (see the code for complete procedure).

Because each pair of char correspond to one character, it is easy to ask for the association of every possible pair of char,
then a reverse dictionnary lookup give the flag. 
