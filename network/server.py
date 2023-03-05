from direct.distributed.PyDatagram import PyDatagram
from panda3d.core import *
from . import NetCommon, ServerProtocol


class Server:
    def __init__(self, port):
        self.protocol = ServerProtocol(self)
        self.listener = QueuedConnectionListener(self.manager, 0)
        socket = self.manager.openTCPServerRendezvous(port, 100)
        self.listener.addConnection(socket)
        self.connections = []

        self.taskMgr.add(self.update_listener, 'update_listener')

    def update_listener(self, task):
        if self.listener.newConnectionAvailable():
            connection = PointerToConnection()
            if self.listener.getNewConnection(connection):
                connection = connection.p()
                self.connections.append(connection)
                self.reader.addConnection(connection)
                message = 'Server: New connection established.'
                print(message)
                self.display_messages(message)

        return task.cont

    def broadcast(self, data):
        for connection in self.connections:
            if connection:
                self.writer.send(data, connection)
