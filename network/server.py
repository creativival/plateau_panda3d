from direct.distributed.PyDatagram import PyDatagram
from panda3d.core import *
from src import Player2D, Players
from . import NetCommon, ServerProtocol


class Server(NetCommon):
    def __init__(self, base, port):
        NetCommon.__init__(self, base)

        self.guest_player = None
        self.connection = None
        self.protocol = ServerProtocol(base)
        self.listener = QueuedConnectionListener(self.manager, 0)
        socket = self.manager.openTCPServerRendezvous(port, 100)
        self.listener.addConnection(socket)
        self.connections = []
        self.client_id = 1

        self.base.top_right_text.setText('server')

        self.base.taskMgr.add(self.update_listener, 'update_listener')
        self.base.taskMgr.doMethodLater(0.1, self.send_player_state, 'send_player_state')

    def update_listener(self, task):
        if self.listener.newConnectionAvailable():
            connection = PointerToConnection()
            if self.listener.getNewConnection(connection):
                self.connection = connection.p()
                self.connections.append(self.connection)
                self.reader.addConnection(self.connection)
                message = 'Server: New connection established.'
                # print(message)
                self.base.display_messages(message)
                self.base.top_right_text.setText(
                    self.base.top_right_text.getText() + f'\nclient{self.client_id}'
                )

                self.base.add_player(self.client_id, is_guest=True)

                sending_message = \
                    f'Server: Welcome, client{self.client_id}! Please send your first message.'
                data = PyDatagram()
                data.addUint8(0)   # クライエント番号を伝達
                data.addUint8(self.client_id)
                data.addString(sending_message)
                self.send(data)

                self.client_id += 1

        return task.cont

    def send(self, data):
        if self.connection:
            self.writer.send(data, self.connection)

    def broadcast(self, data):
        for connection in self.connections:
            if connection:
                self.writer.send(data, connection)

    def send_player_state(self, task):
        if len(self.connections):
            sync = self.player_state()
            self.broadcast(sync)
        return task.again
