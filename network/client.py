from direct.distributed.PyDatagram import PyDatagram
from . import NetCommon, ClientProtocol


class Client:
    def __init__(self):
        self.protocol = ClientProtocol(self)

    def connect(self, host, port, timeout):
        self.connection = self.manager.openTCPClientConnection(host, port, timeout)
        if self.connection:
            self.reader.addConnection(self.connection)
            message = 'Client: Connected to server.'
            print(message)
            self.display_messages(message)

    def send(self, data):
        if self.connection:
            self.writer.send(data, self.connection)
