
from ctypes import  *

def byte_to_short(bytes):
    dbsize = int(len(bytes) / 2)
    arrsh = (c_ushort * dbsize)()
    
    for i in range(dbsize):
        arrsh[i] = (bytes[i] << 8) | (bytes[i+1])


b = 0b01
f = 0b010
print(b | f)
sstr = 'spam'
sb = sstr.encode()
lbs = list(sb)
sh = c_char * 10

print(byte_to_short(sb))

print(sh)