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

    def sync_player_state(self, it, client_id):
        velocity_x = it.getFloat32()
        velocity_y = it.getFloat32()
        velocity_z = it.getFloat32()
        x = it.getFloat32()
        y = it.getFloat32()
        z = it.getFloat32()
        direction_x = it.getFloat32()
        direction_y = it.getFloat32()
        direction_z = it.getFloat32()
        has_moving_hands = it.getInt8()
        # guest_playerとplayerの位置の差を求める
        player_position = Point3(x, y, z)
        diff_position = player_position - self.players[client_id].position
        # print(player_position)
        # print(diff_position)
        if diff_position.length() < 1:
            # guest_playerとplayerを同期するため、guest_playerの速度を変更
            self.players[client_id].velocity = Vec3(velocity_x, velocity_y, velocity_z) + diff_position * 0.1
        else:
            # 位置、速度をダイレクトに合わせる
            self.players[client_id].position = Vec3(x, y, z)
            self.players[client_id].velocity = Vec3(velocity_x, velocity_y, velocity_z)
        self.players[client_id].direction = Vec3(direction_x, direction_y, direction_z)
        self.players[client_id].has_moving_hands = has_moving_hands

    def broadcast_client_state(self, data):
        self.server.broadcast(data)

