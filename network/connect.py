from network import Server, Client, ServerProtocol, ClientProtocol
from constants import *


class Connect:
    def __init__(self, network_state):
        print(network_state)
        self.network_state = network_state

        if self.network_state == 'server':
            # self.server = Server(self, 9999)
            # self.client = None
            self.server = Server(self, PORT_ADDRESS)
        else:  # 'client'
            # self.server = None
            # self.client = Client(self)
            # self.client.connect('localhost', 9999, 3000)
            self.client = Client(self)
            self.client.connect(IP_ADDRESS, PORT_ADDRESS, TIMEOUT)
