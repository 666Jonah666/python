import socket

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)
conn, addr = sock.accept()
while True:
     data = conn.recv(1024)
     if data == b'exit':
         conn.send(b"shutting down ...")
         print("shutting down by client")
         break
     else:
         print("data recieved. Message is - ", data.decode('utf-8'))
         conn.send(b"data recieved")
conn.close()
