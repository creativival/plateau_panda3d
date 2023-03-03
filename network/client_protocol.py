from direct.distributed.PyDatagramIterator import PyDatagramIterator
from . import Protocol


class ClientProtocol(Protocol):
    def __init__(self, base):
        self.base = base

    def process(self, data):
        it = PyDatagramIterator(data)
        msgid = it.getUint8()

        if msgid == 0:
            return self.handleTextMessage(it)
        elif msgid == 1:
            return self.handleQuestion(it)
        elif msgid == 2:
            return self.handleBye(it)

    def handleTextMessage(self, it):
        message = it.getString()
        self.printMessage('Client received:', message)
        self.base.display_messages(message)

    # def handleQuestion(self, it):
    #     self.printMessage('Client received:', it.getString())
    #     return self.buildReply(2, "I'm fine too. Gotta run! Bye!")
    #
    # def handleBye(self, it):
    #     self.printMessage('Client received:', it.getString())
    #     return None

