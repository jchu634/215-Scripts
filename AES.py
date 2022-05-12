from os import path
from Utilities import drawLine
from AESInput.sBox import sBox
from copy import copy
# import numpy as np

def getHex(inputList:list):
    return [hex(a)[2:].upper() for a in inputList]

def splitRows(inputList:list):
    rows = [[],[],[],[]]
    for i in range(0,16,4):
        rows[0].append(inputList[i])
        rows[1].append(inputList[i+1])
        rows[2].append(inputList[i+2])
        rows[3].append(inputList[i+3])
    return rows

def joinRows(inputList:list):
    row = []
    for i in range(0,4):
        row.append(inputList[0][i])
        row.append(inputList[1][i])
        row.append(inputList[2][i])
        row.append(inputList[3][i])
    return row

def splitRows(inputList:list):
    rows = [[],[],[],[]]
    for i in range(0,16,4):
        rows[0].append(inputList[i])
        rows[1].append(inputList[i+1])
        rows[2].append(inputList[i+2])
        rows[3].append(inputList[i+3])
    return rows

def splitColumns(inputList:list):
    columns = [[],[],[],[]]
    for i in range(0,16,4):
        index = int(i/4)
        columns[index].append(inputList[i])
        columns[index].append(inputList[i+1])
        columns[index].append(inputList[i+2])
        columns[index].append(inputList[i+3])
    # print('Columns')
    # for column in columns:
    #     print([hex(a)[2:]for a in column])
    return columns

def joinColumns(inputList:list):
    row = []
    for i in range(0,4):
        row.append(inputList[i][0])
        row.append(inputList[i][1])
        row.append(inputList[i][2])
        row.append(inputList[i][3])
    return row

def printState(inputList:list):
    columns = splitColumns(inputList)
    textOutput = ",".join(getHex(columns[0]))+","+",".join(getHex(columns[1]))+","+",".join(getHex(columns[2]))+","+",".join(getHex(columns[3]))

    rows = splitRows(inputList)
    print(getHex(rows[0]))
    print(getHex(rows[1]))
    print(getHex(rows[2]))
    print(getHex(rows[3]))
    print()
    print(textOutput)


def addRoundKey(plainText:list,roundKey:list):
    # print(plainText)
    # print(roundKey)
    # printState(roundKey)    
    return [b^roundKey[a]for a,b in enumerate(plainText)]

def subBytes(inputList:list):
    return [sBox(a) for a in inputList]

def shiftLeft(inputList:list,noOfShift:int):
    for i in range(noOfShift):
        inputList = inputList[1:] + inputList[:1]  
    return inputList  

def shiftRows(inputList:list):
    rows = splitRows(inputList)
    rows[1] = shiftLeft(rows[1],1)
    rows[2] = shiftLeft(rows[2],2)
    rows[3] = shiftLeft(rows[3],3)
    
    # rows[1] = rows[1][1:] + rows[1][:1]
    return joinRows(rows)

def galois_mult(a, b):
    """
    Multiplication in the Galois field GF(2^8).
    """
    p = 0
    hi_bit_set = 0
    for i in range(8):
        if b & 1 == 1: p ^= a
        hi_bit_set = a & 0x80
        a <<= 1
        if hi_bit_set == 0x80: a ^= 0x1b
        b >>= 1
    return p % 256

def mix_column(column):
    """
    Mix one column by by considering it as a polynomial and performing
    operations in the Galois field (2^8).
    """
    # XOR is addition in this field
    temp = copy(column) # Store temporary column for operations
    column[0] = galois_mult(temp[0], 2) ^ galois_mult(temp[1], 3) ^ \
                galois_mult(temp[2], 1) ^ galois_mult(temp[3], 1)
    column[1] = galois_mult(temp[0], 1) ^ galois_mult(temp[1], 2) ^ \
                galois_mult(temp[2], 3) ^ galois_mult(temp[3], 1)
    column[2] = galois_mult(temp[0], 1) ^ galois_mult(temp[1], 1) ^ \
                galois_mult(temp[2], 2) ^ galois_mult(temp[3], 3)
    column[3] = galois_mult(temp[0], 3) ^ galois_mult(temp[1], 1) ^ \
                galois_mult(temp[2], 1) ^ galois_mult(temp[3], 2)

def mixColumns(inputList:list):
    columns = splitColumns(inputList)
    # a = np.array(columns[0])
    for i in range(4):
        mix_column(columns[i])    
    # print("MixColumns")
    # print(columns[0])
    mix_column(columns[0])
    # print(columns[0])
    # print()
    
    return joinColumns(columns)



def main():
    
    
    if path.exists("AESInput/values.txt"):
        input_file = open("AESInput/values.txt","r")
        lines = input_file.read().splitlines()
        input_file.close()

        plainText = [ord(a) for a in lines[0]]
        rounds = int(lines[1])
        roundKeys = []
        for i in range(rounds):
            roundKeys.append([int(a,16) for a in lines[2+i].split(',')])

    else:
        plainText = input('Plaintext: ')
        plainText = [ord(a) for a in plainText]

        rounds = int(input('Rounds: '))
        roundKeys = []
        for i in range(rounds):
            userInput = input("Round {}'s Key: ".format(i)).split(',')
            roundKeys.append([int(a,16) for a in userInput])

    print('Initial State:')
    state1 = plainText[0:16]
    printState(state1)
    
    #Round 0
    drawLine()
    state1 = addRoundKey(state1,roundKeys[0])
    print('State after Round 0:')
    printState(state1)

    for i in range(10):
        drawLine()
        #SubBytes
        state1 = subBytes(state1)
        print('State after Round {} SubBytes:'.format(i+1))
        printState(state1)

        print()

        #ShiftRows
        state1 = shiftRows(state1)
        print('State after Round {} ShiftRows:'.format(i+1))
        printState(state1)

        print()

        #MixColumns NOTE Only works in theory-Untested
        print('State after Round {} MixColumns:'.format(i+1))
        state1 = mixColumns(state1)
        printState(state1)

        state1 = addRoundKey(state1,roundKeys[i+1])
        if input("Next Round? ([n] to stop, [Any other key] to continue): ").lower() == "n":
            break
    
if __name__ == '__main__':
    main()


