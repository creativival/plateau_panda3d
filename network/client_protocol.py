from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from . import Protocol


class ClientProtocol(Protocol):
    def process(self, data):
        it = PyDatagramIterator(data)
        msgid = it.getUint8()

        if msgid == 0:
            return self.handleHello(it)
        elif msgid == 1:
            return self.handleQuestion(it)
        elif msgid == 2:
            return self.handleBye(it)

    def handleHello(self, it):
        self.printMessage("Client received:", it.getString())
        return self.buildReply(1, "How are you?")

    def handleQuestion(self, it):
        self.printMessage("Client received:", it.getString())
        return self.buildReply(2, "I'm fine too. Gotta run! Bye!")

    def handleBye(self, it):
        self.printMessage("Client received:", it.getString())
        return None

