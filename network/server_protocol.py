from direct.distributed.PyDatagramIterator import PyDatagramIterator
from . import Protocol


class ServerProtocol(Protocol):
    def __init__(self, base):
        Protocol.__init__(self, base)

    def process(self, data):
        it = PyDatagramIterator(data)
        msg_id = it.getUint8()
        user_name = it.getString()

        if msg_id == 0:
            # サーバーがメッセージを受信
            received_message = it.getString()
            message = f'{user_name}: {received_message}'
            # ウインドウにテキスト表示
            self.handle_received_message(message)
            # クライエント全員に転送
            self.base.broadcast_received_message(message)
        elif msg_id == 1:
            return self.handleQuestion(it)
        elif msg_id == 2:
            return self.handleBye(it)

