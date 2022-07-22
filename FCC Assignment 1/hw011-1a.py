from collections import Counter
letter_freq = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}

#ref: https://en.wikipedia.org/wiki/Letter_frequency

letter_count = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}
def readfile(path):
    f = open(path, "r")
    text = f.read()
    f.close()
    return text
def calc_letter_freq(cipher:str)->list: #calculate letter freq and return sorted tuple list. 
    clean_cipher = ''
    sum = 0
    for i in cipher:
        if ord(i)>=ord('A') and ord(i)<=ord('Z'):
            clean_cipher+=i
            sum+=1
    #print(Counter(clean_cipher).most_common(26))
    cipher_letter_freq = []
    for t in Counter(clean_cipher).most_common(26):
        cipher_letter_freq.append((t[0], round(t[1]/sum, 3)))
    #print(cipher_letter_freq)
    #return Counter(clean_cipher).most_common(26)
    return cipher_letter_freq
def get_decrypt_dict(letter_freq: dict, cipher_letter_freq: list)->dict:
    dec_dict = {}
    for index, letter in enumerate(letter_freq.keys()):
        dec_dict[cipher_letter_freq[index][0]]=letter
    return dec_dict
def decrypt_and_output(cipher, dec_dict):
    decrypt_text = ''
    for i in cipher:
        if ord(i)>=ord('A') and ord(i)<=ord('Z'):
            i = dec_dict[i]
        decrypt_text += i
    print(decrypt_text.lower())
cipher = readfile('cipher.txt').upper() 
cipher_letter_freq = calc_letter_freq(cipher)
dec_dict = get_decrypt_dict(letter_freq, cipher_letter_freq)
print('---------------------------')
print(f'Sorted character frequencies in cipher:\n{cipher_letter_freq}')
print('---------------------------')
decrypt_and_output(cipher, dec_dict)
print('-----------------------')
print(f'substitution table:\n{dec_dict}')

