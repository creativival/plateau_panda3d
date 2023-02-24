# モブ
from math import sin, cos, atan2, radians, degrees, sqrt
from random import choice, uniform, randint, random
from panda3d.core import PandaNode, Point3, Vec3, VBase3

# from src.utils import *



class Mob:
    RADIUS_OF_COHERE = 60
    POWER_OF_COHERE = 1
    RADIUS_OF_SEPARATE = 2
    POWER_OF_SEPARATE = 5
    RADIUS_OF_ALIGN = 10
    POWER_OF_ALIGN = 0
    RADIUS_OF_PLAYER = 10
    ATTRACTION_OF_PLAYER = 0
    REPULSION_OF_PLAYER = 100
    MIN_SPEED = 2
    MAX_SPEED = 3

    def __init__(self, base, mob_dic):
        self.base = base
        self.name = mob_dic['name']
        self.scale = mob_dic['scale']
        self.speed = mob_dic['speed']
        self.heading = mob_dic['heading']
        self.position = Point3(
            randint(-50, 50),
            randint(-50, 50),
            1)
        self.direction = Vec3(0, 0, 0)
        self.velocity = Vec3(0, 0, 0)
        self.acceleration_to_cohere = Vec3(0, 0, 0)
        self.acceleration_with_player = Vec3(0, 0, 0)

        self.model_node = base.mobs_node.attachNewNode('model_node')
        self.model_node.setPos(self.position)
        self.model = base.loader.loadModel(mob_dic['model_name'])
        self.model.reparentTo(self.model_node)
        self.model.setScale(self.scale, self.scale, self.scale)
        self.model.setHpr(self.heading, 0, 0)

    def update(self, dt, center_of_gravity):
        # self.position += Point3(
        #     uniform(-1, 1),
        #     uniform(-1, 1),
        #     0)
        self.cohere(center_of_gravity)
        self.player_impact()
        self.set_position(dt)
        self.draw()

    def draw(self):
        heading = degrees(atan2(self.velocity.y, self.velocity.x)) + 90 + uniform(-10, 10)
        pitch = uniform(-5, 5)
        roll = uniform(-1, 1)
        # set mob
        self.model_node.setPos(self.position)
        self.model_node.setHpr(
            heading,
            pitch,
            roll,
        )

    # def update(self):
    #     if not self.render.multiplayer or self.render.multiplayer.network_state == 'server':
    #         self.cohere(self.render.mob_distance_list)
    #         self.separate(self.render.mob_distance_list)
    #         self.align(self.render.mob_distance_list)
    #         self.player_impact()
    #         self.total_acceleration = \
    #             self.acceleration_to_cohere + \
    #             self.acceleration_to_separate + \
    #             self.acceleration_to_align + \
    #             self.acceleration_with_player
    #         if random() < 0.005 and not self.jump_status:
    #             self.velocity.setZ(self.render.settings['mob_jump_speed'])
    #             self.jump_status = True
    #     else:
    #         self.total_acceleration = Vec3(0, 0, 0)
    #     self.set_position()
    #     self.draw()
    #
    # def get(self, var):
    #     try:
    #         return getattr(self, var)
    #     except AttributeError:
    #         return None
    #
    # def set(self, var, val):
    #     setattr(self, var, val)
    #
    def cohere(self, center_of_gravity):
        self.acceleration_to_cohere = \
            (center_of_gravity - self.position).normalized() * self.POWER_OF_COHERE

    # def separate(self, distance_list):
    #     near_mob_ids = [d[1] for d in distance_list[self.mob_id] if 0 < d[0] < self.RADIUS_OF_SEPARATE]
    #     if len(near_mob_ids) > 0:
    #         near_mob_positions = [self.render.mobs[mob_id].position for mob_id in near_mob_ids]
    #         center_of_near_mob_positions = center_of_vectors(near_mob_positions)
    #         self.acceleration_to_separate = \
    #             -(center_of_near_mob_positions - self.position).normalized() * self.POWER_OF_SEPARATE
    #     else:
    #         self.acceleration_to_separate = Vec3(0, 0, 0)
    #
    # def align(self, distance_list):
    #     near_mob_ids = [d[1] for d in distance_list[self.mob_id] if 0 < d[0] < self.RADIUS_OF_ALIGN]
    #     if len(near_mob_ids) > 0:
    #         near_mob_velocities = [self.render.mobs[mob_id].velocity for mob_id in near_mob_ids]
    #         self.acceleration_to_align = \
    #             add_vectors(near_mob_velocities).normalized() * self.POWER_OF_ALIGN
    #     else:
    #         self.acceleration_to_align = Vec3(0, 0, 0)
    #
    def player_impact(self):
        vector_to_player = self.base.player_position - self.position
        length_to_player = vector_to_player.length()
        # print(length_to_player)
        if length_to_player < self.RADIUS_OF_PLAYER * 3:
            self.acceleration_with_player = \
                vector_to_player.normalized() *self. RADIUS_OF_PLAYER * \
                (self.ATTRACTION_OF_PLAYER - self.REPULSION_OF_PLAYER) / length_to_player
        else:
            self.acceleration_with_player = Vec3(0, 0, 0)

    def set_position(self, dt):
        total_acceleration = self.acceleration_to_cohere + self.acceleration_with_player
        self.velocity = \
            (total_acceleration * dt + self.velocity).normalized() * self.speed
        self.position += self.velocity * dt
        # x1, y1, z1 = self.position
        # x2, y2, z2 = self.position + self.velocity * dt
        # if z2 > 1:
        #     self.velocity -= Vec3(0, 0, self.render.settings['gravity_force'] * dt)
        # if z2 <= 1:
        #     z2 = 1
        #     self.velocity.setZ(0)
        #     self.jump_status = False
        # if self.render.can_go_there(x1, y1, z1, x2, y2, z2):
        #     self.position = Point3(x2, y2, z2)
        #     for i in range(2):
        #         # reflection
        #         if self.position[i] <= self.render.ground_size[0] or self.render.ground_size[1] <= self.position[i]:
        #             self.velocity[i] *= -1
        #         # # through
        #         # if self.position[i] <= self.render.world_size[0]:
        #         #     self.position[i] = self.render.world_size[1]
        #         # if self.render.world_size[1] <= self.position[i]:
        #         #     self.position[i] = self.render.world_size[0]
        # else:
        #     self.velocity.x *= -1
        #     self.velocity.y *= -1
