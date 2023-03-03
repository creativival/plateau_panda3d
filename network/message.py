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
        if self.network_state == 'server':
            self.display_messages(message)
            self.server.send(message)
        else:
            self.client.send(message)

    def broadcast_message(self, message):
        data = PyDatagram()
        data.addUint8(0)
        data.addString(message)
        self.server.send(message)
