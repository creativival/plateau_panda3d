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
            self.base.players['myself'].client_id = client_id
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
        elif msg_id == 20:  # サーバーと自分以外もクライエントを同期
            client_id = it.getUint8()

            if client_id != self.base.players['myself'].client_id:
                # 自分からの送信でない
                if (client_id != 0 and  # サーバーからの送信でない
                        client_id not in self.base.players):
                    # 自分以外のクライエントいるとき作成
                    self.base.add_player(client_id, is_guest=True)

                self.sync_player_state(it, client_id)
        elif msg_id == 30:  # モブを同期
            for mob in self.base.mob_obj_list:
                received_text = it.getString()
                # self.printMessage("Client received:", received_text)
                x, y, z, velocity_x, velocity_y, velocity_z, direction_x, direction_y, direction_z = \
                    map(float, received_text.split(','))
                diff_position = Point3(x, y, z) - mob.position
                mob.direction = Vec3(direction_x, direction_y, direction_z)
                # if diff_position.length() < 1:
                if True:
                    # 位置と速度をダイレクトに合わせる
                    mob.position = Point3(x, y, z)
                    mob.velocity = Vec3(velocity_x, velocity_y, velocity_z)
                else:
                    # mobの速度を位置の差を減少させるように補正する
                    mob.velocity = Vec3(velocity_x, velocity_y, velocity_z) + diff_position * 0.1


