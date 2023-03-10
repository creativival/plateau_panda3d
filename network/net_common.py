from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator


class NetCommon:
    def __init__(self, base):
        self.base = base
        self.manager = ConnectionManager()
        self.reader = QueuedConnectionReader(self.manager, 0)
        self.writer = ConnectionWriter(self.manager, 0)

        self.base.taskMgr.add(self.update_reader, 'update_reader')

    def update_reader(self, task):
        if self.reader.dataAvailable():
            data = NetDatagram()
            self.reader.getData(data)
            reply = self.protocol.process(data)

            if reply is not None:
                self.writer.send(reply, data.getConnection())

        return task.cont

    def player_state(self, client_id=0):
        sync = PyDatagram()
        sync.addInt8(20)  # sync player
        sync.addInt8(client_id)
        sync.addFloat32(self.base.players['myself'].velocity.getX())
        sync.addFloat32(self.base.players['myself'].velocity.getY())
        sync.addFloat32(self.base.players['myself'].velocity.getZ())
        sync.addFloat32(self.base.players['myself'].position.getX())
        sync.addFloat32(self.base.players['myself'].position.getY())
        sync.addFloat32(self.base.players['myself'].position.getZ())
        sync.addFloat32(self.base.players['myself'].direction.getX())
        sync.addFloat32(self.base.players['myself'].direction.getY())
        sync.addFloat32(self.base.players['myself'].direction.getZ())
        sync.addFloat32(self.base.players['myself'].hand_length)
        sync.addFloat32(self.base.players['myself'].left_angle)
        sync.addFloat32(self.base.players['myself'].right_angle)
        sync.addFloat32(self.base.players['myself'].rgb_r)
        sync.addFloat32(self.base.players['myself'].rgb_g)
        sync.addFloat32(self.base.players['myself'].rgb_b)
        sync.addFloat32(self.base.players['myself'].rgb_a)
        sync.addInt8(self.base.players['myself'].character_face_num)
        return sync

    # def sendMobState(self, task):
    #     sync = PyDatagram()
    #     sync.addInt8(101)  # sync mobs
    #     for mob in self.base.mobs:
    #         x, y, z = mob.position
    #         velocity_x, velocity_y, velocity_z = mob.velocity
    #         object_name = f'{mob.model_name}_{mob.color_id}'
    #         sync.addString(f'{x},{y},{z},{velocity_x},{velocity_y},{velocity_z},{object_name}')
    #     sync.addString('end')
    #     self.broadcast(sync)
    #     return task.again

    # def sendBlockChanges(self, task):
    #     sync = self.blockChange(self.base)
    #     self.broadcast(sync)
    #     return task.again
