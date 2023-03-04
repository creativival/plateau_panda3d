from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator


class Protocol:
    def process(self, data):
        return None

    def printMessage(self, title, msg):
        print('%s %s' % (title, msg))

    def buildReply(self, msgid, data):
        reply = PyDatagram()
        reply.addUint8(msgid)
        reply.addString(data)
        return reply

    def handle_received_message(self, received_message):
        self.printMessage('received message:', received_message)
        self.base.display_messages(received_message)
