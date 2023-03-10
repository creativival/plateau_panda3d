from . import NetCommon, ClientProtocol


class Client(NetCommon):
    def __init__(self, base):
        NetCommon.__init__(self, base)

        self.server_player = None
        self.connection = None
        self.protocol = ClientProtocol(base)

        self.base.taskMgr.doMethodLater(0.1, self.send_player_state, 'send_player_state')

    def connect(self, host, port, timeout):
        self.connection = self.manager.openTCPClientConnection(host, port, timeout)
        if self.connection:
            self.reader.addConnection(self.connection)
            message = 'Client: Connected to server.'
            # print(message)
            self.base.display_messages(message)

            self.base.add_player(0, is_guest=True)
        else:
            raise TypeError

    def send(self, data):
        if self.connection:
            self.writer.send(data, self.connection)

    def send_player_state(self, task):
        # クライエントがいるとき
        if self.base.players['myself'].client_id > 0:
            # print('client_id:', self.base.players['myself'].client_id)
            sync = self.player_state(self.base.players['myself'].client_id)
            self.send(sync)
        return task.again
