from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from . import NetCommon


class Client(NetCommon):
    def __init__(self, protocol):
        NetCommon.__init__(self, protocol)

    def connect(self, host, port, timeout):
        self.connection = self.manager.openTCPClientConnection(host, port, timeout)
        if self.connection:
            self.reader.addConnection(self.connection)
            print("Client: Connected to server.")

    def send(self, datagram):
        if self.connection:
            self.writer.send(datagram, self.connection)
