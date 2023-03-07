from direct.distributed.PyDatagram import PyDatagram
from panda3d.core import *
from . import Player2D
from network import NetCommon, ServerProtocol


class Players:
    def __init__(self):
        self.players = {}

    def add_player(self, key, is_guest=False):
        self.players[key] = Player2D(self, is_guest)
        print(self.players)
