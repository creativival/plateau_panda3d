from direct.distributed.PyDatagramIterator import PyDatagramIterator
from . import Protocol


class ClientProtocol(Protocol):
    def __init__(self, base):
        Protocol.__init__(self, base)

    def process(self, data):
        it = PyDatagramIterator(data)
        msg_id = it.getUint8()

        if msg_id == 0:
            # クライエントがメッセージを受信
            user_name = it.getString()
            received_message = it.getString()
            message = f'{user_name}: {received_message}'
            # ウインドウにテキスト表示
            self.handle_received_message(message)
        elif msg_id == 1:
            # クライエントが他のクライエントのメッセージを受信
            received_message = it.getString()
            # ウインドウにテキスト表示
            self.handle_received_message(received_message)
        elif msg_id == 100:
            client_id = it.getUint8()
            self.base.player.client_id = client_id
            message = it.getString()
            # ウインドウにテキスト表示
            self.handle_received_message(message)
            self.base.top_right_text.setText(f'client{client_id}')


