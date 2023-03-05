from network import Server, Client, ServerProtocol, ClientProtocol
from constants import *


class Connect:
    def __init__(self, network_state):
        self.network_state = network_state

        if self.network_state == 'server':
            # self.server = Server(self, 9999)
            # self.client = None
            Server.__init__(self, PORT_ADDRESS)
        else:  # 'client'
            # self.server = None
            # self.client = Client(self)
            # self.client.connect('localhost', 9999, 3000)
            Client.__init__(self)
            self.connect(IP_ADDRESS, PORT_ADDRESS, TIMEOUT)
