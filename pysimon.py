#!/usr/bin/env python

class SIMON:

    #Table 3.1 in http://eprint.iacr.org/2013/404.pdf
    Param = [[32,  64,  16, 4, 0, 32],  #block size 2n, key size mn, word size n, key words m, const seq, rounds T
             [48,  72,  24, 3, 0, 36],
             [48,  96,  24, 4, 1, 36],
             [64,  96,  32, 3, 2, 42],
             [64,  128, 32, 4, 3, 44],
             [96,  96,  48, 2, 2, 52],
             [96,  144, 48, 3, 3, 54],
             [128, 128, 64, 2, 2, 68],
             [128, 192, 64, 3 ,3, 69],
             [128, 256, 64, 4, 4, 72]]

    #const sequence used in key expanding
    Z = [
        [1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0],
        [1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0],
        [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
        [1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1],
        [1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1]
    ]


    def __init__(self, blockSize, keySize):

        initFlag = False
        for c in self.Param:
            if(c[0] == blockSize) and (c[1] == keySize):
                self.blockSize = blockSize
                self.keySize = keySize
                self.n = c[2]
                self.m = c[3]
                self.idx = c[4]
                self.T = c[5]
                self.k = list()
                initFlag = True
                break

        if not initFlag:
            raise Exception("the block/key sizes specified are not supported")


    #left circular shift by j bits.
    def S(self, x, j):
        if (j==0):
            return x
        if (j>0):	#left shift
            return ((x<<j) | (x>>(self.n-j))) & ((1<<self.n)-1)
        if (j<0):	#right shift
            j = -1*j
            return ((x>>j) | (x<<(self.n-j))) & ((1<<self.n)-1)


    def expandKey(self, key):
        c = (1<<self.n) - 4
        if self.m == 2:
            self.k.append(key & ((1<<self.n)-1))
            self.k.append((key>>self.n) & ((1<<self.n)-1))
            for i in xrange(self.T-self.m):
                tmp = self.S(self.k[i+1], -3)
                self.k.append(c ^ self.Z[self.idx][i] ^ self.k[i] ^ tmp ^ self.S(tmp, -1))
        elif self.m == 3:
            self.k.append(key & ((1<<self.n)-1))
            self.k.append((key>>self.n) & ((1<<self.n)-1))
            self.k.append((key>>(2*self.n)) & ((1<<self.n)-1))
            for i in xrange(self.T-self.m):
                tmp = self.S(self.k[i+2], -3)
                self.k.append(c ^ self.Z[self.idx][i] ^ self.k[i] ^ tmp ^ self.S(tmp, -1))
        elif self.m == 4:
            self.k.append(key & ((1<<self.n)-1))
            self.k.append((key>>self.n) & ((1<<self.n)-1))
            self.k.append((key>>(2*self.n)) & ((1<<self.n)-1))
            self.k.append((key>>(3*self.n)) & ((1<<self.n)-1))
            for i in xrange(self.T-self.m):
                tmp = self.S(self.k[i+3], -3) ^ self.k[i+1]
                self.k.append(c ^ self.Z[self.idx][i] ^ self.k[i] ^ tmp ^ self.S(tmp, -1))
        else:
            raise Exception("undefined key expanding for m=" + self.m)


    def f(self, x):
        return self.S(x, 1) & self.S(x, 8) ^ self.S(x, 2)


    def encrypt(self, plaintext):
        assert (plaintext < (1<<(2*self.n))), "plaintext can have at most " + 2*self.n + " bits"
        self.L = (plaintext >> self.n) & ((1<<self.n)-1)
        self.R = plaintext & ((1<<self.n)-1)
        for i in xrange(self.T):
            tmp = self.L
            self.L = self.R ^ self.f(self.L) ^ self.k[i]
            self.R = tmp
        return self.L<<self.n | self.R


    def decrypt(self, ciphertext):
        pass


if __name__== '__main__':
    #Simon32/64
    so = SIMON(32, 64)
    so.expandKey(0x1918111009080100)
    ciphertext = so.encrypt(0x65656877)
    assert(ciphertext == 0xc69be9bb)
    print "1/10 tests are passed"

    #Simon48/72
    so = SIMON(48, 72)
    so.expandKey(0x1211100a0908020100)
    ciphertext = so.encrypt(0x6120676e696c)
    assert(ciphertext == 0xdae5ac292cac)
    print "2/10 tests are passed"

    #Simon48/96
    so = SIMON(48, 96)
    so.expandKey(0x1a19181211100a0908020100)
    ciphertext = so.encrypt(0x72696320646e)
    assert(ciphertext == 0x6e06a5acf156)
    print "3/10 tests are passed"

    #Simon64/96
    so = SIMON(64, 96)
    so.expandKey(0x131211100b0a090803020100)
    ciphertext = so.encrypt(0x6f7220676e696c63)
    assert(ciphertext == 0x5ca2e27f111a8fc8)
    print "4/10 tests are passed"

    #Simon64/128
    so = SIMON(64, 128)
    so.expandKey(0x1b1a1918131211100b0a090803020100)
    ciphertext = so.encrypt(0x656b696c20646e75)
    assert(ciphertext == 0x44c8fc20b9dfa07a)
    print "5/10 tests are passed"

    #Simon96/96
    so = SIMON(96, 96)
    so.expandKey(0x0d0c0b0a0908050403020100)
    ciphertext = so.encrypt(0x2072616c6c69702065687420)
    assert(ciphertext == 0x602807a462b469063d8ff082)
    print "6/10 tests are passed"

    #Simon96/144
    so = SIMON(96, 144)
    so.expandKey(0x1514131211100d0c0b0a0908050403020100)
    ciphertext = so.encrypt(0x74616874207473756420666f)
    assert(ciphertext == 0xecad1c6c451e3f59c5db1ae9)
    print "7/10 tests are passed"

    #Simon128/128
    so = SIMON(128, 128)
    so.expandKey(0x0f0e0d0c0b0a09080706050403020100)
    ciphertext = so.encrypt(0x63736564207372656c6c657661727420)
    assert(ciphertext == 0x49681b1e1e54fe3f65aa832af84e0bbc)
    print "8/10 tests are passed"

    #Simon128/192
    so = SIMON(128, 192)
    so.expandKey(0x17161514131211100f0e0d0c0b0a09080706050403020100)
    ciphertext = so.encrypt(0x206572656874206e6568772065626972)
    assert(ciphertext == 0xc4ac61effcdc0d4f6c9c8d6e2597b85b)
    print "9/10 tests are passed"

    #Simon128/256
    so = SIMON(128, 256)
    so.expandKey(0x1f1e1d1c1b1a191817161514131211100f0e0d0c0b0a09080706050403020100)
    ciphertext = so.encrypt(0x74206e69206d6f6f6d69732061207369)
    assert(ciphertext == 0x8d2b5579afc8a3a03bf72a87efe7b868)
    print "10/10 tests are passed"