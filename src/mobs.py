from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import PandaNode, Point3, Vec3, VBase3
from . import Mob


class Mobs(Mob):
    def __init__(self, mob_dic_list):
        self.grobal_clock = globalClock
        self.mobs_node = self.render.attachNewNode(PandaNode('mobs_node'))
        self.mobs_node.setPos(self.area_center)
        self.mob_obj_list = []

        for mob_dic in mob_dic_list:
            self.mob_obj_list.append(Mob(self, mob_dic))

        self.taskMgr.add(self.mobs_update, 'mobs_update')

    def mobs_update(self, task):
        dt = self.grobal_clock.getDt()
        # center_of_gravity = sum([obj.position for obj in self.mob_obj_list]) / len(self.mob_obj_list)
        center_of_gravity = sum([obj.position for obj in self.mob_obj_list], start=Vec3(0,0,0)) / len(self.mob_obj_list)
        # print(center_of_gravity)
        for mob_obj in self.mob_obj_list:
            mob_obj.update(dt, center_of_gravity)

        return task.cont
