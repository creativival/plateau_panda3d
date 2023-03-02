from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from network import Server, Client, ServerProtocol, ClientProtocol
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator


class Application(ShowBase):
    def __init__(self, network_state):
        self.network_state = network_state
        ShowBase.__init__(self)
        self.props = WindowProperties()
        self.props.setTitle(network_state)
        self.win.requestProperties(self.props)

        if self.network_state == 'server':
            self.server = Server(ServerProtocol(), 9999)
            self.client = None
        else:  # 'client'
            self.server = None
            self.client = Client(ClientProtocol())
            self.client.connect("localhost", 9999, 3000)

        self.accept('h', self.hello_func)
        self.accept('t', self.thank_you_func)
        self.accept('escape', exit)

    def hello_func(self):
        data = PyDatagram()
        data.addUint8(0)
        data.addString("Hello!")
        self.send_data(data)

    def thank_you_func(self):
        data = PyDatagram()
        data.addUint8(0)
        data.addString("Thank you!")
        self.send_data(data)

    def send_data(self, data):
        if self.network_state == 'server':
            self.server.send(data)
        else:
            self.client.send(data)


if __name__ == "__main__":
    gameApp = Application('server')
    gameApp.run()
