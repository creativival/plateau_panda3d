from math import sin, cos, radians, atan2, degrees
from panda3d.core import *
from direct.showbase.ShowBaseGlobal import globalClock
from network import Connect, Message
from src import DrawText


class Player2D:
    def __init__(self):
        self.disableMouse()

        self.player = self.render.attachNewNode(PandaNode('player'))
        self.player_model_node = self.player.attachNewNode(PandaNode('player_model_node'))
        self.player_model_node.setHpr(0, -60, 180)
        self.player_model = self.loader.loadModel('models/smiley')
        self.player_model.reparentTo(self.player_model_node)
        self.player_position = Point3(0, 80, 0)
        self.player_velocity = Vec3(0, 0, 0)
        self.player_move_speed = 10
        self.player_phi = 0
        self.player.reparentTo(self.render)
        self.player.setPos(self.player_position)
        if self.network_state == 'client':
            self.player.setColor(0, 0, 1, 0.5)

        # move the player
        self.taskMgr.add(self.update, 'update')

    def draw(self):
        self.player.setPos(self.player_position)

    def set_direction(self):
        if self.mouseWatcherNode.hasMouse():
            mouse_pos = self.mouseWatcherNode.getMouse()
            x = mouse_pos.x
            y = mouse_pos.y
            self.player_phi = degrees(atan2(y, x)) - 90
            # print(x, y)
            # print(self.player_phi)
            self.player.setR(-self.player_phi)
            # heading = -x * self.max_heading_angle
            # pitch = -y * self.max_pitch_angle

    def set_velocity(self):
        key_map = self.key_map

        if key_map['w'] or key_map['a'] or key_map['s'] or key_map['d']:
            add_angle = 0
            if key_map['w'] and key_map['a']:
                add_angle += 215 - 90
            elif key_map['a'] and key_map['s']:
                add_angle += 315 - 90
            elif key_map['s'] and key_map['d']:
                add_angle += 45 - 90
            elif key_map['d'] and key_map['w']:
                add_angle += 135 - 90
            elif key_map['w']:
                add_angle += 180 - 90
            elif key_map['a']:
                add_angle += 270 - 90
            elif key_map['s']:
                add_angle += 0 - 90
            elif key_map['d']:
                add_angle += 90 - 90

            self.player_velocity = \
                Vec3(
                    cos(radians(add_angle + self.player_phi)),
                    0,
                    sin(radians(add_angle + self.player_phi))
                ) * self.player_move_speed
        else:
            self.player_velocity = Vec3(0, 0, 0)

    def set_position(self):
        dt = globalClock.getDt()
        self.player_position = self.player_position + self.player_velocity * dt

    def update(self, task):
        self.set_direction()
        self.set_velocity()
        self.set_position()
        self.draw()
        return task.cont