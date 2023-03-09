from network import Server, Client
from constants import *


class Connect:
    def __init__(self):
        self.server = None
        self.client = None
        self.network_state = ''

        self.acceptOnce('f10', self.open_server)
        self.acceptOnce('f11', self.connect_as_client)

    def open_server(self):
        if not self.network_state:
            self.network_state = 'server'
            self.server = Server(self, PORT_ADDRESS)

    def connect_as_client(self):
        if not self.network_state:
            self.network_state = 'client'
            self.client = Client(self)
            self.client.connect(IP_ADDRESS, PORT_ADDRESS, TIMEOUT)

        # if self.network_state == 'server':
        #     # self.server = Server(self, 9999)
        #     # self.client = None
        #     self.server = Server(self, PORT_ADDRESS)
        # else:  # 'client'
        #     # self.server = None
        #     # self.client = Client(self)
        #     # self.client.connect('localhost', 9999, 3000)
        #     self.client = Client(self)
        #     self.client.connect(IP_ADDRESS, PORT_ADDRESS, TIMEOUT)
