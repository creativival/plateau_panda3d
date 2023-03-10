from math import isclose
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
        player = self.base.players[client_id]
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
        diff_position = player_position - player.position
        # print(player_position)
        # print(diff_position)
        if diff_position.length() < 1:
            # guest_playerとplayerを同期するため、guest_playerの速度を変更
            player.velocity = Vec3(velocity_x, velocity_y, velocity_z) + diff_position * 0.1
        else:
            # 位置、速度をダイレクトに合わせる
            player.position = Vec3(x, y, z)
            player.velocity = Vec3(velocity_x, velocity_y, velocity_z)
        player.direction = Vec3(direction_x, direction_y, direction_z)
        player.hand_length = it.getFloat32()
        player.left_angle = it.getFloat32()
        player.right_angle = it.getFloat32()
        rgb_r = it.getFloat32()
        rgb_g = it.getFloat32()
        rgb_b = it.getFloat32()
        rgb_a = it.getFloat32()

        if not (isclose(player.rgb_r, rgb_r) and isclose(player.rgb_g, rgb_g) and
                isclose(player.rgb_b, rgb_b) and isclose(player.rgb_a, rgb_a)):
            player.rgb_r = rgb_r
            player.rgb_g = rgb_g
            player.rgb_b = rgb_b
            player.rgb_a = rgb_a
            player.character_model.setColor(player.rgb_r, player.rgb_g, player.rgb_b, player.rgb_a)
            player.character_left_hand_model.setColor(player.rgb_r, player.rgb_g, player.rgb_b, player.rgb_a)
            player.character_right_hand_model.setColor(player.rgb_r, player.rgb_g, player.rgb_b, player.rgb_a)

        character_face_num = it.getInt8()

        if character_face_num != player.character_face_num:
            player.character_face_num = character_face_num
            player.cat_tex = self.base.loader.loadTexture(
                f'models/maps/cat{character_face_num}.png')
            player.character_model.setTexture(player.cat_tex, 1)

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
