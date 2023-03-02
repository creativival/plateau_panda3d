from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from network import Server, Client, ServerProtocol, ClientProtocol, Connect, Message
from src import DrawText
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator


class Application(ShowBase, DrawText, Message):
    def __init__(self, network_state):
        ShowBase.__init__(self)
        DrawText.__init__(self)

        self.network_state = network_state
        self.messages = ['message1', 'message2', 'message3']
        self.top_left_text = self.draw_2d_text('', parent=self.a2dTopLeft)

        Connect.__init__(self, network_state)
        Message.__init__(self)

        self.props = WindowProperties()
        self.props.setTitle(network_state)
        self.win.requestProperties(self.props)

        self.display_messages()


if __name__ == "__main__":
    app = Application('client')
    app.run()