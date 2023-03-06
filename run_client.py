from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from network import NetCommon, Server, Client, Connect, Message
from src import DrawText, KeyMap, Ground, Player2D


class Application(ShowBase, DrawText, KeyMap, NetCommon, Server, Client, Message, Player2D):
    def __init__(self, network_state):
        self.area_center = Point3(0, 81, 0)
        ShowBase.__init__(self)
        DrawText.__init__(self)
        Message.__init__(self)
        NetCommon.__init__(self)
        Connect.__init__(self, network_state)
        Ground.__init__(self)
        KeyMap.__init__(self)
        self.player = Player2D(self)

        self.ground_node.setP(90)

        self.props = WindowProperties()
        self.props.setTitle(network_state)
        self.win.requestProperties(self.props)

        self.accept('escape', exit)


if __name__ == "__main__":
    app = Application('client')
    app.run()