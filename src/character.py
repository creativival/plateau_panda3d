from math import sin, cos, radians, floor
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase


class Character:
    def __init__(self, character_color=(1, 1, 1, 1)):
        self.character_node = NodePath('character_node')

        # モデル
        self.cat_tex = self.loader.loadTexture('models/maps/cat.png')
        self.cat_ear_tex = self.loader.loadTexture('models/maps/cat_ear.png')
        self.character_color = character_color
        self.character_face_num = 1
        self.character_hand_length = 1

        self.character_model = self.loader.loadModel('models/egg_shape32')
        self.character_model.reparentTo(self.character_node)
        self.character_model.setTexture(self.cat_tex, 1)
        self.character_model.setScale(1.41, 1.2, 1)
        self.character_model.setPos(0, 0, 0)
        self.character_model.setHpr(0, 0, 0)
        self.character_model.setColor(*self.character_color)
        self.character_model.setTransparency(TransparencyAttrib.MBinary)

        self.character_left_hand_model_node = self.character_node.attachNewNode(
            PandaNode('character_left_hand_model_node'))
        self.character_left_hand_model_node.setPos(0.3, 0, 0.3)
        self.character_left_hand_model_node.setHpr(0, 0, 35)

        self.character_left_hand_model = self.loader.loadModel('models/egg_shape32')
        self.character_left_hand_model.reparentTo(self.character_left_hand_model_node)
        self.character_left_hand_model.setTexture(self.cat_ear_tex, 1)
        self.character_left_hand_model.setScale(0.5, 0.3, 0.8)
        self.character_left_hand_model.setPos(0, 0, 0.4)
        self.character_left_hand_model.setColor(*self.character_color)
        self.character_left_hand_model.setTransparency(TransparencyAttrib.MBinary)

        self.character_right_hand_model_node = self.character_node.attachNewNode(
            PandaNode('character_right_hand_model_node'))
        self.character_right_hand_model_node.setPos(-0.3, 0, 0.3)
        self.character_right_hand_model_node.setHpr(0, 0, -35)

        self.character_right_hand_model = self.loader.loadModel('models/egg_shape32')
        self.character_right_hand_model.reparentTo(self.character_right_hand_model_node)
        self.character_right_hand_model.setTexture(self.cat_ear_tex, 1)
        self.character_right_hand_model.setScale(0.5, 0.3, 0.8)
        self.character_right_hand_model.setPos(0, 0, 0.4)
        self.character_right_hand_model.setColor(*self.character_color)
        self.character_right_hand_model.setTransparency(TransparencyAttrib.MBinary)

        # 表情の変更
        for i in range(1, 10):
            self.accept(str(i), self.change_face, [i])

    def change_face(self, i):
        print(i)
        self.character_face_num = i
        self.cat_tex = self.loader.loadTexture(f'models/maps/cat{i}.png')
        self.character_model.setTexture(self.cat_tex, 1)
        if i in [3, 6, 7, 9]:
            self.character_hand_length = 1.5
        else:
            self.character_hand_length = 1
