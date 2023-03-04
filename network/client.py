from direct.distributed.PyDatagram import PyDatagram
from . import NetCommon


class Client(NetCommon):
    def __init__(self, base, protocol):
        self.base = base
        NetCommon.__init__(self, protocol)

    def connect(self, host, port, timeout):
        self.connection = self.manager.openTCPClientConnection(host, port, timeout)
        if self.connection:
            self.reader.addConnection(self.connection)
            message = 'Client: Connected to server.'
            print(message)
            self.base.display_messages(message)

    def send(self, data):
        if self.connection:
            self.writer.send(data, self.connection)
