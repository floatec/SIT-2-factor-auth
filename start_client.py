__author__ = 'Tieni'

from client import Client
from client_ui import ClientUI

client = Client()
client.open_socket()
clientUI = ClientUI(client)
#client.login('test', '1234')