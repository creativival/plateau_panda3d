from direct.distributed.PyDatagramIterator import PyDatagramIterator
from . import Protocol


class ServerProtocol(Protocol):
    def __init__(self, base):
        self.base = base

    def process(self, data):
        it = PyDatagramIterator(data)
        msgid = it.getUint8()

        if msgid == 0:
            # サーバーがメッセージを受信
            received_message = it.getString()
            # ウインドウにテキスト表示
            self.handle_received_message(received_message)
            # クライエント全員に転送
            self.base.broadcast_received_message(received_message)
        elif msgid == 1:
            return self.handleQuestion(it)
        elif msgid == 2:
            return self.handleBye(it)

    # def broadcast_message(self, it):
    #     message = it.getString()
    #     self.base.display_messages(message)
    #     self.base.broadcast_message(message)


    # def handle_received_message(self, it):
    #     message = it.getString()
    #     self.printMessage('Server received:', message)
    #     self.base.messages += [message]
    #     self.base.display_messages()
    #     # return self.buildReply(0, f'{get_string}, too!')

    # def handleQuestion(self, it):
    #     self.printMessage('Server received:', it.getString())
    #     return self.buildReply(1, "I'm fine. How are you?")
    #
    # def handleBye(self, it):
    #     self.printMessage('Server received:', it.getString())
    #     return self.buildReply(2, 'Bye!')

