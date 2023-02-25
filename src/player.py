from math import sin, cos, radians, floor
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import *


class Player:
    max_heading_angle = 200
    max_pitch_angle = 75
    tps_cam_fov = 90
    tps_cam_back_radius = 7
    tps_cam_forward_radius = 7
    tps_cam_height = 5
    fps_cam_height = 1.5
    fps_cam_fov = 100
    player_head_height = 0.5
    mirror_cam_radius = 5
    mirror_cam_film_size = (4, 3)

    perspective_lens = PerspectiveLens()
    perspective_lens.setFov(fps_cam_fov)
    perspective_lens.setNearFar(0.18, 500)  # 遠方は表示しない（デフォルトは100000）

    # orthographic_lens = OrthographicLens()
    # orthographic_lens.setFilmSize(*mirror_cam_film_size)

    def __init__(self):
        self.player_position = Vec3(0, 0, 1)
        self.player_direction = Vec3(0, 0, 0)
        self.player_velocity = Vec3(0, 0, 0)
        self.player_move_speed = 10
        # jump and fly
        self.gravity = 9.8
        self.player_jump_speed = 10
        self.fly_height = 0
        self.jump_status = False
        self.double_jump_status = False

        # プレイヤー
        self.player_base_node = self.render.attachNewNode(PandaNode('player_base_node'))
        self.player_base_node.setPos(self.area_center)
        self.player_node = self.player_base_node.attachNewNode(PandaNode('player_node'))
        self.player_node.setPos(self.player_position)
        self.player_node.setHpr(self.player_direction)

        self.cat_tex = self.loader.loadTexture("models/maps/cat.png")
        self.cat_ear_tex = self.loader.loadTexture("models/maps/cat_ear.png")

        self.character_node = self.player_node.attachNewNode(PandaNode('character_node'))
        self.character_node.setPos(0, 0, 1)
        self.character_node.setHpr(180, 0, 0)

        self.character = self.loader.loadModel("models/egg_shape32")
        self.character.reparentTo(self.character_node)
        self.character.setTexture(self.cat_tex, 1)
        self.character.setScale(1.41, 1.2, 1)
        self.character.setPos(0, 0, 0)
        self.character.setHpr(0, 0, 0)
        self.character.setColor(1, 1, 1)

        self.character_left_hand = self.loader.loadModel("models/egg_shape32")
        self.character_left_hand.reparentTo(self.character_node)
        self.character_left_hand.setTexture(self.cat_ear_tex, 1)
        self.character_left_hand.setScale(1, 0.3, 1)
        self.character_left_hand.setPos(0.3, 0, 0.3)
        self.character_left_hand.setHpr(0, 0, 45)
        self.character_left_hand.setColor(1, 1, 1)

        self.character_right_hand = self.loader.loadModel("models/egg_shape32")
        self.character_right_hand.reparentTo(self.character_node)
        self.character_right_hand.setTexture(self.cat_ear_tex, 1)
        self.character_right_hand.setScale(1, 0.3, 1)
        self.character_right_hand.setPos(-0.3, 0, 0.3)
        self.character_right_hand.setHpr(0, 0, -45)
        self.character_right_hand.setColor(1, 1, 1)

        # add camera
        # tps cam
        self.tps_cam = self.makeCamera(self.win)
        self.tps_cam.node().setLens(self.perspective_lens)
        self.tps_cam.reparentTo(self.player_node)
        # self.tps_cam.getLens().setFov(tps_cam_fov)
        self.tps_cam.setPos(
            Vec3(0, -self.tps_cam_back_radius, self.tps_cam_height)
        )
        self.tps_cam.lookAt(
            Vec3(0, self.tps_cam_forward_radius, 0)
        )
        # fps cam
        self.fps_cam_height = self.player_head_height
        self.fps_cam = self.makeCamera(self.win)
        self.fps_cam.node().setLens(self.perspective_lens)
        self.fps_cam.reparentTo(self.character_node)
        self.fps_cam.setPos(
            Vec3(0, -self.player_head_height / 2, self.player_head_height / 2)
        )
        self.fps_cam.setH(180)
        # mirror cam
        self.mirror_cam = self.makeCamera(self.win)
        self.mirror_cam.node().setLens(self.perspective_lens)
        self.mirror_cam.reparentTo(self.character_node)
        self.mirror_cam.setPos(
            Vec3(0, -self.mirror_cam_radius, 0)
        )
        # camera change settings
        self.cameras = [self.cam, self.tps_cam, self.fps_cam, self.mirror_cam]
        self.cameras[1].node().getDisplayRegion(0).setActive(0)
        self.cameras[2].node().getDisplayRegion(0).setActive(0)
        self.cameras[3].node().getDisplayRegion(0).setActive(0)

        # カメラの切り替え
        self.accept('t', self.toggle_cam)

        # move the player
        self.taskMgr.add(self.player_update, "player_update")

    def player_draw(self):
        self.player_node.setPos(self.player_position)
        self.player_node.setHpr(self.player_direction)

    def set_player_velocity(self):
        key_map = self.key_map

        # jump
        if key_map['space'] and not self.double_jump_status:
            self.player_velocity.setZ(self.player_jump_speed)
            if not self.jump_status:
                self.jump_status = True
                self.fly_height = 0
            else:
                self.double_jump_status = True

        if key_map['w'] or key_map['a'] or key_map['s'] or key_map['d']:
            # move
            add_angle = 0
            if key_map['w'] and key_map['a']:
                add_angle += 135
            elif key_map['a'] and key_map['s']:
                add_angle += 225
            elif key_map['s'] and key_map['d']:
                add_angle += 315
            elif key_map['d'] and key_map['w']:
                add_angle += 45
            elif key_map['w']:
                add_angle += 90
            elif key_map['a']:
                add_angle += 180
            elif key_map['s']:
                add_angle += 270
            elif key_map['d']:
                add_angle += 0

            self.player_velocity.setX(
                cos(radians(add_angle + self.player_direction.x)) * self.player_move_speed
            )
            self.player_velocity.setY(
                sin(radians(add_angle + self.player_direction.x)) * self.player_move_speed
            )
            # print(self.player_velocity)
        else:
            if self.player_position.z == 0:
                # 重力加速度を残すため、Z成分は0にしない
                self.player_velocity.setX(0)
                self.player_velocity.setY(0)

    def set_player_direction(self):
        if self.mouseWatcherNode.hasMouse():
            mouse_pos = self.mouseWatcherNode.getMouse()
            x = mouse_pos.x
            y = mouse_pos.y
            # print(x, y)
            heading = -x * self.max_heading_angle
            pitch = -y * self.max_pitch_angle
            self.player_direction = VBase3(heading, pitch, 0)

    def set_player_position(self):
        dt = globalClock.getDt()

        if self.player_position.z >= 0:
            self.player_velocity.z -= self.gravity * dt
        else:
            self.player_position.setZ(0)
            self.player_velocity.setZ(0)
            self.jump_status = False
            self.double_jump_status = False

        print(self.player_velocity)
        self.player_position += self.player_velocity * dt

    def player_update(self, task):
        if self.active_cam != 0:
            self.set_player_velocity()
            self.set_player_direction()
            self.set_player_position()
            self.player_draw()
        return task.cont

    def toggle_cam(self):
        self.cameras[self.active_cam].node().getDisplayRegion(0).setActive(0)
        self.active_cam = (self.active_cam + 1) % len(self.cameras)
        self.cameras[self.active_cam].node().getDisplayRegion(0).setActive(1)
        # cam_names = ['Default cam', 'Player cam', 'Mirror cam', 'Guest cam']
        # self.console_window.setText(self.i18n.t(cam_names[self.activeCam]))
        # self.console_window.start_time = time()

    # def get_floor_level(self, x1, y1, z1, x2, y2, z2):
    #     x1, y1, z1, x2, y2, z2 = floor(x1), floor(y1), floor(z1), floor(x2), floor(y2), floor(z2)
    #     x, y = x2, y2
    #     if y1 < y2:
    #         y += 1
    #     if x1 < x2:
    #         x += 1
    #     cursor = self.db.cursor()
    #     for i in reversed(range(z2 + 2)):
    #         args = (x, y, i)
    #         # print(args)
    #         cursor.execute('select count(*) from current where x=? and y=? and z=?', args)
    #         count = cursor.fetchone()[0]
    #         if count:
    #             # print(y1, y2, y, i)
    #             cursor.close()
    #             return i + 1
    #     else:
    #         # print(y1, y2, y, 0)
    #         cursor.close()
    #         return 0
