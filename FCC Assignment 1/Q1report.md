# 1.3
- The substitution table obtained by letter frequency analysis 

  Substitution table obtained purely from frequency analysis:
  ```{'V': 'E','O': 'T', 'J': 'A','Z': 'O','I': 'I','L': 'N','H': 'S','W': 'H','E': 'R','Q': 'D','S': 'L','R': 'C','P': 'U','Y': 'M','B': 'W','T': 'F','C': 'G','D': 'Y','M': 'P','X': 'B','U': 'V','N': 'K','G': 'J','F': 'X','K': 'Q','A': 'Z'}```

If we take advantage of ```most common words in English```, we are able to build a more make-sense substitution: (The procedure is displayed in ```hw011-1b.ipynb```)

```{'V': 'E', 'O': 'T', 'E': 'H', 'Z': 'O', 'J': 'A', 'I': 'R', 'Y': 'F', 'L': 'S', 'R': 'U', 'S': 'D', 'B': 'G', 'W': 'N', 'Q': 'L', 'D': 'Y', 'H': 'I', 'C': 'P', 'X': 'W', 'U': 'V', 'P': 'C', 'T': 'F', 'M': 'P', 'N': 'K', 'G': 'J', 'F': 'X', 'K': 'Q', 'A': 'Z'}```

- The key found by brute-force attack

  a = 3, b = 9:

- What you have done in your code step-by-step

#### 1.a Perform the letter frequency analysis attack.

The idea is to calculate the frequency of letters in encrypted code then match with ```letter_freq```

From the format of ```cipher.txt```, only characters are encrypted, 

#### First try: 

We match characters by frequency with those in standard letter frequency table and then decrypt the cipher. But the result is not that readable. 

This situation is resulted from the limitation of cipher text. The calculated frequency is not accurate enough. For the cipher characters with similar frequencies, such as ```('D', 0.017), ('M', 0.017), ('X', 0.017)```, it's hard to determine their original characters. 

So I changed to try to find out its correct matching one by one with the help of most frequent word in English context.

#### Second try: 

First I only use the top two most frequent character mathings, ```dec_dict={'V': 'E','O': 'T'}```, decrypt the cipher and get the following: 

```tEe WZItEeIW JHICZItL QJPN JWD SeBIee ZY LeIUHPeL HW``` 

Based on the above partially decrypted text, I guess ```tEe``` is ```the```, so here we have one more matching ```dec_dict['E'] = 'H'```. The next attractive cipher is ```tZ```, which leads us to add a new matching ```dec_dict['Z']='O'```.

Recursively, with the help of matching list ```dec_dict``` which we got during our fist try, and ```most frequent word list``` in English context, we can gradually decrypt the whole information. Even though the matching list we calculated is not perfectly accurate, it is able to give good reference to us. The ```dec_dict``` is as follows:
```{'V': 'E','O': 'T', 'J': 'A','Z': 'O','I': 'I','L': 'N','H': 'S','W': 'H','E': 'R','Q': 'D','S': 'L','R': 'C','P': 'U','Y': 'M','B': 'W','T': 'F','C': 'G','D': 'Y','M': 'P','X': 'B','U': 'V','N': 'K','G': 'J','F': 'X','K': 'Q','A': 'Z'}```

If we take advantage of ```most common words in English```, we are able to build a more make-sense substitution:

```{'V': 'E', 'O': 'T', 'E': 'H', 'Z': 'O', 'J': 'A', 'I': 'R', 'Y': 'F', 'L': 'S', 'R': 'U', 'S': 'D', 'B': 'G', 'W': 'N', 'Q': 'L', 'D': 'Y', 'H': 'I', 'C': 'P', 'X': 'W', 'U': 'V', 'P': 'C', 'T': 'F', 'M': 'P', 'N': 'K', 'G': 'J', 'F': 'X', 'K': 'Q', 'A': 'Z'}```

Reference:

https://en.wikipedia.org/wiki/Most_common_words_in_English

https://en.wikipedia.org/wiki/Letter_frequency

#### 1.b Affine cipher

Encryption:

> E(x) = ax+b mod 26

Decryption:

> D ( x ) = a^-1 ( x - b ) mod m
a^-1 : modular multiplicative inverse of a modulo m. 
1 = a * a^-1 mod m .


After we conduct brute force attack by running ```python3 hw011-1b.py > result.txt```, we can draw the conclusion that ```a = 3, b = 9``` by scanning the output decryptions. 

The decrypted text only makes sense when ```a = 3, b = 9```.