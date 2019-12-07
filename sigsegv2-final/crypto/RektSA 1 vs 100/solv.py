from pwn import remote
import Cryptodome.Util.number
import gmpy2
import math

gmpy2.get_context().precision=2048

url = "finale-challs.rtfm.re"
port = 9002

re = remote(url, port)

def func(atmp):
    print('\b' * (13 + math.floor(math.log(atmp, 10))) + 'Attempt %d/100' % atmp, end='')

    N = int(re.recvline()[3:-1])
    partial_phi = int(re.recvline()[5:-1])
    r = int(re.recvline()[3:-1])

    Nmr = N // r
    assert N == Nmr * r

    tmp = N // pow(2, 2050)
    for i in range(10):
        phi = (partial_phi + ((tmp - i) * pow(2, 2050)))  
        if phi % (r-1) == 0:
            pq_phi = phi // (r-1) 
            assert pq_phi * (r-1) == phi

            d = Cryptodome.Util.number.inverse(0x10001, phi)

            a = 1
            b = -(Nmr + 1 - pq_phi)
            c = Nmr

            x = gmpy2.sqrt(gmpy2.mpz(b**2 - 4 * c))
            p = int((-b + x) / 2)
            q = int((-b - x) / 2)

            assert q * p * r == N
            assert (q-1) * (p-1) * (r-1) == phi

            re.recvline()
            re.sendline(b'%d %d %d' % (d, p, q))
            return

if __name__ == '__main__':
    for i in range(1, 101):
        func(i)
    print('\b' * 15 + '%s' % re.recvline().decode(), end='')
