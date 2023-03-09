from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from network import NetCommon, Server, Client, Connect, Message
from src import DrawText, Window, KeyMap, Ground, Player2D, Player2Ds


class Application(ShowBase, DrawText, Window, KeyMap, Message, Player2D, Player2Ds):
    def __init__(self, network_state):
        ShowBase.__init__(self)
        self.disableMouse()

        self.area_center = Point3(0, 81, 0)
        DrawText.__init__(self)
        Window.__init__(self, network_state)
        Message.__init__(self)
        Ground.__init__(self)
        self.ground_node.setP(90)
        KeyMap.__init__(self)
        Player2Ds.__init__(self)

        # マルチプレイ
        Connect.__init__(self, network_state)


if __name__ == "__main__":
    app = Application('client')
    app.run()