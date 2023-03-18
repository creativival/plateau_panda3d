from panda3d.core import *
from direct.gui.DirectGui import *
from network import Server, Client
from constants import *


class Connect:
    def __init__(self):
        self.server = None
        self.client = None
        self.network_state = ''

        # self.acceptOnce('f10', self.open_server)
        # self.acceptOnce('f11', self.connect_as_client)

    def open_server(self):
        if not self.network_state:
            try:
                self.server = Server(self, PORT_ADDRESS)
                self.network_state = 'server'
                self.toggle_menu()
                self.server_button['state'] = DGG.DISABLED
                self.toggle_join_button['state'] = DGG.DISABLED
            except TypeError:
                # 同じパソコンで複数のサーバーを開こうとしたとき、クライエントとして接続
                print('Found server and connect you as client')
                self.toggle_join()
                # self.client = Client(self)
                # self.client.connect(IP_ADDRESS, PORT_ADDRESS, TIMEOUT)
                # self.network_state = 'client'

    def connect_as_client(self):
        if not self.network_state:
            try:
                ip_address = self.join_input_field.get(True)
                self.client = Client(self)
                self.client.connect(ip_address, PORT_ADDRESS, TIMEOUT)
                self.network_state = 'client'
                self.toggle_join()
                self.toggle_menu()
                self.server_button['state'] = DGG.DISABLED
                self.toggle_join_button['state'] = DGG.DISABLED
            except TypeError:
                print('Not found server')

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
