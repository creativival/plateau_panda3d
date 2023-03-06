from direct.distributed.PyDatagram import PyDatagram
from src import Player2D
from . import NetCommon, ClientProtocol


class Client(NetCommon):
    def __init__(self, base):
        NetCommon.__init__(self, base)

        self.server_player = None
        self.connection = None
        self.protocol = ClientProtocol(base)

        self.base.taskMgr.add(self.send_player_state, 'send_player_state')

    def connect(self, host, port, timeout):
        self.connection = self.manager.openTCPClientConnection(host, port, timeout)
        if self.connection:
            self.reader.addConnection(self.connection)
            message = 'Client: Connected to server.'
            # print(message)
            self.base.display_messages(message)

            self.base.server_player = Player2D(self.base, is_guest=True)

    def send(self, data):
        if self.connection:
            self.writer.send(data, self.connection)

    def send_player_state(self, task):
        sync = self.player_state(self.base.player.client_id)
        self.send(sync)
        return task.again
