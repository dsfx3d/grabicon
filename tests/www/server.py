import threading
import os
import io
from http.server import HTTPServer, CGIHTTPRequestHandler



class ServerRunner(threading.Thread):

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        server_address = ('127.0.0.1', 80)  
        self.httpd = HTTPServer(server_address, CGIHTTPRequestHandler)

    def run(self):
        try:
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            self.httpd.serve_forever()
        except OSError:
            print('server stopped')

    def close(self):
        self.httpd.socket.close()