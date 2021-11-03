import socket
from threading import Thread
import logging

logging.basicConfig(level=logging.DEBUG, filename="log.log", filemode="w")
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("", 9090))

users_in_file = []
auth = {}

commands = ['Показ логов', 'Очистка логов', 'Очистка файла идентификации', 'Остановка сервера']
commands_short = ['showlogs','clrlogs','clrID','stop']

def serv_work(sock):
    print('Сервер работает.')
    print('Список доступных комманд:')
    for i in range(len(commands)):
        print(f"{i+1}. {commands[i]}: \"{commands_short[i]}\"")

    while True:
        command = input()
        if command not in commands_short:
            print('Нет такой команды.')
        elif 'showlogs' == command:
            with open('log.log', 'r') as file:
                for raw in file:
                    print(raw)
        elif 'clrlogs' == command:
            with open('log.log', 'w') as file:
                pass
            print("Выполнено")
        elif 'clrID' == command:
            with open('users.txt', 'w') as file:
                file.writelines("")
            print("Выполнено")
        elif 'stop' == command:
            sock.close()
            break

def read_file():
	global users_in_file
	with open("users.txt", mode="r", encoding="UTF-8") as u:
		file = u.readlines()
		for i in range(len(file)):
			file[i] = file[i].strip("\n")
			file[i] = file[i].split(";")
	users_in_file = file

def write_in_file():
	with open("users.txt", mode="w", encoding="UTF-8") as u:
		for i in range(len(users_in_file)):
			data = users_in_file[i][0] + ";" + users_in_file[i][1] + ";" + users_in_file[i][2] + "\n"
			u.writelines(data)

class multiServer(Thread):
	users = []
	def __init__(self, sock, address):
		Thread.__init__(self)
		self.__sock = sock
		self.__address = address
		logging.info(f"Add new user: {address}")
		self.msg_name = self.func(self.__sock)

	def add_new_user(self, conn):
		conn.send(str.encode("1"))
		name = conn.recv(1024).decode("UTF-8")
		password = conn.recv(1024).decode("UTF-8")
		users_in_file.append([name, password, self.__address[0]])
		return (name)

	def func(self, conn):
		for i in range(len(users_in_file)):
			if(self.__address[0] == users_in_file[i][2]):
				msg_name = users_in_file[i][0]
				if(msg_name not in auth.keys()):
					while (True):
						conn.send(str.encode("2"))
						password = conn.recv(1024).decode("UTF-8")
						if(password == users_in_file[i][1]):
							auth[msg_name] = 1
							conn.send(str.encode("4"))
							break
				break
		else:
			msg_name = self.add_new_user(conn)
			auth[msg_name] = 1
		return (msg_name)

	def run(self):
		read_file()
		self.users.append(self)
		while (True):
			data = self.__sock.recv(1024).decode("UTF-8")
			if (data == "exit"):
				break
			logging.info(f"Message from {self.msg_name}: {data}")
			print(f"Message from {self.msg_name}: {data}")
			for con in self.users:
				con.__sock.send(self.msg_name.encode())
				con.__sock.send(data.encode())
		write_in_file()

def main():
    work = Thread(target=serv_work, args=[server])
    work.start()
    while (True):
        try:
            server.listen(1)
            sock, address = server.accept()
            newUser = multiServer(sock, address)
            newUser.start()
        except OSError:
            print("Сервер закрыт!")
            break

if __name__ == "__main__":
    main()
