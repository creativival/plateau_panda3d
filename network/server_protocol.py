from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from . import Protocol


class ServerProtocol(Protocol):
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
        get_string = it.getString()
        self.printMessage("Server received:", get_string)
        return self.buildReply(0, f"{get_string}, too!")

    def handleQuestion(self, it):
        self.printMessage("Server received:", it.getString())
        return self.buildReply(1, "I'm fine. How are you?")

    def handleBye(self, it):
        self.printMessage("Server received:", it.getString())
        return self.buildReply(2, "Bye!")

