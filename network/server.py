from direct.distributed.PyDatagram import PyDatagram
from panda3d.core import *
from . import NetCommon


class Server(NetCommon):
    def __init__(self, base, protocol, port):
        self.base = base
        NetCommon.__init__(self, protocol)
        self.listener = QueuedConnectionListener(self.manager, 0)
        socket = self.manager.openTCPServerRendezvous(port, 100)
        self.listener.addConnection(socket)
        self.connections = []

        self.base.taskMgr.add(self.updateListener, 'updateListener')

    def updateListener(self, task):
        if self.listener.newConnectionAvailable():
            connection = PointerToConnection()
            if self.listener.getNewConnection(connection):
                connection = connection.p()
                self.connections.append(connection)
                self.reader.addConnection(connection)
                message = 'Server: New connection established.'
                print(message)
                self.base.display_messages(message)

        return task.cont

    def broadcast(self, data):
        for connection in self.connections:
            if connection:
                self.writer.send(data, connection)
