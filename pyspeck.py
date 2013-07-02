#!/usr/bin/env python

class SPECK:

    #Table 4.1 in http://eprint.iacr.org/2013/404.pdf
    Param = [[32,  64,  16, 4, 7, 2, 22],  #block size 2n, key size mn, word size n, key words m, rot alpha, rot beta, rounds T
             [48,  72,  24, 3, 8, 3, 22],
             [48,  96,  24, 4, 8, 3, 23],
             [64,  96,  32, 3, 8, 3, 26],
             [64,  128, 32, 4, 8, 3, 27],
             [96,  96,  48, 2, 8, 3, 28],
             [96,  144, 48, 3, 8, 3, 29],
             [128, 128, 64, 2, 8, 3, 32],
             [128, 192, 64, 3 ,8, 3, 33],
             [128, 256, 64, 4, 8, 3, 34]]


    def __init__(self, blockSize, keySize):

        initFlag = False
        for c in self.Param:
            if(c[0] == blockSize) and (c[1] == keySize):
                self.blockSize = blockSize
                self.keySize = keySize
                self.n = c[2]
                self.m = c[3]
                self.alpha = c[4]
                self.beta = c[5]
                self.T = c[6]
                self.k = list()
                initFlag = True
                break

        if not initFlag:
            raise Exception("the block/key sizes specified are not supported")


    def S(self, x, j):
        if (j==0):
            return x
        if (j>0):	#left shift
            return ((x<<j) | (x>>(self.n-j))) & ((1<<self.n)-1)
        if (j<0):	#right shift
            j = -1*j
            return ((x>>j) | (x<<(self.n-j))) & ((1<<self.n)-1)


    def add(self, x, y):
        return (x+y)%(1<<self.n)


    def expandKey(self, key):
        l = list()
        self.k.append(key & ((1<<self.n)-1))

        for i in xrange(self.m-1):
            key = key>>self.n;
            l.append(key & ((1<<self.n)-1))

        for i in xrange(self.T-1):
            l.append(self.add(self.k[i], self.S(l[i], -1*self.alpha)) ^ i)
            self.k.append(self.S(self.k[i], self.beta) ^ l[-1])


    def encrypt(self, plaintext):
        assert (plaintext < (1<<(2*self.n))), "plaintext can have at most " + 2*self.n + " bits"
        self.L = (plaintext >> self.n) & ((1<<self.n)-1)
        self.R = plaintext & ((1<<self.n)-1)
        for i in xrange(self.T):
            self.L = self.add(self.S(self.L, -1*self.alpha), self.R) ^ self.k[i]
            self.R = self.S(self.R, self.beta) ^ self.L
        return self.L<<self.n | self.R


    def decrypt(self, ciphertext):
        pass


if __name__== '__main__':
    #Simon32/64
    so = SPECK(32, 64)
    so.expandKey(0x1918111009080100)
    ciphertext = so.encrypt(0x6574694c)
    assert(ciphertext == 0xa86842f2)
    print "1/10 tests are passed"

    #Simon48/72
    so = SPECK(48, 72)
    so.expandKey(0x1211100a0908020100)
    ciphertext = so.encrypt(0x20796c6c6172)
    assert(ciphertext == 0xc049a5385adc)
    print "2/10 tests are passed"

    #Simon48/96
    so = SPECK(48, 96)
    so.expandKey(0x1a19181211100a0908020100)
    ciphertext = so.encrypt(0x6d2073696874)
    assert(ciphertext == 0x735e10b6445d)
    print "3/10 tests are passed"

    #Simon64/96
    so = SPECK(64, 96)
    so.expandKey(0x131211100b0a090803020100)
    ciphertext = so.encrypt(0x74614620736e6165)
    assert(ciphertext == 0x9f7952ec4175946c)
    print "4/10 tests are passed"

    #Simon64/128
    so = SPECK(64, 128)
    so.expandKey(0x1b1a1918131211100b0a090803020100)
    ciphertext = so.encrypt(0x3b7265747475432d)
    assert(ciphertext == 0x8c6fa548454e028b)
    print "5/10 tests are passed"

    #Simon96/96
    so = SPECK(96, 96)
    so.expandKey(0x0d0c0b0a0908050403020100)
    ciphertext = so.encrypt(0x65776f68202c656761737520)
    assert(ciphertext == 0x9e4d09ab717862bdde8f79aa)
    print "6/10 tests are passed"

    #Simon96/144
    so = SPECK(96, 144)
    so.expandKey(0x1514131211100d0c0b0a0908050403020100)
    ciphertext = so.encrypt(0x656d6974206e69202c726576)
    assert(ciphertext == 0x2bf31072228a7ae440252ee6)
    print "7/10 tests are passed"

    #Simon128/128
    so = SPECK(128, 128)
    so.expandKey(0x0f0e0d0c0b0a09080706050403020100)
    ciphertext = so.encrypt(0x6c617669757165207469206564616d20)
    assert(ciphertext == 0xa65d9851797832657860fedf5c570d18)
    print "8/10 tests are passed"

    #Simon128/192
    so = SPECK(128, 192)
    so.expandKey(0x17161514131211100f0e0d0c0b0a09080706050403020100)
    ciphertext = so.encrypt(0x726148206665696843206f7420746e65)
    assert(ciphertext == 0x1be4cf3a13135566f9bc185de03c1886)
    print "9/10 tests are passed"

    #Simon128/256
    so = SPECK(128, 256)
    so.expandKey(0x1f1e1d1c1b1a191817161514131211100f0e0d0c0b0a09080706050403020100)
    ciphertext = so.encrypt(0x65736f6874206e49202e72656e6f6f70)
    assert(ciphertext == 0x4109010405c0f53e4eeeb48d9c188f43)
    print "10/10 tests are passed"