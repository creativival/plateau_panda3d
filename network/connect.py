from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from network import Server, Client, ServerProtocol, ClientProtocol
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator


class Connect:
    def __init__(self, network_state):
        self.network_state = network_state

        if self.network_state == 'server':
            self.server = Server(self, ServerProtocol(self), 9999)
            self.client = None
        else:  # 'client'
            self.server = None
            self.client = Client(self, ClientProtocol(self))
            self.client.connect("localhost", 9999, 3000)