#/usr/bin/env python

from Crypto.Random import random, atfork
from Crypto.Hash import SHA256

from database import get_permitted_users
from secrets import flag

import SocketServer,threading,os,time

msg = """Welcome to the 0kauth System!\n"""

N = 168875487862812718103814022843977235420637243601057780595044400667893046269140421123766817420546087076238158376401194506102667350322281734359552897112157094231977097740554793824701009850244904160300597684567190792283984299743604213533036681794114720417437224509607536413793425411636411563321303444740798477587L
g = 19595533242629369747791401605606558418088927130487463844933662202465281465266200982457647235235528838735010358900495684567911298014908298340170885513171109743249504533143507682501017145381579984990109696


permitted_users=get_permitted_users() # {username:(salt,secret)}

def H(P):
  h = SHA256.new()
  h.update(P)
  return h.hexdigest()

def tohex(A):
  return hex(A)[2:].strip('L')

class incoming(SocketServer.BaseRequestHandler):
  def handle(self):
    atfork()
    req = self.request
    req.sendall(msg)
    username = req.recv(512)[:-1]
    if username not in permitted_users:
      req.sendall('Sorry, not permitted.\n')
      req.close()
      return
    public_client = int(req.recv(512).strip('\n'), 16) % N
    c = (public_client * permitted_users[username][1]) % N
    if c in [N-g, N-1, 0, 1, g]:
      req.sendall('Sorry, not permitted.\n')
      req.close()
      return
    random_server = random.randint(2, N-3)
    public_server = pow(g, random_server, N)
    residue = (public_server + permitted_users[username][1]) % N
    req.sendall(tohex(permitted_users[username][0]) + '\n')
    req.sendall(tohex(residue) + '\n')

    session_secret = (public_client * permitted_users[username][1]) % N
    session_secret = pow(session_secret, random_server, N)
    session_key = H(tohex(session_secret))

    proof = req.recv(512).strip('\n')

    if (proof != H(tohex(residue) + session_key)):
      req.sendall('Sorry, not permitted.\n')
      req.close()
      return

    our_verifier = H(tohex(public_client) + session_key)
    req.sendall(our_verifier + '\n')

    req.sendall('Congratulations! The flag is ' + flag + '\n')
    req.close()

class ReusableTCPServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
  pass

SocketServer.TCPServer.allow_reuse_address = True
server = ReusableTCPServer(("0.0.0.0", 1337), incoming)
server.timeout = 60
server.serve_forever()
