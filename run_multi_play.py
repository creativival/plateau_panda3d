from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from network import Connect, Message
from src import DrawText, Window, KeyMap, Ground, Player2Ds


class Application(ShowBase, DrawText, Window, KeyMap, Message, Player2Ds, Connect):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()

        self.area_center = Point3(0, 81, 0)
        DrawText.__init__(self)
        Window.__init__(self, 'multi play')
        Ground.__init__(self)
        self.ground_node.setP(90)
        KeyMap.__init__(self)
        Player2Ds.__init__(self)

        # マルチプレイ
        Message.__init__(self)
        # F10 サーバー開始 / F11 クライエントとして接続
        Connect.__init__(self)


if __name__ == "__main__":
    app = Application()
    app.run()
