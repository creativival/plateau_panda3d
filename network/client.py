from . import NetCommon


class Client(NetCommon):
    def __init__(self, base, protocol):
        self.base = base
        NetCommon.__init__(self, protocol)

    def connect(self, host, port, timeout):
        self.connection = self.manager.openTCPClientConnection(host, port, timeout)
        if self.connection:
            self.reader.addConnection(self.connection)
            print("Client: Connected to server.")

    def send(self, datagram):
        if self.connection:
            self.writer.send(datagram, self.connection)
