from direct.distributed.PyDatagramIterator import PyDatagramIterator
from panda3d.core import *
from . import Protocol


class ClientProtocol(Protocol):
    def __init__(self, base):
        Protocol.__init__(self, base)

    def process(self, data):
        it = PyDatagramIterator(data)
        msg_id = it.getUint8()

        if msg_id == 0:
            client_id = it.getUint8()
            self.base.player.client_id = client_id
            message = it.getString()
            # ウインドウにテキスト表示
            self.handle_received_message(message)
            self.base.top_right_text.setText(f'client{client_id}')
        elif msg_id == 10:
            # クライエントがサーバーからのメッセージを受信
            user_name = it.getString()
            received_message = it.getString()
            message = f'{user_name}: {received_message}'
            # ウインドウにテキスト表示
            self.handle_received_message(message)
        elif msg_id == 11:
            # クライエントが他のクライエントのメッセージを受信
            received_message = it.getString()
            # ウインドウにテキスト表示
            self.handle_received_message(received_message)
        elif msg_id == 20:  # sync player
            client_id = it.getUint8()
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
            # server_playerとplayerの位置の差を求める
            player_position = Point3(x, y, z)
            diff_position = player_position - self.base.server_player.position
            # print(player_position)
            # print(diff_position)
            if diff_position.length() < 1:
                # server_playerとplayerを同期するため、server_playerの速度を変更
                self.base.server_player.velocity = Vec3(velocity_x, velocity_y, velocity_z) + diff_position * 0.1
            else:
                # 位置、速度をダイレクトに合わせる
                self.base.server_player.position = Vec3(x, y, z)
                self.base.server_player.velocity = Vec3(velocity_x, velocity_y, velocity_z)
            self.base.server_player.direction = Vec3(direction_x, direction_y, direction_z)
            self.base.server_player.has_moving_hands = has_moving_hands


