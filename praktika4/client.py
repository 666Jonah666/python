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
    #m_public=random.randrange(100, 200)
    #m_private=random.randrange(100, 200)
    #m_public=132 #if you want to check what happens if public key not allowed uncomment this and comment next line
    m_public=int(pub[1])
    m_private=int(priv[1])
    m_port = 9000 + random.randrange(0, 100)
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    sock.connect(('localhost', 9090)) #setup connection

    sock.sendto(bytes(str(m_public), encoding='utf-8'), ('localhost', 9090)) #send client public key
    data1 = sock.recvfrom(1024)
    s_public = int(data1[0].decode('utf-8')) #recieve server public key
    Michael = DH_Endpoint(s_public, m_public, m_private) #generate class instance
    m_partial=Michael.generate_partial_key() #generate client partial key
    sock.sendto(bytes(str(m_partial), encoding='utf-8'), ('localhost', 9090)) #send client partial key
    data2 = sock.recvfrom(1024)
    s_partial = int(data2[0].decode('utf-8')) #recieve server partial key
    m_full=Michael.generate_full_key(s_partial) #generate full key
    sock.sendto(bytes(Michael.encrypt_message(str(m_port)), encoding='utf-8'), ('localhost', 9090)) #send encrypted port to server
    data3 = sock.recvfrom(1024)
    s_port = int(Michael.decrypt_message(data3[0].decode('utf-8'))) #recieve server encrypted port
    sock.close()
    return s_port if s_port < m_port else m_port, Michael #if server port < client port then use server port else use client port

def sock_recv(Michael, sock):
    while True:
        c_data = sock.recvfrom(1024)
        print('Server - ', Michael[0].decrypt_message(c_data[0].decode('utf-8')))

def main():
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    data = setup()
    port = data[0]
    Michael = data[1]
    sock.connect(('localhost', port))
    sock.sendto(bytes(Michael.encrypt_message(input('Type the first message - ')), encoding='utf-8'), ('localhost', port))
    threading.Thread(target=sock_recv, args=([Michael], sock)).start()
    while True:
        you = input()
        print("You - ", you)
        sock.sendto(bytes(Michael.encrypt_message(you), encoding='utf-8'), ('localhost', port))
    sock.close()

main()
