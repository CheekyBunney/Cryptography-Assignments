def readfile(path):
    f = open(path, "r")
    text = f.read()
    f.close()
    return text
def get_inverse(a):
    # a in [1, 25]
    for cand in range(1,26):
        if (cand * a)%26 == 1:
            return cand
    return -1
def brute_force_affine(affine_cipher):
    # enc = ax+b; x = a^-1 ( Enc - b ) mod m
    
    for a in range(1, 26):
        for b in range(26):
            decipher = ''
            for i in affine_cipher.upper():
                if ord(i) >= ord('A') and ord(i) <= ord('Z'): # i is letter
                    # find the inverse a^-1, which a a^-1 = 1 mode m
                    inverse = get_inverse(a)
                    if inverse > -1: # inverse found
                        i = (ord(i) - ord('A') - b) * inverse % 26# 0-25
                        i = chr(i+ord('A')).lower()
                    else:
                        print(f'no inverse when a={a}')
                    #print(f'i is ascii number {i}')
                decipher += i
            #if(' the ' in decipher):
            print('------------------')
            print(f'a = {a}, b = {b}')
            print(decipher)
            print('------------------')
            print('The decrypted text only makes sense when a = 3, b = 9.')


affine_cipher = readfile('cipher.txt')
brute_force_affine(affine_cipher)