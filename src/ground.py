from math import *
from panda3d.core import *
from . import draw_triangles, draw_line_between_two_points


class Ground:
    def __init__(self):
        # 義麺
        ground_size = 10000
        vertices = [Vec3(ground_size, ground_size, 0), Vec3(-ground_size, ground_size, 0),
                    Vec3(-ground_size, -ground_size, 0), Vec3(ground_size, -ground_size, 0)]
        # colors=[Vec4(1, 0, 0, 1), Vec4(0, 1, 0, 1), Vec4(0, 0, 1, 1), Vec4(1, 0, 1, 1)]
        colors = [Vec4(0, 1, 0, 0.1), Vec4(0, 1, 0, 0.1), Vec4(0, 1, 0, 0.1), Vec4(0, 1, 0, 0.1)]
        ground_center_position = self.area_center - Point3(0, 0, 0.1)
        draw_triangles(vertices, colors, self.render, position=ground_center_position,
                       node_name='ground_node')

        self.ground_node = self.render.find('ground_node')

        line_color = (1, 0, 0, 0.3)
        for i in range(1001):
            p1 = Point3(i * 10 - 5000, -5000, 0.01)
            p2 = Point3(i * 10 - 5000, 5000, 0.01)
            p3 = Point3(-5000, i * 10 - 5000, 0.01)
            p4 = Point3(5000, i * 10 - 5000, 0.01)

            draw_line_between_two_points(p1, p2, line_color=line_color, parent=self.ground_node)
            draw_line_between_two_points(p3, p4, line_color=line_color, parent=self.ground_node)



