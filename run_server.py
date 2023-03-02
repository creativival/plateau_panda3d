from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from network import Connect, Message
from src import DrawText


class Application(ShowBase, DrawText, Message):
    def __init__(self, network_state):
        ShowBase.__init__(self)
        DrawText.__init__(self)
        Message.__init__(self)
        Connect.__init__(self, network_state)

        self.props = WindowProperties()
        self.props.setTitle(network_state)
        self.win.requestProperties(self.props)

        self.accept('escape', exit)


if __name__ == "__main__":
    app = Application('server')
    app.run()
