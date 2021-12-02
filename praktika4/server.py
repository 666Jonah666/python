import random
import socket
import threading

class DH_Endpoint(object):
    def __init__(self, public_key1, public_key2, private_key):
        self.public_key1 = public_key1
        self.public_key2 = public_key2
        self.private_key = private_key
        self.full_key = None
    def generate_partial_key(self):
        partial_key = self.public_key1**self.private_key
        partial_key = partial_key%self.public_key2
        return partial_key
    def generate_full_key(self, partial_key_r):
        full_key = partial_key_r**self.private_key
        full_key = full_key%self.public_key2
        self.full_key = full_key
        return full_key
    def encrypt_message(self, message):
        encrypted_message = ""
        key = self.full_key
        for c in message:
            encrypted_message += chr(ord(c)+key)
        return encrypted_message
    def decrypt_message(self, encrypted_message):
        decrypted_message = ""
        key = self.full_key
        for c in encrypted_message:
            decrypted_message += chr(ord(c)-key)
        return decrypted_message

def setup():
    with open('public_keys.txt', 'r') as f:
        pub = f.read().splitlines()
    with open('private_keys.txt', 'r') as f:
        priv = f.read().splitlines()
    with open('allowed_pub_keys.txt', 'r') as f:
        allowed = f.read().splitlines()
    #s_public=random.randrange(100, 200)
    #s_private=random.randrange(100, 200)
    s_public = int(pub[0])
    s_private = int(priv[0])
    s_port = 9000 + random.randrange(0, 100) ###################
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    sock.bind(('localhost', 9090)) #setup server

    data1 = sock.recvfrom(1024)
    m_public = int(data1[0].decode('utf-8')) #recieve client public key
    if str(m_public) not in allowed:
        print("This public key is not allowed")
        raise SystemExit
    Sadat = DH_Endpoint(s_public, m_public, s_private) #generate class instance
    sock.sendto(bytes(str(s_public), encoding='utf-8'), data1[1]) #send server public key
    s_partial=Sadat.generate_partial_key() #generate partial key
    data2 = sock.recvfrom(1024)
    m_partial=int(data2[0].decode('utf-8')) #recieve client partial key
    s_full=Sadat.generate_full_key(m_partial) #generate full key
    sock.sendto(bytes(str(s_partial), encoding='utf-8'), data2[1]) #send server partial key to client
    data3 = sock.recvfrom(1024)
    m_port = int(Sadat.decrypt_message(data3[0].decode('utf-8'))) #recieve port from client
    sock.sendto(bytes(Sadat.encrypt_message(str(s_port)), encoding='utf-8'), data3[1]) #send our port to client
    sock.close()
    return s_port if s_port < m_port else m_port, Sadat #if server port < client port then use server port else use client port

def sock_recv(Sadat, sock):
    while True:
        c_data = sock.recvfrom(1024)
        print("Client - ", Sadat[0].decrypt_message(c_data[0].decode('utf-8')))

def main():
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    data = setup()
    port = data[0]
    Sadat = data[1]
    sock.bind(('localhost', port))
    print('Waiting for the first message from client')
    c_data = sock.recvfrom(1024)
    port = c_data[1]
    print("Client - ", Sadat.decrypt_message(c_data[0].decode('utf-8')))
    threading.Thread(target=sock_recv, args=([Sadat], sock)).start()
    while True:
        you = input()
        print("You - ", you)
        sock.sendto(bytes(Sadat.encrypt_message(you), encoding='utf-8'), port)
    sock.close()

main()
