__author__ = 'Tieni'

from server import Server

server = Server()
server.open_socket()
server.handle_clients()