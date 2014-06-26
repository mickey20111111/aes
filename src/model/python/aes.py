#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#=======================================================================
#
# aes.py
# ------
# Simple, pure Python model of the AES block cipher. The model is
# used as a reference for the HW implementation. The code follows
# the structure of the HW implementation as much as possible.
#
#
# Author: Joachim Strömbergson
# Copyright (c) 2014, Secworks Sweden AB
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or 
# without modification, are permitted provided that the following 
# conditions are met: 
# 
# 1. Redistributions of source code must retain the above copyright 
#    notice, this list of conditions and the following disclaimer. 
# 
# 2. Redistributions in binary form must reproduce the above copyright 
#    notice, this list of conditions and the following disclaimer in 
#    the documentation and/or other materials provided with the 
#    distribution. 
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS 
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE 
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, 
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#=======================================================================

#-------------------------------------------------------------------
# Python module imports.
#-------------------------------------------------------------------
import sys


#-------------------------------------------------------------------
# Constants.
#-------------------------------------------------------------------
AES_128_KEYSIZE = 128
AES_192_KEYSIZE = 192
AES_256_KEYSIZE = 256

AES_128_ROUNDS = 10
AES_192_ROUNDS = 12
AES_256_ROUNDS = 14

AES_ENCIPHER = 1
AES_DECIPHER = 0

AES_128_BIT_KEY = 0
AES_192_BIT_KEY = 1
AES_256_BIT_KEY = 2

VERBOSE = True


#-------------------------------------------------------------------
# AES()
#
# AES class. Implements AES with 128, 192 and 256 bit keys.
# Implements encryption and decryption, but only ECB mode.
# All inputs and ouputs are 32-bit big endian words.
#-------------------------------------------------------------------
class AES():
    # The AES sbox.
    sbox = [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5,
            0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
            0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0,
            0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
            0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc,
            0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
            0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a,
            0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
            0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0,
            0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
            0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b,
            0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
            0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85,
            0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
            0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5,
            0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
            0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17,
            0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
            0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88,
            0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
            0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c,
            0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
            0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9,
            0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
            0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6,
            0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
            0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e,
            0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
            0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94,
            0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
            0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68,
            0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]

    # The AES inverse sbox.
    isbox = [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38,
             0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
             0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87,
             0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
             0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d,
             0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
             0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2,
             0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
             0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16,
             0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
             0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda,
             0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
             0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a,
             0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
             0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02,
             0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
             0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea,
             0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
             0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85,
             0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
             0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89,
             0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
             0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20,
             0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
             0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31,
             0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
             0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d,
             0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
             0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0,
             0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
             0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26,
             0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d]


    #---------------------------------------------------------------
    # __init__
    #
    # Simply create an instance with the internal state cleared.
    #---------------------------------------------------------------
    def __init__(self, verbose = 0):
        self.verbose = verbose
        self.S = [[0] * 4 for i in range(4)]


    #---------------------------------------------------------------
    # init()
    #
    # Initialize the instance with the given key. Note that we
    # do support reinitialize with keys of different sizes.
    #---------------------------------------------------------------
    def init(self, key):
        self.keylen = (8 * len(key))
        if self.keylen not in [AES_128_KEYSIZE, AES_192_KEYSIZE, AES_256_KEYSIZE]:
            print("Key is %d bits, not 128, 192 or 256 bits long." % (self.keylen))
            return 0

        self.key = key

        if self.keylen == AES_128_KEYSIZE:
            self.num_rounds = AES_128_ROUNDS
        if self.keylen == AES_192_KEYSIZE:
            self.num_rounds = AES_192_ROUNDS
        if self.keylen == AES_256_KEYSIZE:
            self.num_rounds = AES_256_ROUNDS

        if self.verbose:
            print("Key length: %d bits" % self.keylen)
        self._gen_roundkeys()


    def next(self, encdec, block):
#        self.S = [0][0 : 3] = block[0  :  3]
#        self.S = [1][0 : 3] = block[4  :  7]
#        self.S = [2][0 : 3] = block[8  : 11]
#        self.S = [3][0 : 3] = block[12 : 15]
        if self.verbose:
            print(self.S)
        return self.S


    #---------------------------------------------------------------
    #---------------------------------------------------------------
    def _initial_round(self):
        pass


    #---------------------------------------------------------------
    #---------------------------------------------------------------
    def _aes_round(self):
        pass


    #---------------------------------------------------------------
    #---------------------------------------------------------------
    def _final_round(self):
        pass


    #---------------------------------------------------------------
    #---------------------------------------------------------------
    def _gen_roundkeys(self):
        self.round_keys = [[0x00] * 16] * self.num_rounds
        self.rcon = 0x8d

        # Initial round key created by copying from the key.
        if self.keylen == 128:
            self.round_keys[0] = self.key[:]
        if self.keylen == 192:
            self.round_keys[0] = self.key[0 : 16]
            self.round_keys[1] = self.key[16 : 24] + [0] * 8

        if self.keylen == 256:
            self.round_keys[0] = self.key[0 : 16]
            self.round_keys[1] = self.key[16 : 32]

        if self.verbose:
            print("Round keys:")
            print(self.round_keys)

        #self.roundkeys = [0] * rounds[self.keylen]


    #---------------------------------------------------------------
    # _next_rcon()
    #
    # Update the internal rcon value used during key expansion.
    #---------------------------------------------------------------
    def _next_rcon(self):
        self.rcon = ((self.rcon << 1) ^ (0x11b & -(self.rcon >> 7))) & 0xff


    #---------------------------------------------------------------
    #---------------------------------------------------------------
    def _subbytes(self):
        pass
            

    #---------------------------------------------------------------
    #---------------------------------------------------------------
    def _mixcolumn(self, op0, op1, op2, op3):
        (self.S[0][0], self.S[1][0], self.S[2][0], self.S[3][0]) =\
        self._mixer(self.S[0][0], self.S[1][0], self.S[2][0], self.S[3][0])

        (self.S[0][1], self.S[1][1], self.S[2][1], self.S[3][1]) =\
        self._mixer(self.S[0][1], self.S[1][1], self.S[2][1], self.S[3][1])

        (self.S[0][2], self.S[1][2], self.S[2][2], self.S[3][2]) =\
        self._mixer(self.S[0][2], self.S[1][2], self.S[2][2], self.S[3][2])

        (self.S[0][3], self.S[1][3], self.S[2][3], self.S[3][3]) =\
        self._mixer(self.S[0][3], self.S[1][3], self.S[2][3], self.S[3][3])


    #---------------------------------------------------------------
    #---------------------------------------------------------------
    def _inverse_mixcolumn(self, op0, op1, op2, op3):
        (self.S[0][0], self.S[1][0], self.S[2][0], self.S[3][0]) =\
        self._inv_mixer(self.S[0][0], self.S[1][0], self.S[2][0], self.S[3][0])

        (self.S[0][1], self.S[1][1], self.S[2][1], self.S[3][1]) =\
        self._inv_mixer(self.S[0][1], self.S[1][1], self.S[2][1], self.S[3][1])

        (self.S[0][2], self.S[1][2], self.S[2][2], self.S[3][2]) =\
        self._inv_mixer(self.S[0][2], self.S[1][2], self.S[2][2], self.S[3][2])

        (self.S[0][3], self.S[1][3], self.S[2][3], self.S[3][3]) =\
        self._inv_mixer(self.S[0][3], self.S[1][3], self.S[2][3], self.S[3][3])


    #---------------------------------------------------------------
    #---------------------------------------------------------------
    def _mixer(self, op0, op1, op2, op3):
        new_op0 = self._gm2(op0) ^ self._gm3(op1) ^ op2            ^ op3;
        new_op1 = op0            ^ self._gm2(op1) ^ self._gm3(op2) ^ op3;
        new_op2 = op0            ^ op1            ^ self._gm2(op2) ^ self._gm3(op3);
        new_op3 = self._gm3(op0) ^ op1            ^ op2            ^ self._gm2(op3);
        return (new_op0, new_op1, new_op2, new_op3)


    #---------------------------------------------------------------
    #---------------------------------------------------------------
    def _inv_mixer(self, op0, op1, op2, op3):
        new_op0 = self._gm14(op0) ^ self._gm11(op1) ^ self._gm13(2) ^ self._gm09(3);
        new_op1 = self._gm09(op0) ^ self._gm14(op1) ^ self._gm11(2) ^ self._gm13(3);
        new_op2 = self._gm13(op0) ^ self._gm09(op1) ^ self._gm14(2) ^ self._gm11(3);
        new_op3 = self._gm11(op0) ^ self._gm13(op1) ^ self._gm09(2) ^ self._gm14(3);
        return (new_op0, new_op1, new_op2, new_op3)


    #---------------------------------------------------------------
    #---------------------------------------------------------------
    def _print_state(self, round):
        print("State at round 0x%02x:" % round)
        print("")


    #---------------------------------------------------------------
    #---------------------------------------------------------------
    def _gm2(self, op):
        tmp_op = (op << 1) & 0xff
        if (op & 0x80):
            return tmp_op ^ 0x1b
        else:
            return tmp_op


    #---------------------------------------------------------------
    #---------------------------------------------------------------
    def _gm3(self, op):
        return self._gm2(op) ^ op


    #---------------------------------------------------------------
    #---------------------------------------------------------------
    def _gm4(self, op):
        return self._gm2(self._gm2(op))

    
    #---------------------------------------------------------------
    #---------------------------------------------------------------
    def _gm8(self, op):
        return self._gm4(self._gm4(op))


    #---------------------------------------------------------------
    #---------------------------------------------------------------
    def _gm9(self, op):
        return self._gm8(op) ^ op


    #---------------------------------------------------------------
    #---------------------------------------------------------------
    def _gm11(self, op):
        return self._gm8(op) ^ self._gm2(op) ^ op


    #---------------------------------------------------------------
    #---------------------------------------------------------------
    def _gm13(self, op):
        return self._gm8(op) ^ self._gm4(op) ^ op


    #---------------------------------------------------------------
    #---------------------------------------------------------------
    def _gm14(self, op):
        return self._gm8(op) ^ self._gm4(op) ^ self._gm2(op)


#-------------------------------------------------------------------
# compare_blocks()
#
# Compare an AES block and print results.
#-------------------------------------------------------------------
def compare_blocks(block, expected):
    if (block != expected):
        print("Error:")
        print("Got:")
        print(block)
        print("Expected:")
        print(expected)
    else:
        print("Test case ok.")


#-------------------------------------------------------------------
# test_NIST_ecb_single_block()
#
# Perform single block ECB mode testing as specified by NIST:
# http://csrc.nist.gov/publications/nistpubs/800-38a/sp800-38a.pdf
#-------------------------------------------------------------------
def test_nist_ecb_single_block(tc, encdec, key, plaintext, expected):
    my_aes = AES()
    my_aes.init(key)
    my_aes.next(encdec, plaintext)


#-------------------------------------------------------------------
# test_rcon()
#
# Test the rcon logic used in key expansion.
#-------------------------------------------------------------------
def test_rcon():
    print("Testing rcon generation:")
    print("------------------------")

    my_aes = AES()
    my_aes.init([0x00] * 16)
    for i in range(256):
        print("rcon[%02x] = 0x%02x" % (i, my_aes.rcon))
        my_aes._next_rcon()
    print("")


#-------------------------------------------------------------------
# test_mixers()
#
# Test the mixcolumn and inverse mixcolumn functions.
#-------------------------------------------------------------------
def test_mixers():
    my_aes = AES()
    mixer_tests = [((0xdb, 0x13, 0x53, 0x45), (0x8e, 0x4d, 0xa1, 0xbc)),
                   ((0xf2, 0x0a, 0x22, 0x5c), (0x9f, 0xdc, 0x58, 0x9d)),
                   ((0x01, 0x01, 0x01, 0x01), (0x01, 0x01, 0x01, 0x01)),
                   ((0xc6, 0xc6, 0xc6, 0xc6), (0xc6, 0xc6, 0xc6, 0xc6)),
                   ((0xd4, 0xd4, 0xd4, 0xd5), (0xd5, 0xd5, 0xd7, 0xd6)),
                   ((0x2d, 0x26, 0x31, 0x4c), (0x4d, 0x7e, 0xbd, 0xf8))]

    print("Testing mixer function:")
    print("-----------------------")

    for (input, expected) in mixer_tests:
        (op0, op1, op2, op3) = input
        result = my_aes._mixer(op0, op1, op2, op3)
        print("Result: ", result)
        print("Expected: ", expected)
    print("")
        

#-------------------------------------------------------------------
# test_key_expansion()
#
# Perform testing of round key generation/key expansion for
# 128, 192 and 256 bit keys.
#-------------------------------------------------------------------
def test_key_expansion():
    key128_1 = (0x00000000, 0x00000000, 0x00000000, 0x00000000)
    exp128_1 = ((0x00000000, 0x00000000, 0x00000000, 0x00000000),
                (0x62636363, 0x62636363, 0x62636363, 0x62636363),
                (0x9b9898c9, 0xf9fbfbaa, 0x9b9898c9, 0xf9fbfbaa),
                (0x90973450, 0x696ccffa, 0xf2f45733, 0x0b0fac99),
                (0xee06da7b, 0x876a1581, 0x759e42b2, 0x7e91ee2b),
                (0x7f2e2b88, 0xf8443e09, 0x8dda7cbb, 0xf34b9290),
                (0xec614b85, 0x1425758c, 0x99ff0937, 0x6ab49ba7),
                (0x21751787, 0x3550620b, 0xacaf6b3c, 0xc61bf09b),
                (0x0ef90333, 0x3ba96138, 0x97060a04, 0x511dfa9f),
                (0xb1d4d8e2, 0x8a7db9da, 0x1d7bb3de, 0x4c664941),
                (0xb4ef5bcb, 0x3e92e211, 0x23e951cf, 0x6f8f188e))

    key128_2 = (0xffffffff, 0xffffffff, 0xffffffff, 0xffffffff)
    exp128_2 = ((0xffffffff, 0xffffffff, 0xffffffff, 0xffffffff),
                (0xe8e9e9e9, 0x17161616, 0xe8e9e9e9, 0x17161616),
                (0xadaeae19, 0xbab8b80f, 0x525151e6, 0x454747f0),
                (0x090e2277, 0xb3b69a78, 0xe1e7cb9e, 0xa4a08c6e),
                (0xe16abd3e, 0x52dc2746, 0xb33becd8, 0x179b60b6),
                (0xe5baf3ce, 0xb766d488, 0x045d3850, 0x13c658e6),
                (0x71d07db3, 0xc6b6a93b, 0xc2eb916b, 0xd12dc98d),
                (0xe90d208d, 0x2fbb89b6, 0xed5018dd, 0x3c7dd150),
                (0x96337366, 0xb988fad0, 0x54d8e20d, 0x68a5335d),
                (0x8bf03f23, 0x3278c5f3, 0x66a027fe, 0x0e0514a3),
                (0xd60a3588, 0xe472f07b, 0x82d2d785, 0x8cd7c326))

    key128_3 = (0x00010203, 0x04050607, 0x08090a0b, 0x0c0d0e0f)
    exp128_3 = ((0x00010203, 0x04050607, 0x08090a0b, 0x0c0d0e0f),
                (0xd6aa74fd, 0xd2af72fa, 0xdaa678f1, 0xd6ab76fe),
                (0xb692cf0b, 0x643dbdf1, 0xbe9bc500, 0x6830b3fe),
                (0xb6ff744e, 0xd2c2c9bf, 0x6c590cbf, 0x0469bf41),
                (0x47f7f7bc, 0x95353e03, 0xf96c32bc, 0xfd058dfd),
                (0x3caaa3e8, 0xa99f9deb, 0x50f3af57, 0xadf622aa),
                (0x5e390f7d, 0xf7a69296, 0xa7553dc1, 0x0aa31f6b),
                (0x14f9701a, 0xe35fe28c, 0x440adf4d, 0x4ea9c026),
                (0x47438735, 0xa41c65b9, 0xe016baf4, 0xaebf7ad2),
                (0x549932d1, 0xf0855768, 0x1093ed9c, 0xbe2c974e),
                (0x13111d7f, 0xe3944a17, 0xf307a78b, 0x4d2b30c5))

    key128_4 = (0x6920e299, 0xa5202a6d, 0x656e6368, 0x69746f2a)
    exp128_4 = ((0x6920e299, 0xa5202a6d, 0x656e6368, 0x69746f2a),
                (0xfa880760, 0x5fa82d0d, 0x3ac64e65, 0x53b2214f),
                (0xcf75838d, 0x90ddae80, 0xaa1be0e5, 0xf9a9c1aa),
                (0x180d2f14, 0x88d08194, 0x22cb6171, 0xdb62a0db),
                (0xbaed96ad, 0x323d1739, 0x10f67648, 0xcb94d693),
                (0x881b4ab2, 0xba265d8b, 0xaad02bc3, 0x6144fd50),
                (0xb34f195d, 0x096944d6, 0xa3b96f15, 0xc2fd9245),
                (0xa7007778, 0xae6933ae, 0x0dd05cbb, 0xcf2dcefe),
                (0xff8bccf2, 0x51e2ff5c, 0x5c32a3e7, 0x931f6d19),
                (0x24b7182e, 0x7555e772, 0x29674495, 0xba78298c),
                (0xae127cda, 0xdb479ba8, 0xf220df3d, 0x4858f6b1))

    key192_1 = (0x00000000, 0x00000000, 0x00000000,
                0x00000000, 0x00000000, 0x00000000)
    exp192_1 = ((0x00000000, 0x00000000, 0x00000000, 0x00000000),
                (0x00000000, 0x00000000, 0x62636363, 0x62636363),
                (0x62636363, 0x62636363, 0x62636363, 0x62636363),
                (0x9b9898c9, 0xf9fbfbaa, 0x9b9898c9, 0xf9fbfbaa),
                (0x9b9898c9, 0xf9fbfbaa, 0x90973450, 0x696ccffa),
                (0xf2f45733, 0x0b0fac99, 0x90973450, 0x696ccffa),
                (0xc81d19a9, 0xa171d653, 0x53858160, 0x588a2df9),
                (0xc81d19a9, 0xa171d653, 0x7bebf49b, 0xda9a22c8),
                (0x891fa3a8, 0xd1958e51, 0x198897f8, 0xb8f941ab),
                (0xc26896f7, 0x18f2b43f, 0x91ed1797, 0x407899c6),
                (0x59f00e3e, 0xe1094f95, 0x83ecbc0f, 0x9b1e0830),
                (0x0af31fa7, 0x4a8b8661, 0x137b885f, 0xf272c7ca),
                (0x432ac886, 0xd834c0b6, 0xd2c7df11, 0x984c5970))

    key192_2 = (0xffffffff, 0xffffffff, 0xffffffff,
                0xffffffff, 0xffffffff, 0xffffffff)
    exp192_2 = ((0xffffffff, 0xffffffff, 0xffffffff, 0xffffffff),
                (0xffffffff, 0xffffffff, 0xe8e9e9e9, 0x17161616),
                (0xe8e9e9e9, 0x17161616, 0xe8e9e9e9, 0x17161616),
                (0xadaeae19, 0xbab8b80f, 0x525151e6, 0x454747f0),
                (0xadaeae19, 0xbab8b80f, 0xc5c2d8ed, 0x7f7a60e2),
                (0x2d2b3104, 0x686c76f4, 0xc5c2d8ed, 0x7f7a60e2),
                (0x1712403f, 0x686820dd, 0x454311d9, 0x2d2f672d),
                (0xe8edbfc0, 0x9797df22, 0x8f8cd3b7, 0xe7e4f36a),
                (0xa2a7e2b3, 0x8f88859e, 0x67653a5e, 0xf0f2e57c),
                (0x2655c33b, 0xc1b13051, 0x6316d2e2, 0xec9e577c),
                (0x8bfb6d22, 0x7b09885e, 0x67919b1a, 0xa620ab4b),
                (0xc53679a9, 0x29a82ed5, 0xa25343f7, 0xd95acba9),
                (0x598e482f, 0xffaee364, 0x3a989acd, 0x1330b418))

    key192_3 = (0x00010203, 0x04050607, 0x08090a0b,
                0x0c0d0e0f, 0x10111213, 0x14151617)
    exp192_3 = ((0x00010203, 0x04050607, 0x08090a0b, 0x0c0d0e0f),
                (0x10111213, 0x14151617, 0x5846f2f9, 0x5c43f4fe),
                (0x544afef5, 0x5847f0fa, 0x4856e2e9, 0x5c43f4fe),
                (0x40f949b3, 0x1cbabd4d, 0x48f043b8, 0x10b7b342),
                (0x58e151ab, 0x04a2a555, 0x7effb541, 0x6245080c),
                (0x2ab54bb4, 0x3a02f8f6, 0x62e3a95d, 0x66410c08),
                (0xf5018572, 0x97448d7e, 0xbdf1c6ca, 0x87f33e3c),
                (0xe5109761, 0x83519b69, 0x34157c9e, 0xa351f1e0),
                (0x1ea0372a, 0x99530916, 0x7c439e77, 0xff12051e),
                (0xdd7e0e88, 0x7e2fff68, 0x608fc842, 0xf9dcc154),
                (0x859f5f23, 0x7a8d5a3d, 0xc0c02952, 0xbeefd63a),
                (0xde601e78, 0x27bcdf2c, 0xa223800f, 0xd8aeda32),
                (0xa4970a33, 0x1a78dc09, 0xc418c271, 0xe3a41d5d))


    key256_1 = (0x00000000, 0x00000000, 0x00000000, 0x00000000,
                0x00000000, 0x00000000, 0x00000000, 0x0000000)
    exp256_1 = ((0x00000000, 0x00000000, 0x00000000, 0x00000000),
                (0x00000000, 0x00000000, 0x00000000, 0x00000000),
                (0x62636363, 0x62636363, 0x62636363, 0x62636363),
                (0xaafbfbfb, 0xaafbfbfb, 0xaafbfbfb, 0xaafbfbfb),
                (0x6f6c6ccf, 0x0d0f0fac, 0x6f6c6ccf, 0x0d0f0fac),
                (0x7d8d8d6a, 0xd7767691, 0x7d8d8d6a, 0xd7767691),
                (0x5354edc1, 0x5e5be26d, 0x31378ea2, 0x3c38810e),
                (0x968a81c1, 0x41fcf750, 0x3c717a3a, 0xeb070cab),
                (0x9eaa8f28, 0xc0f16d45, 0xf1c6e3e7, 0xcdfe62e9),
                (0x2b312bdf, 0x6acddc8f, 0x56bca6b5, 0xbdbbaa1e),
                (0x6406fd52, 0xa4f79017, 0x553173f0, 0x98cf1119),
                (0x6dbba90b, 0x07767584, 0x51cad331, 0xec71792f),
                (0xe7b0e89c, 0x4347788b, 0x16760b7b, 0x8eb91a62),
                (0x74ed0ba1, 0x739b7e25, 0x2251ad14, 0xce20d43b),
                (0x10f80a17, 0x53bf729c, 0x45c979e7, 0xcb706385))

    key256_2 = (0xffffffff, 0xffffffff, 0xffffffff, 0xffffffff,
                0xffffffff, 0xffffffff, 0xffffffff, 0xffffffff)
    exp256_2 = ((0xffffffff, 0xffffffff, 0xffffffff, 0xffffffff),
                (0xffffffff, 0xffffffff, 0xffffffff, 0xffffffff),
                (0xe8e9e9e9, 0x17161616, 0xe8e9e9e9, 0x17161616),
                (0x0fb8b8b8, 0xf0474747, 0x0fb8b8b8, 0xf0474747),
                (0x4a494965, 0x5d5f5f73, 0xb5b6b69a, 0xa2a0a08c),
                (0x355858dc, 0xc51f1f9b, 0xcaa7a723, 0x3ae0e064),
                (0xafa80ae5, 0xf2f75596, 0x4741e30c, 0xe5e14380),
                (0xeca04211, 0x29bf5d8a, 0xe318faa9, 0xd9f81acd),
                (0xe60ab7d0, 0x14fde246, 0x53bc014a, 0xb65d42ca),
                (0xa2ec6e65, 0x8b5333ef, 0x684bc946, 0xb1b3d38b),
                (0x9b6c8a18, 0x8f91685e, 0xdc2d6914, 0x6a702bde),
                (0xa0bd9f78, 0x2beeac97, 0x43a565d1, 0xf216b65a),
                (0xfc223491, 0x73b35ccf, 0xaf9e35db, 0xc5ee1e05),
                (0x0695ed13, 0x2d7b4184, 0x6ede2455, 0x9cc8920f),
                (0x546d424f, 0x27de1e80, 0x88402b5b, 0x4dae355e))


    key256_3 = (0x00010203, 0x04050607, 0x08090a0b, 0x0c0d0e0f,
                0x10111213, 0x14151617, 0x18191a1b, 0x1c1d1e1f)
    exp256_3 = ((0x00010203, 0x04050607, 0x08090a0b, 0x0c0d0e0f),
                (0x10111213, 0x14151617, 0x18191a1b, 0x1c1d1e1f),
                (0xa573c29f, 0xa176c498, 0xa97fce93, 0xa572c09c),
                (0x1651a8cd, 0x0244beda, 0x1a5da4c1, 0x0640bade),
                (0xae87dff0, 0x0ff11b68, 0xa68ed5fb, 0x03fc1567),
                (0x6de1f148, 0x6fa54f92, 0x75f8eb53, 0x73b8518d),
                (0xc656827f, 0xc9a79917, 0x6f294cec, 0x6cd5598b),
                (0x3de23a75, 0x524775e7, 0x27bf9eb4, 0x5407cf39),
                (0x0bdc905f, 0xc27b0948, 0xad5245a4, 0xc1871c2f),
                (0x45f5a660, 0x17b2d387, 0x300d4d33, 0x640a820a),
                (0x7ccff71c, 0xbeb4fe54, 0x13e6bbf0, 0xd261a7df),
                (0xf01afafe, 0xe7a82979, 0xd7a5644a, 0xb3afe640),
                (0x2541fe71, 0x9bf50025, 0x8813bbd5, 0x5a721c0a),
                (0x4e5a6699, 0xa9f24fe0, 0x7e572baa, 0xcdf8cdea),
                (0x24fc79cc, 0xbf0979e9, 0x371ac23c, 0x6d68de36))

    key_expansion_testcases = [(key128_1, exp128_1),
                               (key128_2, exp128_2),
                               (key128_3, exp128_3),
                               (key128_4, exp128_4),
                               (key192_1, exp192_1),
                               (key192_2, exp192_2),
                               (key192_3, exp192_3),
                               (key256_1, exp256_1),
                               (key256_2, exp256_2),
                               (key256_3, exp256_3)]


    print("Key expansion test started.")
    print("---------------------------")

    my_aes = AES(verbose=True)

    for (key, expect) in key_expansion_testcases:
        if VERBOSE:
            print("Key:")
            print(key)
            print("Expected round keys:")
            print(expect)
            print("")

        my_aes.init(key)
#        if my_aes.round_keys == expect:
#            print("Correct round keys generated.")
#        else:
#            print("Error! Not correct round keys generated.")

    
#-------------------------------------------------------------------
# main()
#
# If executed tests the ChaCha class using known test vectors.
#-------------------------------------------------------------------
def main():
    print("Testing the AES Python model started")
    print("====================================")
    print

    # Test rcon generation.
    test_rcon()

    # Test the mixers.
    test_mixers()

    # Test the key expansion.
    test_key_expansion()

    # Test of AES. These keys are from:
    # http://www.inconteam.com/software-development/41-encryption/55-aes-test-vectors
    nist_aes128_key = (0x2b7e1516, 0x28aed2a6, 0xabf71588, 0x09cf4f3c)
    nist_aes192_key = (0x8e73b0f7, 0xda0e6452, 0xc810f32b,
                       0x809079e5, 0x62f8ead2, 0x522c6b7b)
    nist_aes256_key = (0x603deb10, 0x15ca71be, 0x2b73aef0, 0x857d7781,
                       0x1f352c07, 0x3b6108d7, 0x2d9810a3, 0x0914dff4)
    
    nist_plaintext0 = (0x6bc1bee2, 0x2e409f96, 0xe93d7e11, 0x7393172a)
    nist_plaintext1 = (0xae2d8a57, 0x1e03ac9c, 0x9eb76fac, 0x45af8e51)
    nist_plaintext2 = (0x30c81c46, 0xa35ce411, 0xe5fbc119, 0x1a0a52ef)
    nist_plaintext3 = (0xf69f2445, 0xdf4f9b17, 0xad2b417b, 0xe66c3710)

    nist_exp128_0 = (0x3ad77bb4, 0x0d7a3660, 0xa89ecaf3, 0x2466ef97)
    nist_exp128_1 = (0xf5d3d585, 0x03b9699d, 0xe785895a, 0x96fdbaaf)
    nist_exp128_2 = (0x43b1cd7f, 0x598ece23, 0x881b00e3, 0xed030688)
    nist_exp128_3 = (0x7b0c785e, 0x27e8ad3f, 0x82232071, 0x04725dd4)

    nist_exp192_0 = (0xbd334f1d, 0x6e45f25f, 0xf712a214, 0x571fa5cc)
    nist_exp192_1 = (0x97410484, 0x6d0ad3ad, 0x7734ecb3, 0xecee4eef)
    nist_exp192_2 = (0xef7afd22, 0x70e2e60a, 0xdce0ba2f, 0xace6444e)
    nist_exp192_3 = (0x9a4b41ba, 0x738d6c72, 0xfb166916, 0x03c18e0e)
    
    nist_exp256_0 = (0xf3eed1bd, 0xb5d2a03c, 0x064b5a7e, 0x3db181f8)
    nist_exp256_1 = (0x591ccb10, 0xd410ed26, 0xdc5ba74a, 0x31362870)
    nist_exp256_2 = (0xb6ed21b9, 0x9ca6f4f9, 0xf153e7b1, 0xbeafed1d)
    nist_exp256_3 = (0x23304b7a, 0x39f9f3ff, 0x067d8d8f, 0x9e24ecc7)

    print("ECB 128 bit key tests")
    print("---------------------")
    
    test_nist_ecb_single_block(1, AES_ENCIPHER, nist_aes128_key, 
                               nist_plaintext0, nist_ecb_128_enc_expected0)

    test_nist_ecb_single_block(2, AES_ENCIPHER, nist_aes128_key, 
                               nist_plaintext1, nist_ecb_128_enc_expected1)

    test_nist_ecb_single_block(3, AES_ENCIPHER, nist_aes128_key, 
                               nist_plaintext2, nist_ecb_128_enc_expected2)
    
    test_nist_ecb_single_block(3, AES_ENCIPHER, nist_aes128_key, 
                               nist_plaintext3, nist_ecb_128_enc_expected3)

    
    test_nist_ecb_single_block(5, AES_DECIPHER, nist_aes128_key, 
                               nist_ecb_128_enc_expected0, nist_plaintext0)
    
    test_nist_ecb_single_block(6, AES_DECIPHER, nist_aes128_key, 
                               nist_ecb_128_enc_expected1, nist_plaintext1)

    test_nist_ecb_single_block(7, AES_DECIPHER, nist_aes128_key, 
                               nist_ecb_128_enc_expected2, nist_plaintext2)

    test_nist_ecb_single_block(8, AES_DECIPHER, nist_aes128_key, 
                               nist_ecb_128_enc_expected3, nist_plaintext3)
    

    print("")
    print("ECB 192 bit key tests")
    print("---------------------")
    
    test_nist_ecb_single_block(9, AES_ENCIPHER, nist_aes192_key, 
                               nist_plaintext0, nist_ecb_192_enc_expected0)
    
    test_nist_ecb_single_block(10, AES_ENCIPHER, nist_aes192_key, 
                               nist_plaintext1, nist_ecb_192_enc_expected1)
    
    test_nist_ecb_single_block(11, AES_ENCIPHER, nist_aes192_key, 
                               nist_plaintext2, nist_ecb_192_enc_expected2)

    test_nist_ecb_single_block(12, AES_ENCIPHER, nist_aes192_key, 
                               nist_plaintext3, nist_ecb_192_enc_expected3)

      
    test_nist_ecb_single_block(13, AES_DECIPHER, nist_aes192_key, 
                               nist_ecb_192_enc_expected0, nist_plaintext0)

    test_nist_ecb_single_block(14, AES_DECIPHER, nist_aes192_key, 
                               nist_ecb_192_enc_expected1, nist_plaintext1)

    test_nist_ecb_single_block(15, AES_DECIPHER, nist_aes192_key, 
                               nist_ecb_192_enc_expected2, nist_plaintext2)

    test_nist_ecb_single_block(16, AES_DECIPHER, nist_aes192_key, 
                               nist_ecb_192_enc_expected3, nist_plaintext3)


      
    print("")
    print("ECB 256 bit key tests")
    print("---------------------")
    test_nist_ecb_single_block(17, AES_ENCIPHER, nist_aes256_key, 
                               nist_plaintext0, nist_ecb_256_enc_expected0)

    test_nist_ecb_single_block(18, AES_ENCIPHER, nist_aes256_key, 
                               nist_plaintext1, nist_ecb_256_enc_expected1)
      
    test_nist_ecb_single_block(19, AES_ENCIPHER, nist_aes256_key, 
                               nist_plaintext2, nist_ecb_256_enc_expected2)

    test_nist_ecb_single_block(20, AES_ENCIPHER, nist_aes256_key, 
                               nist_plaintext3, nist_ecb_256_enc_expected3)
      
      
    test_nist_ecb_single_block(21, AES_DECIPHER, nist_aes256_key, 
                               nist_ecb_256_enc_expected0, nist_plaintext0)

    test_nist_ecb_single_block(22, AES_DECIPHER, nist_aes256_key, 
                               nist_ecb_256_enc_expected1, nist_plaintext1)
      
    test_nist_ecb_single_block(23, AES_DECIPHER, nist_aes256_key, 
                               nist_ecb_256_enc_expected2, nist_plaintext2)

    test_nist_ecb_single_block(24, AES_DECIPHER, nist_aes256_key, 
                               nist_ecb_256_enc_expected3, nist_plaintext3)
    
    print("")
    print("Testing the AES Python model completed")
    print("======================================")


#-------------------------------------------------------------------
# __name__
# Python thingy which allows the file to be run standalone as
# well as parsed from within a Python interpreter.
#-------------------------------------------------------------------
if __name__=="__main__": 
    # Run the main function.
    sys.exit(main())

#=======================================================================
# EOF aes.py
#=======================================================================
