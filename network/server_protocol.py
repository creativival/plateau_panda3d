from direct.distributed.PyDatagramIterator import PyDatagramIterator
from panda3d.core import *
from . import Protocol


class ServerProtocol(Protocol):
    def __init__(self, base):
        Protocol.__init__(self, base)

    def process(self, data):
        it = PyDatagramIterator(data)
        msg_id = it.getUint8()

        if msg_id == 10:
            user_name = it.getString()
            # サーバーがクライエントからのメッセージを受信
            received_message = it.getString()
            message = f'{user_name}: {received_message}'
            # ウインドウにテキスト表示
            self.handle_received_message(message)
            # クライエント全員に転送
            self.base.broadcast_received_message(message)
        elif msg_id == 20:  # クライエントの位置と向きを同期
            client_id = it.getUint8()
            self.sync_player_state(it, client_id)
            
            # 別のクライエントに転送
            self.broadcast_client_state(data)
            

