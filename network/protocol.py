from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator


class Protocol:
    def __init__(self, base):
        self.base = base

    def process(self, data):
        return None

    def handle_received_message(self, received_message):
        self.print_message('received message:', received_message)
        self.base.display_messages(received_message)

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
        # guest_playerとplayerの位置の差を求める
        player_position = Point3(x, y, z)
        diff_position = player_position - self.base.players[client_id].position
        # print(player_position)
        # print(diff_position)
        if diff_position.length() < 1:
            # guest_playerとplayerを同期するため、guest_playerの速度を変更
            self.base.players[client_id].velocity = Vec3(velocity_x, velocity_y, velocity_z) + diff_position * 0.1
        else:
            # 位置、速度をダイレクトに合わせる
            self.base.players[client_id].position = Vec3(x, y, z)
            self.base.players[client_id].velocity = Vec3(velocity_x, velocity_y, velocity_z)
        self.base.players[client_id].direction = Vec3(direction_x, direction_y, direction_z)
        self.base.players[client_id].hand_length = it.getFloat32()
        self.base.players[client_id].left_angle = it.getFloat32()
        self.base.players[client_id].right_angle = it.getFloat32()

    def broadcast_client_state(self, data):
        self.base.server.broadcast(data)

    @staticmethod
    def print_message(title, msg):
        print('%s %s' % (title, msg))

    @staticmethod
    def build_reply(msg_id, data):
        reply = PyDatagram()
        reply.addUint8(msg_id)
        reply.addString(data)
        return reply

