from math import *
from panda3d.core import *
from . import draw_line_between_two_points


class Axis:
    def __init__(self):
        # 座標軸
        self.axis_node = self.render.attachNewNode(PandaNode('axis_node'))
        self.axis_node.setPos(self.area_center)

        draw_line_between_two_points(
            Point3(0, 0, 0),
            Point3(10000, 0, 0),
            (1, 0, 0),
            self.axis_node,
            thickness=3
        )

        draw_line_between_two_points(
            Point3(0, 0, 0),
            Point3(0, 10000, 0),
            (0, 1, 0),
            self.axis_node,
            thickness=3
        )

        draw_line_between_two_points(
            Point3(0, 0, 0),
            Point3(0, 0, 10000),
            (0, 0, 1),
            self.axis_node,
            thickness=3
        )
