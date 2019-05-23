import sympy
import random
import math


def generate_n(num_digits):
    prime_size = pow(10, num_digits)
    p = sympy.randprime(prime_size, 2 * prime_size)
    q = sympy.randprime(prime_size, 2 * prime_size)
    n = p * q
    phi_of_n = (p - 1) * (q - 1)
    # Since p and q are prime, phi(p) = (p-1) and phi(q) = (q-1)
    # Euler's Totient Function is multiplicative meaning that
    # phi(n) = phi(pq) = phi(p)phi(q) = (p-1)(q-1)
    return n, phi_of_n


def generate_e(num_digits, phi_of_n):
    size = pow(10, num_digits)
    e = random.randint(size, 2*size)
    while math.gcd(e, phi_of_n) != 1:
        e = random.randint(size, 2 * size)
    d = mod_inv(e, phi_of_n)
    return e, d


def extended_gcd(aa, bb):
    # Code taken from https://rosettacode.org/wiki/Modular_inverse#Python
    last_remainder, remainder = abs(aa), abs(bb)
    x, last_x, y, last_y = 0, 1, 1, 0
    while remainder:
        last_remainder, (quotient, remainder) = remainder, divmod(last_remainder, remainder)
        x, last_x = last_x - quotient * x, x
        y, last_y = last_y - quotient * y, y
    return last_remainder, last_x * (-1 if aa < 0 else 1), last_y * (-1 if bb < 0 else 1)


def mod_inv(a, m):
    # Code taken from https://rosettacode.org/wiki/Modular_inverse#Python
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError
    return x % m


def convert_m_to_int(m):
    hex_val = "0x"
    for char in list(m):
        hex_val += format(ord(char), "x")

    hex_int = int(hex_val, 16)
    return hex_int


def convert_m_to_str(m):
    m = str(hex(m))[2:]
    res = ""

    x = 0
    while x < len(m)-1:
        cur_hex_val = m[x] + m[x+1]
        cur_hex_val = int(cur_hex_val, 16)
        res += chr(cur_hex_val)
        x += 2
    return res


def encrypt(m, e, n):
    return pow(m, e, n)


def decrypt(c, d, n):
    return pow(c, d, n)


def main():
    n, phi_of_n = generate_n(50)
    e, d = generate_e(25, phi_of_n)

    m = "Hello, world."
    print("Initial message: " + str(m))
    m_converted = convert_m_to_int(m)

    c = encrypt(m_converted, e, n)
    print("Cipher Text: " + str(c))

    m = decrypt(c, d, n)
    m = convert_m_to_str(m)
    print("Decrypted Message: " + str(m))


if __name__ == "__main__":
    main()