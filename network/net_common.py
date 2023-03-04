from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator


class NetCommon:
    def __init__(self, protocol):
        self.manager = ConnectionManager()
        self.reader = QueuedConnectionReader(self.manager, 0)
        self.writer = ConnectionWriter(self.manager, 0)
        self.protocol = protocol

        self.base.taskMgr.add(self.updateReader, 'updateReader')

    def updateReader(self, task):
        if self.reader.dataAvailable():
            data = NetDatagram()
            self.reader.getData(data)
            reply = self.protocol.process(data)

            if reply != None:
                self.writer.send(reply, data.getConnection())

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
