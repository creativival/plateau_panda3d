from math import sin, cos, radians, atan2, degrees
from panda3d.core import *
from direct.showbase.ShowBaseGlobal import globalClock


class Player2D:
    def __init__(self, base, is_guest=False):
        # print('is_guest:', is_guest)
        self.base = base
        self.is_guest = is_guest
        self.client_id = 0

        self.player_base_node = self.base.render.attachNewNode(PandaNode('player_base_node'))
        self.model_node = self.player_base_node.attachNewNode(PandaNode('model_node'))
        self.model_node.setHpr(0, -60, 180)
        self.model = self.base.loader.loadModel('models/smiley')
        self.model.reparentTo(self.model_node)
        self.position = Point3(0, 80, 0)
        self.velocity = Vec3(0, 0, 0)
        self.direction = Vec3(0, 0, 0)
        self.hand_length = 0
        self.left_angle = 0
        self.right_angle = 0
        self.guest_face_num = 1
        self.move_speed = 10
        # self.phi = 0
        self.player_base_node.reparentTo(self.base.render)
        self.player_base_node.setPos(self.position)
        if is_guest:
            self.player_base_node.setColor(0, 0, 1, 0.5)

        # move the player
        self.base.taskMgr.add(self.player_update, 'player_update')

    def player_draw(self):
        self.player_base_node.setPos(self.position)
        self.player_base_node.setHpr(self.direction)

    def set_player_direction(self):
        if (not self.is_guest and
                not self.base.is_paused_player and
                self.base.menu_node.isStashed()):
            if self.base.mouseWatcherNode.hasMouse():
                mouse_pos = self.base.mouseWatcherNode.getMouse()
                x = mouse_pos.x
                y = mouse_pos.y
                phi = degrees(atan2(y, x)) - 90
                # print(x, y)
                # print(self.phi)
                self.direction = Vec3(0, 0, -phi)
                # heading = -x * self.max_heading_angle
                # pitch = -y * self.max_pitch_angle

    def set_player_velocity(self):
        if not self.is_guest:
            key_map = self.base.key_map
            phi = -self.direction.z

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

                self.velocity = \
                    Vec3(
                        cos(radians(add_angle + phi)),
                        0,
                        sin(radians(add_angle + phi))
                    ) * self.move_speed
            else:
                self.velocity = Vec3(0, 0, 0)

    def set_player_position(self):
        dt = globalClock.getDt()
        self.position = self.position + self.velocity * dt

    def player_update(self, task):
        self.set_player_direction()
        self.set_player_velocity()
        self.set_player_position()
        self.player_draw()
        return task.cont
