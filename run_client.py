from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from network import NetCommon, Server, Client, Connect, Message
from src import DrawText, KeyMap, Ground, Player2D, Players


class Application(ShowBase, DrawText, KeyMap, Message, Player2D, Players):
    def __init__(self, network_state):
        ShowBase.__init__(self)
        self.disableMouse()

        self.area_center = Point3(0, 81, 0)
        DrawText.__init__(self)
        Message.__init__(self)
        Ground.__init__(self)
        self.ground_node.setP(90)
        KeyMap.__init__(self)
        Players.__init__(self)
        self.add_player('myself')

        self.props = WindowProperties()
        self.props.setTitle(network_state)
        self.win.requestProperties(self.props)

        # マルチプレイ
        Connect.__init__(self, network_state)

        self.accept('escape', exit)


if __name__ == "__main__":
    app = Application('client')
    app.run()