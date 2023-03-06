from direct.distributed.PyDatagram import PyDatagram
from panda3d.core import *
from . import NetCommon, ServerProtocol


class Server:
    def __init__(self, port):
        self.connection = None
        self.protocol = ServerProtocol(self)
        self.listener = QueuedConnectionListener(self.manager, 0)
        socket = self.manager.openTCPServerRendezvous(port, 100)
        self.listener.addConnection(socket)
        self.connections = []
        self.client_id = 1

        self.top_right_text.setText('server')

        self.taskMgr.add(self.update_listener, 'update_listener')

    def update_listener(self, task):
        if self.listener.newConnectionAvailable():
            connection = PointerToConnection()
            if self.listener.getNewConnection(connection):
                self.connection = connection.p()
                self.connections.append(self.connection)
                self.reader.addConnection(self.connection)
                message = 'Server: New connection established.'
                # print(message)
                self.display_messages(message)
                self.top_right_text.setText(
                    self.top_right_text.getText() + f'\nclient{self.client_id}'
                )

                sending_message = \
                    f'Server: Welcome, client{self.client_id}! Please send your first message.'
                data = PyDatagram()
                data.addUint8(100)
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
