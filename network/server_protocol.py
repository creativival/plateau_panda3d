from direct.distributed.PyDatagramIterator import PyDatagramIterator
from . import Protocol


class ServerProtocol(Protocol):
    def __init__(self, base):
        Protocol.__init__(self, base)

    def process(self, data):
        it = PyDatagramIterator(data)
        msg_id = it.getUint8()

        if msg_id == 0:
            # サーバーがメッセージを受信
            received_message = it.getString()
            # ウインドウにテキスト表示
            self.handle_received_message(received_message)
            # クライエント全員に転送
            self.base.broadcast_received_message(received_message)
        elif msg_id == 1:
            return self.handleQuestion(it)
        elif msg_id == 2:
            return self.handleBye(it)

