from Crypto.Random import random
from Crypto.Hash import SHA256
from pwn import *

N = 168875487862812718103814022843977235420637243601057780595044400667893046269140421123766817420546087076238158376401194506102667350322281734359552897112157094231977097740554793824701009850244904160300597684567190792283984299743604213533036681794114720417437224509607536413793425411636411563321303444740798477587L
g = 19595533242629369747791401605606558418088927130487463844933662202465281465266200982457647235235528838735010358900495684567911298014908298340170885513171109743249504533143507682501017145381579984990109696
v=0x14122eb4a4082a02771144fa850bc7fc490771bd0831d5bbba024419656528185894820b5b18631029e15f3b0bd93fd9e530a4134a0863206e9297b998494f6bf4b53d077aa6f9b7040d2ef88f8534c7c7d56a4156576046bc5a3e109192f9bf7b07dda14cdc09971d3ce8b5484e240317ceaf84cc1bec4a95bead74e37af1a6

def H(P):
  h = SHA256.new()
  h.update(P)
  return h.hexdigest()

def tostr(A):
  return hex(A)[2:].strip('L')

def extended_gcd(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError
    return x % m
def tostr(A):
    return hex(A)[2:].strip('L')


pC=(g**2 * modinv(v,N))%N

# context.log_level="DEBUG"

r=remote("46.101.24.55", 1337)
r.recvline() # Welcome.
r.sendline("get_flag") # Username known from SQLi
r.sendline(tostr(pC))

r.recvline() # Salt.
res=int(r.recvline(),16) # Residue=(pS+v)%N
pS=(res-v+N)%N

key=H(tostr(pow(pS, 2, N)))
r.sendline(H(tostr(res)+key))

print r.recvall()
