from math import sin, cos, radians, floor
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import *


class Character:
    def __init__(self):
        self.cat_tex = self.loader.loadTexture("models/maps/cat.png")
        self.cat_ear_tex = self.loader.loadTexture("models/maps/cat_ear.png")

        self.character_node = NodePath('character_node')

        # モデル
        self.character_color = (1, 1, 0, 1)

        self.character_model = self.loader.loadModel("models/egg_shape32")
        self.character_model.reparentTo(self.character_node)
        self.character_model.setTexture(self.cat_tex, 1)
        self.character_model.setScale(1.41, 1.2, 1)
        self.character_model.setPos(0, 0, 0)
        self.character_model.setHpr(0, 0, 0)
        self.character_model.setColor(*self.character_color)
        self.character_model.setTransparency(TransparencyAttrib.MBinary)

        self.character_left_hand_model = self.loader.loadModel("models/egg_shape32")
        self.character_left_hand_model.reparentTo(self.character_node)
        self.character_left_hand_model.setTexture(self.cat_ear_tex, 1)
        self.character_left_hand_model.setScale(1, 0.3, 1)
        self.character_left_hand_model.setPos(0.3, 0, 0.3)
        self.character_left_hand_model.setHpr(0, 0, 45)
        self.character_left_hand_model.setColor(*self.character_color)
        self.character_left_hand_model.setTransparency(TransparencyAttrib.MBinary)

        self.character_right_hand_model = self.loader.loadModel("models/egg_shape32")
        self.character_right_hand_model.reparentTo(self.character_node)
        self.character_right_hand_model.setTexture(self.cat_ear_tex, 1)
        self.character_right_hand_model.setScale(1, 0.3, 1)
        self.character_right_hand_model.setPos(-0.3, 0, 0.3)
        self.character_right_hand_model.setHpr(0, 0, -45)
        self.character_right_hand_model.setColor(*self.character_color)
        self.character_right_hand_model.setTransparency(TransparencyAttrib.MBinary)

        # 表情の変更
        for i in range(1, 10):
            self.accept(str(i), self.change_face, [i])

    def change_face(self, i):
        self.cat_tex = self.loader.loadTexture(f'models/maps/cat{i}.png')
