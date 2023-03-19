from math import sin, cos, radians, floor
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import *
from . import Character


class Player(Character):
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
    perspective_lens.setNearFar(0.18, 4000)  # 遠方は表示しない（デフォルトは100000）

    # orthographic_lens = OrthographicLens()
    # orthographic_lens.setFilmSize(*mirror_cam_film_size)

    def __init__(self, base, is_guest=False):
        # print('is_guest:', is_guest)
        self.base = base
        self.is_guest = is_guest
        self.client_id = 0
        # self.has_moving_hands = False
        Character.__init__(self)

        self.position = Vec3(0, 0, 1)
        self.direction = Vec3(0, 0, 0)
        self.velocity = Vec3(0, 0, 0)
        self.hand_length = 0
        self.left_angle = 0
        self.right_angle = 0
        self.guest_face_num = 1
        self.move_speed = 10
        self.is_walking = False
        self.walking_count = 0
        # jump and fly
        self.gravity = 9.8
        self.jump_speed = 10
        self.fly_height = 0
        self.jump_status = False
        self.double_jump_status = False

        # プレイヤー
        self.player_node = self.base.players_node.attachNewNode(PandaNode('player_node'))
        self.player_node.setPos(self.position)
        self.player_node.setHpr(self.direction)
        self.character_node.reparentTo(self.player_node)
        self.character_node.setPos(0, 0, 1)
        self.character_node.setHpr(180, 0, 0)

        if not is_guest:
            # add camera
            self.has_player_camera = True
            # tps cam
            self.tps_cam = self.base.makeCamera(self.base.win)
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
            self.fps_cam = self.base.makeCamera(self.base.win)
            self.fps_cam.node().setLens(self.perspective_lens)
            self.fps_cam.reparentTo(self.character_node)
            self.fps_cam.setPos(
                Vec3(0, -self.player_head_height / 2, self.player_head_height / 2)
            )
            self.fps_cam.setH(180)
            # mirror cam
            self.mirror_cam = self.base.makeCamera(self.base.win)
            self.mirror_cam.node().setLens(self.perspective_lens)
            self.mirror_cam.reparentTo(self.character_node)
            self.mirror_cam.setPos(
                Vec3(0, -self.mirror_cam_radius, 0)
            )
            # camera change settings
            self.cameras = [self.base.cam, self.tps_cam, self.fps_cam, self.mirror_cam]
            self.cameras[1].node().getDisplayRegion(0).setActive(0)
            self.cameras[2].node().getDisplayRegion(0).setActive(0)
            self.cameras[3].node().getDisplayRegion(0).setActive(0)

            # カメラの切り替え
            self.base.accept('f5', self.toggle_cam)

        # move the player
        self.base.taskMgr.add(self.player_update, 'player_update')
        self.base.taskMgr.doMethodLater(0.5, self.set_player_motion, 'set_player_motion')
        # self.base.taskMgr.add(self.change_guest_face, 'change_guest_face')

    def change_guest_face(self, task):
        if self.is_changed_guest_face_num and self.is_guest:
            self.cat_tex = self.base.loader.loadTexture(f'models/maps/cat/cat{self.character_face_num}.png')
            self.character_model.setTexture(self.cat_tex, 1)

        return task.cont

    def set_player_motion(self, task):
        if not self.is_guest:
            self.hand_length = 0.8 * self.character_hand_length

            if self.character_face_num in [2, 8, 9]:
                self.left_angle = 45
                self.right_angle = 45
            else:
                self.left_angle = 0
                self.right_angle = 0

            if self.is_walking:
                self.walking_count += 1
                if self.walking_count % 2:
                    self.left_angle -= 20
                    self.right_angle += 20
                else:
                    self.left_angle += 20
                    self.right_angle -= 20
        # else:
        #     print('guest hand:', self.hand_length, self.left_angle, self.right_angle)

        self.character_left_hand_model.setSz(self.hand_length)
        self.character_right_hand_model.setSz(self.hand_length)
        self.character_right_hand_model_node.setP(self.left_angle)
        self.character_left_hand_model_node.setP(self.right_angle)
        return task.again

    def player_draw(self):
        if not self.is_guest:
            x, y, z = [floor(v) for v in self.position]
            self.base.bottom_left_text.setText(f'player position: {x}, {y}, {z}')
        self.player_node.setPos(self.position)
        self.player_node.setHpr(self.direction)

    def set_player_velocity(self):
        if not self.is_guest:
            key_map = self.base.key_map
            walk_sound = self.base.walk_sound

            # jump
            if key_map['space'] and not self.double_jump_status:
                self.base.jump_sound.play()

                self.velocity.setZ(self.jump_speed)
                if not self.jump_status:
                    self.jump_status = True
                    self.fly_height = 0
                else:
                    self.double_jump_status = True

            if key_map['w'] or key_map['a'] or key_map['s'] or key_map['d']:
                self.is_walking = True
                if walk_sound.status() is not walk_sound.PLAYING:
                    walk_sound.play()
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

                self.velocity.setX(
                    cos(radians(add_angle + self.direction.x)) * self.move_speed
                )
                self.velocity.setY(
                    sin(radians(add_angle + self.direction.x)) * self.move_speed
                )
                # print(self.velocity)
            else:
                self.is_walking = False
                if self.position.z == 0:
                    if walk_sound.status() is walk_sound.PLAYING:
                        walk_sound.stop()
                    # 重力加速度を残すため、Z成分は0にしない
                    self.velocity.setX(0)
                    self.velocity.setY(0)

    def set_player_direction(self):
        if (not self.is_guest and
                not self.base.is_paused_player and
                self.menu_node.isStashed()):
            if self.base.mouseWatcherNode.hasMouse():
                mouse_pos = self.base.mouseWatcherNode.getMouse()
                x = mouse_pos.x
                y = mouse_pos.y
                # print(x, y)
                heading = -x * self.max_heading_angle
                pitch = -y * self.max_pitch_angle
                self.direction = VBase3(heading, pitch, 0)

    def set_player_position(self):
        if not self.is_guest:
            dt = globalClock.getDt()

            if self.position.z > 0 or self.velocity.z == self.jump_speed:
                self.velocity.z -= self.gravity * dt
            else:
                self.position.setZ(0)
                self.velocity.setZ(0)
                self.jump_status = False
                self.double_jump_status = False

            self.position += self.velocity * dt

    def player_update(self, task):
        if self.base.active_cam != 0:
            self.set_player_velocity()
            self.set_player_direction()
            self.set_player_position()
            self.player_draw()
        return task.cont

    def toggle_cam(self):
        # print('toggle_cam')
        if self.has_player_camera:
            self.cameras[self.base.active_cam].node().getDisplayRegion(0).setActive(0)
            self.base.active_cam = (self.base.active_cam + 1) % len(self.cameras)
            self.cameras[self.base.active_cam].node().getDisplayRegion(0).setActive(1)
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
