import numpy as np

def drop_parity_bits(key)->str:
    # drop bits: 8, 16, 24, ... , 64
    return key[0:7]+key[8:15]+key[16:23]+key[24:31]+key[32:39]+key[40:47]+key[48:55]+key[56:63]

# Permute function to rearrange the bits
def permutation(source, rearrange_table, size_n):
    permutation = ""
    for i in range(0, size_n):
        permutation = permutation + source[rearrange_table[i] - 1]
    return permutation
def initial_permutation(plaintext, initial_perm):
    return permute(plaintext, initial_perm, 64)
def generate_final_perm_table(initial_perm):
    final_perm = [i for i in range(64)]
    for index, value in enumerate(initial_perm):
        final_perm[value-1]=index+1
    return final_perm
def final_permutation(text, initial_perm):
    final_perm = generate_final_perm_table(initial_perm)
    return permute(text, final_perm, 64)
def f_func(half, subkey):
    #  Expansion: the 32-bit half-block is expanded to 48 bits using the expansion permutation
    expanded_half = permute(half, expansion_table, 48)
        
    # Key mixing: the result is combined with a subkey using an XOR operation.
    xor_x = xor(expanded_half, subkey)

    # Substitution: after mixing in the subkey, the block is divided into eight 6-bit pieces before processing by the S-boxes
    sbox_str = s_box_substitution(xor_x)
            
    # Permutation: finally, the 32 outputs from the S-boxes are rearranged according to a fixed permutation, the P-box 
    sbox_str = permute(sbox_str, per, 32)
    return sbox_str

def s_box_substitution(mixedkey): # each 6-bits block in the input is converted to a 4-bits block
    sbox_str = ""
    ##col
    col_num = {'0000': 0, '0001': 1, '0010':2, '0011': 3, '0100': 4, '0101': 5, 
        '0110': 6, '0111': 7, '1000': 8, '1001': 9, '1010': 10, '1011': 11, 
         '1100': 12, '1101': 13, '1110': 14, '1111': 15}
    ##row
    row_num = {'00': 0, '01': 1, '10': 2, '11': 3}
    for j in range(0, 8):
        row = row_num[mixedkey[j * 6] + mixedkey[j * 6 + 5]]
        col = col_num[mixedkey[j * 6 + 1] + mixedkey[j * 6 + 2] + mixedkey[j * 6 + 3] + mixedkey[j * 6 + 4]]
        # row = bin2dec(int(mixedkey[j * 6] + mixedkey[j * 6 + 5]))
        # col = bin2dec(int(mixedkey[j * 6 + 1] + mixedkey[j * 6 + 2] + mixedkey[j * 6 + 3] + mixedkey[j * 6 + 4]))
        decimal_value = sbox[j][row][col]
        sbox_str = sbox_str + dec2bin(decimal_value)
    return sbox_str
def key_schedule(key):
    thiskey = key
    subkeys = []
    for i in range(0, 16):
        left = thiskey[0:28]
        right = thiskey[28:56]
        left = rotation(left, rotation_table[i])
        right = rotation(right, rotation_table[i])
        thiskey = left+right
        subkeys.append(permute(thiskey, key_comprasion_table, 48))
    return subkeys

def DES_encrypt(plaintext, subkeys):
    plaintext = initial_permutation(plaintext, initial_perm)
    left = plaintext[0:32]
    right = plaintext[32:64]
    # 16-round processing
    for i in range(0, 16):
            # f_function
            sbox_str = f_func(right, subkeys[i])

            # XOR left and sbox_str
            result = xor(left, sbox_str)
            left = result
            
            # Swap
            if(i != 15):
                left, right = right, left 

    # Final permutaion
    b_cipher_text = final_permutation(left+right, initial_perm)


    return b_cipher_text # in binary

def DES_decrypt(cipher_text, subkeys_reverse):
    return DES_encrypt(cipher_text, subkeys_reverse)

# Hexdecimal to binary conversion
def hex2bin(hex_key):
    dic = {'0' : "0000", '1' : "0001", '2' : "0010", '3' : "0011", '4' : "0100", '5' : "0101", '6' : "0110", '7' : "0111", '8' : "1000", '9' : "1001", 'A' : "1010", 'B' : "1011", 'C' : "1100", 'D' : "1101", 'E' : "1110", 'F' : "1111" }
    output = ""
    for i in range(len(hex_key)):
        output += dic[hex_key[i]]
    return output

	
# Binary to hexadecimal conversion
def bin2hex(binary):
	mapping = {"0000" : '0', "0001" : '1', "0010" : '2', "0011" : '3', "0100" : '4', "0101" : '5', "0110" : '6', "0111" : '7', "1000" : '8', "1001" : '9',
		"1010" : 'A', "1011" : 'B', "1100" : 'C', "1101" : 'D', "1110" : 'E', "1111" : 'F' }
	hex = ""
	for i in range(0,len(binary),4):
		ch = binary[i] + binary[i + 1] + binary[i + 2] + binary[i + 3]
		hex += mapping[ch]
	return hex
def readfile(path):
    f = open(path, "r")
    text = f.read()
    f.close()
    return text
def bin2ascii(binary):
    string = ''
    for i in range(0, len(binary), 8):
        thisbyte = binary[i : i + 8]
        string += chr(int(thisbyte, 2))
    return string
def ascii2bin(plaintext):
    return ''.join(format(ord(i), '08b') for i in plaintext)

# Permutation
def permute(source, rearrange_table, size_n): 
	permutation = ""
	for i in range(0, size_n):
		permutation = permutation + source[rearrange_table[i] - 1]
	return permutation

# rotate the bits towards left by nth bit	
def rotation(key, n):
    rotated = ''
    rotated = key[int(n):] + key[0:int(n)]
    return rotated
# Binary to decimal conversion
def bin2dec(binary):
	binary1 = binary
	decimal, i, n = 0, 0, 0
	while(binary != 0):
		dec = binary % 10
		decimal = decimal + dec * pow(2, i)
		binary = binary//10
		i += 1
	return decimal

# Decimal to binary conversion
def dec2bin(num):
	res = bin(num).replace("0b", "")
	if(len(res)%4 != 0):
		div = len(res) / 4
		div = int(div)
		counter =(4 * (div + 1)) - len(res)
		for i in range(0, counter):
			res = '0' + res
	return res
def arbitrary_input_handler(plaintext):
    #----------------------#
    # Paddding or chopping #
    #----------------------#
    cipher_text = ''

    if len(plaintext) % 64 == 0:
        # adding 64 bits. the last 16 bits are '64' in ascii.
        plaintext += '0000000000000000000000000000000000000000000000000011011000110100'
    else: #padding
        r = len(plaintext) % 64
        # the first r bits in the last 64 bits are part of plaintext.
        b_padded = ''
        if r == 8:
            b_padded = ascii2bin('08')
        else:
            b_padded = ascii2bin(str(r))
        b_padded = '0' * (64-r-len(b_padded)) + b_padded
        #print(f'b_padded: {b_padded}')
        plaintext += b_padded

    return plaintext

# binary a xor binary b
# def xor(a, b):
# 	result = ""
# 	for i in range(len(a)):
# 		if a[i] == b[i]:
# 			result += "0"
# 		else:
# 			result += "1"
# 	return result
def xor(a, b):
    y = int(a,2) ^ int(b,2)
    y = '{0:0{1}b}'.format(y,len(a))
    return y
def output(cipher_text, outputfile, flag='hex'):
    if flag == 'hex':
        with open(outputfile, 'w') as f:
            f.write(bin2hex(cipher_text))
    if flag == 'ascii':
        with open(outputfile, 'w') as f:
            f.write(bin2ascii(cipher_text))
if __name__ == "__main__":
    # Expansion: 32->48
    expansion_table = [32, 1 , 2 , 3 , 4 , 5 , 4 , 5, 
                    6 , 7 , 8 , 9 , 8 , 9 , 10, 11, 
                    12, 13, 12, 13, 14, 15, 16, 17, 
                    16, 17, 18, 19, 20, 21, 20, 21, 
                    22, 23, 24, 25, 24, 25, 26, 27, 
                    28, 29, 28, 29, 30, 31, 32, 1 ]

    # 32-bit Permutaion Table: 
    per = [element+1 for element in list(np.random.permutation(32))]

    # Initial Permutation Table: 64 bits
    initial_perm = [58, 50, 42, 34, 26, 18, 10, 2, 
                60, 52, 44, 36, 28, 20, 12, 4, 
                62, 54, 46, 38, 30, 22, 14, 6, 
                64, 56, 48, 40, 32, 24, 16, 8, 
                57, 49, 41, 33, 25, 17, 9, 1, 
                59, 51, 43, 35, 27, 19, 11, 3, 
                61, 53, 45, 37, 29, 21, 13, 5, 
                63, 55, 47, 39, 31, 23, 15, 7]

    # Rotation table
    # Both halves are rotated left by one or two bits (specified for each round)
    rotation_table = [1, 1, 2, 2, 
                    2, 2, 2, 2, 
                    1, 2, 2, 2, 
                    2, 2, 2, 1 ]

    # Key Compression Table :  56 bits -> 48 bits
    # Discard: 8, 12, 17, 29, 30, 41, 44, 53
    key_comprasion_table = [14, 17, 11, 24, 1, 5, 
                            3, 28, 15, 6, 21, 10, 
                            23, 19, 12, 4, 26, 8, 
                            16, 7, 27, 20, 13, 2, 
                            41, 52, 31, 37, 47, 55, 
                            30, 40, 51, 45, 33, 48, 
                            44, 49, 39, 56, 34, 53, 
                            46, 42, 50, 36, 29, 32 ]
    # S-box Table 
    #Reference:
    # S-boxes are from: https://en.wikipedia.org/wiki/DES_supplementary_material#Substitution_boxes_(S-boxes)
    sbox =  [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7], 
          [ 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8], 
          [ 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0], 
          [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13 ]],
             
         [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10], 
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5], 
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15], 
           [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9 ]], 
    
         [ [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8], 
           [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1], 
           [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7], 
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12 ]], 
        
          [ [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15], 
           [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9], 
           [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4], 
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14] ], 
         
          [ [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9], 
           [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6], 
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14], 
           [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3 ]], 
        
         [ [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11], 
           [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8], 
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6], 
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13] ], 
          
          [ [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1], 
           [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6], 
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2], 
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12] ], 
         
         [ [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7], 
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2], 
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8], 
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11] ] ]
    plaintext = readfile('DES-test.txt')
    plaintext = ascii2bin(plaintext) # binary plaintext
    #print(f'plaintext: {bin2ascii(plaintext)}')

    key = "1011101010111011000010010101101100100111101101101100110011011101" #  hard-coded 64 bits

    #----------------------#
    # Paddding or chopping #
    #----------------------#
    plaintext = arbitrary_input_handler(plaintext)
    #----------------#
    # DES Encryption #
    #----------------#
    b_cipher_text = ''
    key = drop_parity_bits(key) # 64->56 bits key
    subkeys = key_schedule(key) # 16 subkeys in binary format
    for i in range(0, len(plaintext), 64):
        b_cipher_text += DES_encrypt(plaintext[i: i+64], subkeys)
    print(f'hexdecimal cipher text is in DES-cipher-hex.txt')
    print(f'ascii cipher text is in DES-cipher-ascii.txt')
    output(b_cipher_text, 'DES-cipher-ascii.txt', 'ascii')
    output(b_cipher_text, 'DES-cipher-hex.txt', 'hex')
    #----------------#
    # DES Decryption #
    #----------------#
    b_decrypted_text = ''
    subkeys.reverse()
    for i in range(0, len(b_cipher_text), 64):
        b_decrypted_text += DES_decrypt(b_cipher_text[i: i+64], subkeys)
    
    #check last 16 bits to determine if it has padding
    if bin2ascii(b_decrypted_text[-16:]) == '64': # no padding
        b_decrypted_text = b_decrypted_text[:-64]
        # print(f'decrypted text is in DES-decrpted.txt')
        output(b_decrypted_text, 'DES-decrpted.txt', 'ascii')
    else: # plaintext is padded
        r = int(bin2ascii(b_decrypted_text[-16:]))
        b_decrypted_text = b_decrypted_text[:-64+r]
        print(f'decrypted text is in DES-decrpted-ascii.txt')
        output(b_decrypted_text, 'DES-decrpted-ascii.txt', 'ascii')
    #------#
    # DONE #
    #------#
# Ref:
# https://en.wikipedia.org/wiki/DES_supplementary_material#Substitution_boxes_(S-boxes)



    


