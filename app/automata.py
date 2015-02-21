import hashlib
m = hashlib.md5()
m.update("ObMaX")
hexValue = m.hexdigest()
seqChar = ""
for i in range (0,4):
  a = int(hexValue[i],16) %4 
  seqChar = seqChar + str(a)
#This will produce the knock sequence for the given usernam
seqInt = int(seq)


