from math import *
from panda3d.core import *
from . import draw_line_between_two_points


class CelestialSphere:
    def __init__(self, sky_texture):
        self.sky_texture = self.loader.loadTexture(sky_texture)
        # 座標軸
        self.celestial_sphere_node = self.render.attachNewNode(PandaNode('axis_node'))
        self.celestial_sphere_node.setPos(self.area_center)

        draw_line_between_two_points(
            Point3(0, 0, 0),
            Point3(10000, 0, 0),
            (1, 0, 0),
            self.celestial_sphere_node,
            thickness=3
        )

        draw_line_between_two_points(
            Point3(0, 0, 0),
            Point3(0, 10000, 0),
            (0, 1, 0),
            self.celestial_sphere_node,
            thickness=3
        )

        draw_line_between_two_points(
            Point3(0, 0, 0),
            Point3(0, 0, 10000),
            (0, 0, 1),
            self.celestial_sphere_node,
            thickness=3
        )

        self.celestial_sphere = self.loader.loadModel('models/sphere_uv_reverse64')
        self.celestial_sphere.setScale(self.celestial_radius, self.celestial_radius, self.celestial_radius)
        self.celestial_sphere.setTexture(self.sky_texture, 1)
        self.celestial_sphere.reparentTo(self.celestial_sphere_node)
