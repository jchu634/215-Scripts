ip = input ("IP: ")
ipl = ip.split(".")
sumIP =""
for item in ipl:
    sumIP += bin (int (item)) [2:].zfill(8)+" "
print (sumIP)
