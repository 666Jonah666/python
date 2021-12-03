'''
Перед запуском имеет смысл изменить self.path на свою директорию!
'''
import http.server
import socketserver
#my custom extended SimpleHTTPRequestHandler class with custom handler
class HTTP_Server(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/media/sf_shared_folder': #set server directory. This is my directory!!!!
            self.path = 'index.html' #set html file to display
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

http_server = socketserver.TCPServer(("", 80), HTTP_Server) #create tcp server
#start server
try:
    http_server.serve_forever()
except KeyboardInterrupt:
    print("\nserver close")
    http_server.server_close()
