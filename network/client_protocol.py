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


