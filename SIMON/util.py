WS = 16
#Z = 0b11011011101011000110010111100000010010001010011100110100001111    #Z3,
Z = 0b11111010001001010110000111001101111101000100101011000011100110    #Z0, SIMON32/64

ROT = [8, 1, 2]
ROUNDS = 32
#MASTER_KEY = 0x1b1a1918131211100b0a090803020100
MASTER_KEY = 0x1918111009080100


#左移
def rotl(n, d, SZ = WS):
    d %= SZ
    if(d<0):
        d += SZ
    return ((n << d)%(1 << SZ)) | (n >> (SZ - d))

#右移
def rotr(n, d, SZ = WS):
    d %= SZ
    if(d<0):
        d+= SZ
    return (n >> d)|((n << (SZ - d))%(1<<SZ))

#
def f(x, SZ = WS):
    return ((rotl(x, 1, SZ)&rotl(x, 8, SZ))^rotl(x, 2, SZ))

#
def get(a, n):
    return (a>>n)&1

#
def convert(a, SZ = WS):
    ret = 0
    for i in range(SZ):
            ret += (2**i)*a[i]
    return ret

#
def convert2(a,SZ=WS):
    """Converts a list into an int, with rightmost bit being least value"""
    return convert(a[::-1], SZ)

#
def arr(a, SZ = WS):
    ret = []
    for i in range(SZ):
            ret.append(get(a, i))
    return ret

#
def compose(l, r, SZ = WS):
    return r + (l<<SZ)

#
def split(x, SZ = WS):
    return (x>>SZ), ((x)%(1<<SZ))

#
def flip(x, SZ = WS):
    return (1<<SZ) - 1 - x

#
def wt(x):
    return bin(x).count("1")


