from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator


class Protocol:
    def __init__(self, base):
        self.base = base

    def process(self, data):
        return None

    def handle_received_message(self, received_message):
        self.print_message('received message:', received_message)
        self.base.display_messages(received_message)

    @staticmethod
    def print_message(title, msg):
        print('%s %s' % (title, msg))

    @staticmethod
    def build_reply(msg_id, data):
        reply = PyDatagram()
        reply.addUint8(msg_id)
        reply.addString(data)
        return reply

