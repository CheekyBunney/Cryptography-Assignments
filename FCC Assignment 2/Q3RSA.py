import binascii
import random
def get_plaintext(filename: str)->str:
    input = ''
    with open(filename, 'r') as f:
        input = f.read()
    return input
def prime_test(n):
    if(n<=3):
        if (n>1):
            return True
    if(n%2 == 0 or n%3 == 0):
        return False
    for i in range( 5, n, 6):
        if (i ** 2 > n):
            break
        if (n%i == 0 or n % (i+2) == 0):
            return False
    return True
    # Reference: https://en.wikipedia.org/wiki/RSA_(cryptosystem)
def euler_totient(p, q):
    return (p-1)*(q-1)
def euclid(a, b):
    if b == 0:
        return a
    else:
        r = a % b
        return euclid(b, r)
def calculate_e(phi):
    # It's better to choose the largest integer e such that 1 < e < φ(n) and gcd(e, φ(n)) = 1
    # But for speed consideration, we calculate e where 1< e < 1000
    for i in range(2, 1000):
        gcd = euclid(phi, i)
        if gcd == 1:
            e = i
    return e

def extended_euclidean(a, b):
#ref: https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
#ref: https://www.geeksforgeeks.org/euclidean-algorithms-basic-and-extended/
    if a == 0 : 
        return b, 0, 1     
    gcd, x1, y1 = extended_euclidean(b%a, a)
    x = y1 - (b//a) * x1
    y = x1
    return gcd, x, y
def mult_inverse(e, phi):
    gcd, x, y = extended_euclidean(e, phi)
    if (gcd != 1):
        return None
    else:
        return x % phi
def key_schedule():
    p = 0
    q = 0
    while(1):
        #p = random.getrandbits(128)
        p = random.getrandbits(50)
        if(prime_test(p)):
            break
    print(f'p = {p}')
    while(1):
        #q = random.getrandbits(128)
        q = random.getrandbits(50)
        if(prime_test(q)):
            break
    print(f'q = {q}')
    # p = 7919
    # q = 7907
    n = p*q
    phi = euler_totient(p, q)
    e = calculate_e(phi) # released as part of the public key
    d = mult_inverse(e, phi)
    public_key = (e, n)
    private_key = (d, n)
    print("Public Key is:", public_key)
    print("Private Key is:", private_key)
    return public_key, private_key
def text2integer(message, n):
    hex_data = binascii.hexlify(message.encode())
    print('hex data', hex_data)
    
    plaintext_integer = int(hex_data, 16)
    print('plain text integer      ', plaintext_integer)
    if plaintext_integer > n:
        raise Exception('plaintext_integer m > n')

    return plaintext_integer
def encrypt(message, public_key):
    # public key = (e,n)
    e = public_key[0]
    n = public_key[1]
    message_integer = text2integer(message, n)
    # pow() modular exponentiation
    ciphertext_integer = pow(message_integer,  e, n)
    print('ciphertext integer  ', ciphertext_integer)
    return ciphertext_integer
def decrypt(ciphertext_integer, private_key):
    # private key = (d, n)
    d = private_key[0]
    n = private_key[1]
    decrypted_integer = pow(ciphertext_integer, d, n)
    print('decrypted text integer  ', decrypted_integer)
    print('message:\n', binascii.unhexlify(hex(decrypted_integer)[2:]).decode())


# main

# pub_key = (e, n)
# priv_key = (d, n)
pub_key, priv_key = key_schedule()

message = get_plaintext('short-test.txt')
cipher_integer = encrypt(message, pub_key)
decrypt(cipher_integer, priv_key)