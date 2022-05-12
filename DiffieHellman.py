from tqdm import tqdm

g = int(input('g: '))
p = int(input('p: '))
cipherText = input('cipherText: ')
validNums = []
validKeys = set()
for a in tqdm(range(1000),ascii=True):
    for b in range(1000):
        alicePublic = (g**a)%p
        if alicePublic != 6:
            continue
        bobPublic = (g**b)%p
        if bobPublic != 9:
            continue

        aliceS = (bobPublic**a)% p
        bobS = (alicePublic**b)% p
        print("" + str(aliceS)+""+str(bobPublic))

        if aliceS == bobS:
            validKeys.add(aliceS)
            validNums.append([a,b])
            # validKeys.append(aliceS)

f = open('DiffieHellmanOutput/keys.txt','w')
for key in validKeys:
    f.write(str(key)+"\n")
f.close()
f = open('DiffieHellmanOutput/privateKeys.txt','w')
for key in validNums:
    f.write(str(key)+"\n")
f.close()

f = open('DiffieHellmanOutput/output.txt','w')
for key in validKeys:
    f.write("".join([hex(int(a,16)^key)[2:] for a in cipherText]).upper()+"\n")
f.close()