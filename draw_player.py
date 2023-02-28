from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from src import Sound, Camera, Player
import constants


class DrawPlayer(ShowBase, Sound, Camera, Player):
    def __init__(self):
        self.area_center = Point3(0, 0, 0)
        ShowBase.__init__(self)
        Sound.__init__(self)
        Camera.__init__(self)
        Player.__init__(self)

        self.accept('escape', exit)


if __name__ == '__main__':
    app = DrawPlayer()
    app.run()
