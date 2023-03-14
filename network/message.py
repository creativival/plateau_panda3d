from direct.distributed.PyDatagram import PyDatagram
from direct.stdpy import threading
from panda3d.core import *
from direct.gui.DirectGui import *


class Message:
    def __init__(self):
        self.accept('h', self.send_hello_message)

    def toggle_text_field(self):
        if self.text_field.isHidden():
            self.text_field.show()
            self.is_open_text_field = True
            self.text_field.setFocus()
        else:
            self.text_field.hide()
            self.is_open_text_field = False

    def send_chat(self, text):
        if text:
            self.send_message(text)
            self.text_field.enterText('')
            self.text_field.hide()
            self.is_open_text_field = False

    def display_messages(self, message):
        if len(self.messages) > 5:
            self.messages.pop(0)
        self.messages += [message]
        self.show_message()
        self.top_left_text.setText('\n'.join(self.messages))

        for timer in self.timers:
            timer.cancel()

        timer = threading.Timer(5, self.hide_message)
        timer.start()
        self.timers = [timer]

    def show_message(self):
        if self.top_left_text.isHidden():
            self.top_left_text.show()

    def hide_message(self):
        if not self.top_left_text.isHidden():
            self.top_left_text.hide()
        self.timers = []

    def send_hello_message(self):
        if not self.is_open_text_field:
            self.send_message('Hello!')

    def send_message(self, message):
        data = PyDatagram()
        data.addUint8(10)

        if self.network_state == 'server':
            # サーバーがメッセージを送信
            name = 'server'
            # ウインドウにテキスト表示
            self.display_messages(f'{name}: {message}')
            # クライエント全員に送信
            data.addString(name)
            data.addString(message)
            self.server.broadcast(data)
        elif self.network_state == 'client':
            # クライエントがメッセージを送信
            name = f'client{self.players["myself"].client_id}'
            # サーバーにメッセージを送信
            data.addString(name)
            data.addString(message)
            self.client.send(data)

    def broadcast_received_message(self, received_message):
        # クライエントから受信したメッセージを全クライエントに再送信
        data = PyDatagram()
        data.addUint8(11)
        data.addString(received_message)
        self.server.broadcast(data)
