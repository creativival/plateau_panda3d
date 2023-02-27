from math import *
from panda3d.core import *
from . import draw_triangles


class Ground:
    def __init__(self):
        # 義麺
        ground_size = 10000
        vertices=[Vec3(ground_size, ground_size, 0), Vec3(-ground_size, ground_size, 0),
                  Vec3(-ground_size, -ground_size, 0), Vec3(ground_size, -ground_size, 0)]
        # colors=[Vec4(1, 0, 0, 1), Vec4(0, 1, 0, 1), Vec4(0, 0, 1, 1), Vec4(1, 0, 1, 1)]
        colors=[Vec4(0, 1, 0, 0.1), Vec4(0, 1, 0, 0.1), Vec4(0, 1, 0, 0.1), Vec4(0, 1, 0, 0.1)]
        ground_center_position = self.area_center - Point3(0, 0, 0.1)
        draw_triangles(vertices, colors, self.render, position=ground_center_position, node_name='ground_node')
