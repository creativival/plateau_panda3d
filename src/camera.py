from math import sin, cos, radians, floor
from time import time
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import *
from panda3d.core import *


class Camera:
    # 初期化メソッド
    def __init__(self):
        # マウス操作を禁止
        self.disableMouse()
        # カメラの設定
        self.camera_radius = 400
        self.camera_theta = -30
        self.camera_phi = 0
        self.camera_base_node = self.render.attachNewNode(PandaNode('camera_base_node'))
        self.camera_base_node.setPos(self.area_center)
        self.camera_base_node.setH(-90)
        self.camera_move_node = self.camera_base_node.attachNewNode(PandaNode('camera_move_node'))
        self.camera_node = self.camera_move_node.attachNewNode(PandaNode('camera_move_node'))
        self.camera.reparentTo(self.camera_node)
        self.camera.setHpr(90, 0, 0)
        self.camera.setPos(self.camera_radius, 0, 0)
        self.set_camera_pos()
        self.camera_position = Vec2(0, 0)
        self.camera_velocity = Vec2(0, 0)
        self.camera_move_speed = 100
        self.active_cam = 0

        # キー操作でカメラを動かす
        self.accept('arrow_right', self.right_key)
        self.accept('arrow_left', self.left_key)
        self.accept('arrow_up', self.up_key)
        self.accept('arrow_down', self.down_key)
        self.accept('arrow_right-repeat', self.right_key)
        self.accept('arrow_left-repeat', self.left_key)
        self.accept('arrow_up-repeat', self.up_key)
        self.accept('arrow_down-repeat', self.down_key)
        self.accept('wheel_up', self.wheel_up)
        self.accept('wheel_down', self.wheel_down)

        # key_map
        self.key_map = {
            'w': False,
            'a': False,
            's': False,
            'd': False,
            'space': False,
            'mouse1': False,
            'mouse2': False,
            'mouse3': False,
        }

        self.accept('w', self.update_key_map, ['w', True])
        self.accept('w-up', self.update_key_map, ['w', False])
        self.accept('a', self.update_key_map, ['a', True])
        self.accept('a-up', self.update_key_map, ['a', False])
        self.accept('s', self.update_key_map, ['s', True])
        self.accept('s-up', self.update_key_map, ['s', False])
        self.accept('d', self.update_key_map, ['d', True])
        self.accept('d-up', self.update_key_map, ['d', False])
        self.accept('space', self.update_key_map, ['space', True])
        self.accept('space-up', self.update_key_map, ['space', False])
        self.accept('mouse1', self.update_key_map, ['mouse1', True])
        self.accept('mouse1-up', self.update_key_map, ['mouse1', False])
        self.accept('mouse2', self.update_key_map, ['mouse2', True])
        self.accept('mouse2-up', self.update_key_map, ['mouse2', False])
        self.accept('mouse3', self.update_key_map, ['mouse3', True])
        self.accept('mouse3-up', self.update_key_map, ['mouse3', False])

        # カメラの切り替え
        self.accept('t', self.toggle_cam)

        # move the camera
        self.taskMgr.add(self.update, "update")

    def update_key_map(self, key_name, key_state):
        self.key_map[key_name] = key_state

    def draw(self):
        self.camera_move_node.setPos(*self.camera_position, 0)

    def set_velocity(self):
        key_map = self.key_map

        if key_map['w'] or key_map['a'] or key_map['s'] or key_map['d']:
            if key_map['w'] and key_map['a']:
                angle = 215
            elif key_map['a'] and key_map['s']:
                angle = 315
            elif key_map['s'] and key_map['d']:
                angle = 45
            elif key_map['d'] and key_map['w']:
                angle = 135
            elif key_map['w']:
                angle = 180
            elif key_map['a']:
                angle = 270
            elif key_map['s']:
                angle = 0
            elif key_map['d']:
                angle = 90
            self.camera_velocity = \
                Vec2(
                    cos(radians(angle + self.camera_phi)),
                    sin(radians(angle + self.camera_phi))
                ) * self.camera_move_speed
        else:
            self.camera_velocity = Vec2(0, 0)

    def set_position(self):
        dt = globalClock.getDt()
        self.camera_position = self.camera_position + self.camera_velocity * dt

    def update(self, task):
        if self.active_cam == 0:
            self.set_velocity()
            self.set_position()
            self.draw()
        return task.cont

    def set_camera_pos(self):
        r = self.camera_radius
        print('camera:', r, self.camera_theta, self.camera_phi)
        self.camera.setPos(r, 0, 0)
        self.camera_node.setHpr(self.camera_phi, 0, self.camera_theta)

    def right_key(self):
        # カメラを円周上で+1度動かす
        self.camera_phi += 1
        self.set_camera_pos()

    def left_key(self):
        # カメラを円周上で-1度動かす
        self.camera_phi -= 1
        self.set_camera_pos()

    def up_key(self):
        # カメラの仰角で-1度動かす
        self.camera_theta -= 1
        self.set_camera_pos()

    def down_key(self):
        # カメラの仰角で+1度動かす
        self.camera_theta += 1
        self.set_camera_pos()

    def wheel_up(self):
        # カメラを近づける
        self.camera_radius *= 0.8
        self.set_camera_pos()

        if self.camera_radius <= self.max_camera_radius_to_render_surface:
            # ビルを表示
            building_nodes = self.map_node.findAllMatches('**/building*')
            for building_node in building_nodes:
                for child in building_node.getChildren():
                    height = child.getNetTag('height')
                    if height and float(height) <= 10:
                        name = child.getName()
                        if name not in ['pillar_line_node', 'ceil_line_node']:
                            if child.isHidden():
                                child.show()
            # 道路を表示
            road_nodes = self.map_node.findAllMatches('**/road*')
            for road_node in road_nodes:
                if road_node.isHidden():
                    road_node.show()

    def wheel_down(self):
        # カメラを遠ざける
        self.camera_radius *= 1.25
        self.set_camera_pos()

        if self.max_camera_radius_to_render_surface < self.camera_radius:
            # ビルを非表示
            building_nodes = self.map_node.findAllMatches('**/building*')
            for building_node in building_nodes:
                for child in building_node.getChildren():
                    height = child.getNetTag('height')
                    if height and float(height) <= 10:
                        name = child.getName()
                        if name not in ['pillar_line_node', 'ceil_line_node']:
                            if not child.isHidden():
                                child.hide()
            # 道路を非表示
            road_nodes = self.map_node.findAllMatches('**/road*')
            for road_node in road_nodes:
                if not road_node.isHidden():
                    road_node.hide()
