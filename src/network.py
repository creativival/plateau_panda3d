from panda3d.core import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from time import sleep, time


class NetCommon:
    def __init__(self, protocol):
        self.manager = ConnectionManager()
        self.reader = QueuedConnectionReader(self.manager, 0)
        self.writer = ConnectionWriter(self.manager, 0)
        self.protocol = protocol

        self.taskMgr.add(self.updateReader, "updateReader")

    def updateReader(self, task):
        if self.reader.dataAvailable():
            data = NetDatagram()
            self.reader.getData(data)
            reply = self.protocol.process(data)
            if reply != None:
                self.writer.send(reply, data.getConnection())
        return task.cont

    def blockChange(self, base):
        sync = PyDatagram()
        sync.addInt8(102)  # sync block change
        for block_change in base.block_changes:
            x, y, z, block_id = block_change
            sync.addString(f'{x},{y},{z},{block_id}')
        base.block_changes = []
        sync.addString('end')
        return sync

    def playerState(self, base):
        sync = PyDatagram()
        sync.addInt8(100)  # sync player
        sync.addFloat32(base.player.velocity.getX())
        sync.addFloat32(base.player.velocity.getY())
        sync.addFloat32(base.player.velocity.getZ())
        sync.addFloat32(base.player.position.getX())
        sync.addFloat32(base.player.position.getY())
        sync.addFloat32(base.player.position.getZ())
        sync.addFloat32(base.player.direction.getX())
        sync.addFloat32(base.player.direction.getY())
        sync.addFloat32(base.player.direction.getZ())
        sync.addInt8(base.player.has_moving_hands)
        return sync


class Server(NetCommon):
    def __init__(self, base, protocol, port):
        NetCommon.__init__(self, protocol)
        self.network_state = 'server'
        self.base = base
        self.listener = QueuedConnectionListener(self.manager, 0)
        socket = self.manager.openTCPServerRendezvous(port, 100)
        self.listener.addConnection(socket)
        self.connections = []

        # 接続待機して、クライエントの接続があればコネクションを作る
        self.base.taskMgr.add(self.updateListener, "updateListener")
        # 0.5秒間隔でplayerの位置、速度をクライエントに送って、guest_playerの位置を同期
        self.base.taskMgr.doMethodLater(0.5, self.sendPlayerState, "sendPlayerState")
        # 0.5秒間隔でmobの位置、速度をクライエントに送って、mobの位置を同期
        self.base.taskMgr.doMethodLater(0.5, self.sendMobState, "sendMobState")
        # 0.5秒間隔でブロックの変更をクライエントに送って、ブロックの位置を同期
        self.base.taskMgr.doMethodLater(0.5, self.sendBlockChanges, "sendBlockChanges")

    def updateListener(self, task):
        if self.listener.newConnectionAvailable():
            connection = PointerToConnection()
            if self.listener.getNewConnection(connection):
                connection = connection.p()
                self.connections.append(connection)
                self.reader.addConnection(connection)
                print("Server: New connection established.")

        return task.cont

    def sendPlayerState(self, task):
        sync = self.playerState(self.base)
        self.broadcast(sync)
        return task.again

    def sendMobState(self, task):
        sync = PyDatagram()
        sync.addInt8(101)  # sync mobs
        for mob in self.base.mobs:
            x, y, z = mob.position
            velocity_x, velocity_y, velocity_z = mob.velocity
            object_name = f'{mob.model_name}_{mob.color_id}'
            sync.addString(f'{x},{y},{z},{velocity_x},{velocity_y},{velocity_z},{object_name}')
        sync.addString('end')
        self.broadcast(sync)
        return task.again

    def sendBlockChanges(self, task):
        sync = self.blockChange(self.base)
        self.broadcast(sync)
        return task.again

    def broadcast(self, datagram):
        for conn in self.connections:
            self.writer.send(datagram, conn)


class Client(NetCommon):
    def __init__(self, base, protocol):
        NetCommon.__init__(self, protocol)
        self.base = base
        self.network_state = 'client'

        # 0.5秒間隔でplayerの位置、速度をホストに送って、guest_playerの位置を同期
        self.base.taskMgr.doMethodLater(0.5, self.sendPlayerState, "sendPlayerState")
        # 0.5秒間隔でブロックの変更をホストに送って、ブロックの位置を同期
        self.base.taskMgr.doMethodLater(0.5, self.sendBlockChanges, "sendBlockChanges")

    # サーバーと接続する
    def connect(self, host, port, timeout):
        self.connection = self.manager.openTCPClientConnection(host, port, timeout)
        if self.connection:
            self.reader.addConnection(self.connection)
            print("Client: Connected to server.")
            # first message
            data = PyDatagram()
            data.addInt8(0)
            data.addString("Hello!")
            self.send(data)
            # send guest player position
            sync = PyDatagram()
            sync.addInt8(-1)
            x, y, z = self.base.player.position
            object_name = 'player'
            guest_player_position = f'{x},{y},{z},{object_name}'
            sync.addString(guest_player_position)
            self.send(sync)

    def sendPlayerState(self, task):
        sync = self.playerState(self.base)
        self.send(sync)
        return task.again

    def sendBlockChanges(self, task):
        sync = self.blockChange(self.base)
        self.send(sync)
        return task.again

    def send(self, datagram):
        if self.connection:
            self.writer.send(datagram, self.connection)


class Protocol:
    def __init__(self, base):
        self.base = base

    def process(self, data):
        # playerの速度と位置を受信
        it = PyDatagramIterator(data)
        msg_id = it.getInt8()
        # print('Protocol:', msg_id)
        if msg_id == 100:  # sync player
            velocity_x = it.getFloat32()
            velocity_y = it.getFloat32()
            velocity_z = it.getFloat32()
            x = it.getFloat32()
            y = it.getFloat32()
            z = it.getFloat32()
            direction_x = it.getFloat32()
            direction_y = it.getFloat32()
            direction_z = it.getFloat32()
            has_moving_hands = it.getInt8()
            # guest_playerとplayerの位置の差を求める
            player_position = Point3(x, y, z)
            diff_position = player_position - self.base.guest_player.position
            # print(player_position)
            # print(diff_position)
            if diff_position.length() < 1:
                # guest_playerとplayerを同期するため、guest_playerの速度を変更
                self.base.guest_player.velocity = Vec3(velocity_x, velocity_y, velocity_z) + diff_position * 0.1
            else:
                # 位置、速度をダイレクトに合わせる
                self.base.guest_player.position = Vec3(x, y, z)
                self.base.guest_player.velocity = Vec3(velocity_x, velocity_y, velocity_z)
            self.base.guest_player.direction = Vec3(direction_x, direction_y, direction_z)
            self.base.guest_player.has_moving_hands = has_moving_hands
            return None
        elif msg_id == 10:  # chat
            received_text = it.getString()
            self.printMessage("Protocol received:", received_text)
            self.base.console_window.setText(received_text)
            self.base.console_window.start_time = time()
            return None
        elif msg_id == 102:  # sync block changes
            while True:
                received_text = it.getString()
                if received_text == 'end':
                    break
                x, y, z, block_id = received_text.split(',')
                x, y, z = int(x), int(y), int(z)
                if block_id == 'remove':
                    self.base.block.remove_block_position(x, y, z)
                    self.base.block.remove_block(x, y, z)
                else:  # add block
                    self.base.block.add_block_position(x, y, z, block_id)
                    self.base.block.add_block(x, y, z, block_id)
            return None

    def printMessage(self, title, msg):
        print("%s %s" % (title, msg))

    def buildReply(self, msg_id, data):
        reply = PyDatagram()
        reply.addUint8(msg_id)
        reply.addString(data)
        return reply


class ServerProtocol(Protocol):
    def process(self, data):
        super().process(data)
        it = PyDatagramIterator(data)
        msg_id = it.getInt8()
        # print('server:', msg_id)
        if msg_id == -1:  # sync block_positions
            received_text = it.getString()
            x, y, z, object_id = received_text.split(',')
            x, y, z = float(x), float(y), float(z)
            self.base.guest_player.position = Point3(x, y, z)
            return self.sendHostWorld()
        elif msg_id == 0:  # first chat
            return self.handleHello(it)
        elif msg_id == 1:  # second chat
            return self.handleQuestion(it)
        elif msg_id == 2:  # third chat
            return self.handleBye(it)

    def sendHostWorld(self):
        sync = PyDatagram()
        sync.addInt8(-1)
        size = self.base.settings['world_size']
        # send block position
        ground_size = self.base.ground_size
        sync.addString(f'{ground_size[0]},{ground_size[1]},0,ground_size')
        cursor = self.base.db.cursor()
        cursor.execute("select * from current")
        block_positions = cursor.fetchall()
        cursor.close()
        for block_position in block_positions:
            x, y, z, block_id = block_position
            sync.addString(f'{x},{y},{z},{block_id}')
        # send mob position
        for mob in self.base.mobs:
            x, y, z = mob.position
            object_name = f'{mob.model_name}_{mob.color_id}'
            sync.addString(f'{x},{y},{z},{object_name}')
        # send player position
        x, y, z = self.base.player.position
        object_name = 'player'
        sync.addString(f'{x},{y},{z},{object_name}')
        sync.addString('end')
        return sync

    def handleHello(self, it):
        received_text = it.getString()
        self.printMessage("Server received:", received_text)
        self.base.console_window.setText(received_text)
        self.base.console_window.start_time = time()
        sleep(1)
        return self.buildReply(0, "Hello, too!")

    def handleQuestion(self, it):
        received_text = it.getString()
        self.printMessage("Server received:", received_text)
        self.base.console_window.setText(received_text)
        self.base.console_window.start_time = time()
        sleep(1)
        return self.buildReply(1, "I'm fine. How are you?")

    def handleBye(self, it):
        received_text = it.getString()
        self.printMessage("Server received:", received_text)
        self.base.console_window.setText(received_text)
        self.base.console_window.start_time = time()
        sleep(1)
        return self.buildReply(2, "Bye!")


class ClientProtocol(Protocol):
    def process(self, data):
        super().process(data)
        it = PyDatagramIterator(data)
        msg_id = it.getInt8()
        if msg_id == -1:  # sync block_positions
            return self.receiveHostWorld(it)
        elif msg_id == 0:  # first chat
            return self.handleHello(it)
        elif msg_id == 1:
            return self.handleQuestion(it)
        elif msg_id == 2:  # second chat
            return self.handleBye(it)
        elif msg_id == 101:  # sync mob
            return self.receiveMobState(it)

    def receiveHostWorld(self, it):
        self.base.clear_world()
        cursor = self.base.db.cursor()
        while True:
            received_text = it.getString()
            # self.printMessage("Client received:", received_text)
            if received_text == 'end':
                break
            obj = received_text.split(',')
            self.base.load_object(obj)
        self.base.db.commit()
        cursor.close()
        self.base.block.draw_blocks()
        return None

    def receiveMobState(self, it):
        for mob in self.base.mobs:
            received_text = it.getString()
            # self.printMessage("Client received:", received_text)
            if received_text == 'end':
                break
            obj = received_text.split(',')
            x, y, z, velocity_x, velocity_y, velocity_z, object_id = obj
            x, y, z, velocity_x, velocity_y, velocity_z = \
                float(x), float(y), float(z), float(velocity_x), float(velocity_y), float(velocity_z)
            diff_position = Point3(x, y, z) - mob.position
            if diff_position.length() < 1:
                # 位置と速度をダイレクトに合わせる
                mob.position = Point3(x, y, z)
                mob.velocity = Vec3(velocity_x, velocity_y, velocity_z)
            else:
                # mobの速度を位置の差を減少させるように補正する
                mob.velocity = Vec3(velocity_x, velocity_y, velocity_z) + diff_position * 0.1
        return None

    def handleHello(self, it):
        received_text = it.getString()
        self.printMessage("Client received:", received_text)
        self.base.console_window.setText(received_text)
        self.base.console_window.start_time = time()
        sleep(1)
        return self.buildReply(1, "How are you?")

    def handleQuestion(self, it):
        received_text = it.getString()
        self.printMessage("Client received:", received_text)
        self.base.console_window.setText(received_text)
        self.base.console_window.start_time = time()
        sleep(1)
        return self.buildReply(2, "I'm fine too. Gotta run! Bye!")

    def handleBye(self, it):
        received_text = it.getString()
        self.printMessage("Client received:", received_text)
        self.base.console_window.setText(received_text)
        self.base.console_window.start_time = time()
        return None
