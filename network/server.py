from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from . import NetCommon


class Server(NetCommon):
    def __init__(self, protocol, port):
        NetCommon.__init__(self, protocol)
        self.listener = QueuedConnectionListener(self.manager, 0)
        socket = self.manager.openTCPServerRendezvous(port, 100)
        self.listener.addConnection(socket)
        self.connections = []

        taskMgr.add(self.updateListener, "updateListener")

    def updateListener(self, task):
        if self.listener.newConnectionAvailable():
            connection = PointerToConnection()
            if self.listener.getNewConnection(connection):
                connection = connection.p()
                self.connections.append(connection)
                self.reader.addConnection(connection)
                print("Server: New connection established.")

        return task.cont

    def send(self, datagram):
        for connection in self.connections:
            self.writer.send(datagram, connection)
