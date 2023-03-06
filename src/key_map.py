from math import sin, cos, radians, floor
from time import time
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import *
from panda3d.core import *


class KeyMap:
    def __init__(self):
        # key_map
        self.key_map = {
            'w': False,
            'a': False,
            's': False,
            'd': False,
            'space': False,
            'mouse1': False,
            'mouse2': False,
            'mouse3': False,
        }

        self.accept('w', self.update_key_map, ['w', True])
        self.accept('w-up', self.update_key_map, ['w', False])
        self.accept('a', self.update_key_map, ['a', True])
        self.accept('a-up', self.update_key_map, ['a', False])
        self.accept('s', self.update_key_map, ['s', True])
        self.accept('s-up', self.update_key_map, ['s', False])
        self.accept('d', self.update_key_map, ['d', True])
        self.accept('d-up', self.update_key_map, ['d', False])
        self.accept('space', self.update_key_map, ['space', True])
        self.accept('space-up', self.update_key_map, ['space', False])
        self.accept('mouse1', self.update_key_map, ['mouse1', True])
        self.accept('mouse1-up', self.update_key_map, ['mouse1', False])
        self.accept('mouse2', self.update_key_map, ['mouse2', True])
        self.accept('mouse2-up', self.update_key_map, ['mouse2', False])
        self.accept('mouse3', self.update_key_map, ['mouse3', True])
        self.accept('mouse3-up', self.update_key_map, ['mouse3', False])

    def update_key_map(self, key_name, key_state):
        # print(key_name, key_state)
        self.key_map[key_name] = key_state
