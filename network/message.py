from direct.distributed.PyDatagram import PyDatagram
from direct.stdpy import threading


class Message:
    def __init__(self):
        self.messages = []
        self.top_left_text = self.draw_2d_text('', parent=self.a2dTopLeft)

        self.accept('h', self.send_message, ['Hello!'])
        self.accept('t', self.send_message, ['thank you!'])

    def display_messages(self, message):
        if len(self.messages) > 5:
            self.messages.pop(0)
        self.messages += [message]
        self.show_message()
        self.top_left_text.setText('\n'.join(self.messages))
        timer = threading.Timer(3, self.hide_message)
        timer.start()

    def show_message(self):
        if self.top_left_text.isHidden():
            self.top_left_text.show()

    def hide_message(self):
        if not self.top_left_text.isHidden():
            self.top_left_text.hide()

    def send_message(self, message):
        data = PyDatagram()
        data.addUint8(0)
        data.addString(message)

        if self.network_state == 'server':
            # サーバーがメッセージを送信
            # ウインドウにテキスト表示
            self.display_messages(message)
            # クライエント全員に送信
            self.server.broadcast(data)
        else:
            # クライエントがメッセージを送信
            # サーバーにメッセージを送信
            self.client.send(data)

    def broadcast_received_message(self, received_message):
        # クライエントから受信したメッセージを全クライエントに再送信
        data = PyDatagram()
        data.addUint8(0)
        data.addString(received_message)
        self.server.broadcast(data)
