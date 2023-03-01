from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from src import Window, Sound, Camera, Player, Character
import constants


class DrawPlayer(ShowBase, Sound, Camera, Player):
    def __init__(self):
        # self.area_center = Point3(0, 0, 0)
        # ShowBase.__init__(self)
        # Sound.__init__(self)
        # Camera.__init__(self)
        # Player.__init__(self)
        #
        self.accept('escape', exit)

        ShowBase.__init__(self)

        self.props = WindowProperties()
        self.props.setTitle('Panda3D')
        self.props.setSize(1200, 800)
        self.win.requestProperties(self.props)
        # self.setBackgroundColor(0, 0, 0)

        self.character_color = (1, 0, 0, 1)
        Character.__init__(self, character_face_num=1, character_hand_length=1)
        self.character_node.reparentTo(self.render)
        self.character_node.setPos(-5, 20, 3)

        self.character_color = (0, 1, 0, 1)
        Character.__init__(self, character_face_num=2, character_hand_length=1)
        self.character_node.reparentTo(self.render)
        self.character_node.setPos(0, 20, 3)

        self.character_color = (0, 0, 1, 1)
        Character.__init__(self, character_face_num=3, character_hand_length=1.5)
        self.character_node.reparentTo(self.render)
        self.character_node.setPos(5, 20, 3)

        self.character_color = (1, 1, 0, 1)
        Character.__init__(self, character_face_num=4, character_hand_length=1)
        self.character_node.reparentTo(self.render)
        self.character_node.setPos(-5, 20, 0)

        self.character_color = (1, 0, 1, 1)
        Character.__init__(self, character_face_num=5, character_hand_length=1)
        self.character_node.reparentTo(self.render)
        self.character_node.setPos(0, 20, 0)

        self.character_color = (0, 1, 1, 1)
        Character.__init__(self, character_face_num=6, character_hand_length=1.5)
        self.character_node.reparentTo(self.render)
        self.character_node.setPos(5, 20, 0)

        self.character_color = (1, 1, 1, 1)
        Character.__init__(self, character_face_num=7, character_hand_length=1.5)
        self.character_node.reparentTo(self.render)
        self.character_node.setPos(-5, 20, -3)

        self.character_color = (0.5, 0.5, 0.5, 1)
        Character.__init__(self, character_face_num=8, character_hand_length=1.5)
        self.character_node.reparentTo(self.render)
        self.character_node.setPos(0, 20, -3)

        self.character_color = (0.3, 0.3, 0.3, 1)
        Character.__init__(self, character_face_num=9, character_hand_length=1)
        self.character_node.reparentTo(self.render)
        self.character_node.setPos(5, 20, -3)


if __name__ == '__main__':
    app = DrawPlayer()
    app.run()
