
import socket

sock = socket.socket()
sock.connect(('localhost', 9090))
while True:
    b = bytes(input(), encoding='utf-8')
    sock.send(b)
    data = sock.recv(1024)
    print(data.decode('utf-8'))
    if b == b"exit":
        sock.close()
        break
    else:
        continue
