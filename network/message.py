from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from network import Server, Client, ServerProtocol, ClientProtocol, Connect
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from src import DrawText


class Message:
    def __init__(self):
        self.accept('h', self.hello_func)
        self.accept('t', self.thank_you_func)
        self.accept('escape', exit)

    def display_messages(self):
        self.top_left_text.setText('\n'.join(self.messages))

    def hello_func(self):
        message = 'Hello!'

        if self.network_state == 'server':
            self.messages += [message]
            self.display_messages()

        data = PyDatagram()
        data.addUint8(0)
        data.addString(message)
        self.send_data(data)

    def thank_you_func(self):
        message = 'Thank you!'

        if self.network_state == 'server':
            self.messages += [message]
            self.display_messages()

        data = PyDatagram()
        data.addUint8(0)
        data.addString(message)
        self.send_data(data)

    def send_data(self, data):
        if self.network_state == 'server':
            self.server.send(data)
        else:
            self.client.send(data)

    def broadcast_message(self, message):
        data = PyDatagram()
        data.addUint8(0)
        data.addString(message)
        self.server.send(data)
