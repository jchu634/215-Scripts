from os import path
from shutil import get_terminal_size
from platform import python_implementation

def output(cipherText):
    print(hex(cipherText)[2:].upper(),end=" ")

def encrypt(plaintext,key):
    #Change this function to your custom function
    return plaintext^key

def ECB(plainText,key):
    print("ECB = ",end="")
    for text in plainText:
        output(encrypt(text,key))
    print()

def CBC(plainText,key,iv):
    print("CBC = ",end="")
    for text in plainText:
        cipherText = encrypt(encrypt(text,iv),key)
        
        output(cipherText)
        iv = cipherText
    print()

def PCBC(plainText,key,iv):
    print("PCBC = ",end="")
    for text in plainText:
        midText = encrypt(text,iv)
        cipherText = encrypt(midText,key)
        output(cipherText)
        iv = encrypt(cipherText,text)
    print()

def CFB(plainText,key,iv):
    print("CFB = ",end="")
    for text in plainText:
        # print()
        # output(encrypt(key,iv))
        cipherText = encrypt(encrypt(key,iv),text)
        output(cipherText)
        iv = cipherText
    print()

def OFB(plainText,key,iv):
    print("OFB = ",end="")
    for text in plainText:
        midText = encrypt(iv,key)
        cipherText = encrypt(midText,text)
        output(cipherText)
        iv = midText
    print()

def drawLine():
    if python_implementation() == 'PyPy':
        print('-' * get_terminal_size().columns)
    else:
        print(u'\u2500' * get_terminal_size().columns)

def main():
    if path.exists("BlockCipherInput/input.txt"):
        with open("BlockCipherInput/input.txt") as f:
            plainText = [int(a,16) for a in f.read().splitlines()]
    else:
        plainText = []
        print("Input Lines, Stop by inputing 'STOP'")
        while (True):
            temp = input("Input Line: ")
            if temp.lower() == "stop":
                break
            else:
                plainText.append(int(temp,16))
    drawLine()

    if path.exists("BlockCipherInput/keys.txt"):
        keys = open("BlockCipherInput/Keys.txt")
        key = int(keys.readline(),16)
        initialisationVector = int(keys.readline(),16)
        keys.close()
    else:
        key = int(input('Key: '),16)
        initialisationVector = int(input('I.V.: '),16)
    
    if path.exists("BlockCipherInput/keys.txt"):
        print("Key: " + hex(key)[2:].upper())
        print("I.V.: " + hex(initialisationVector)[2:].upper())
    drawLine()
    ECB(plainText,key)
    CBC(plainText,key,initialisationVector)
    PCBC(plainText,key,initialisationVector)
    CFB(plainText,key,initialisationVector)
    OFB(plainText,key,initialisationVector)

if __name__ == '__main__':
    main()


    

# print(plainText)