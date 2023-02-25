from panda3d.core import *

from . import draw_line_between_two_points


class WireFrame:
    def __init__(self):
        center_x = self.area_center[0]
        center_y = self.area_center[1]

        # 建物
        for attributes in self.building_attributes_list:
            height = attributes['height']
            if height:
                bldg_id = attributes['building_id']
                name = attributes['name']
                positions = attributes['positions']
                base_position = Point3(*attributes['center_position'])
                building_node = self.map_node.find(f'building{bldg_id}')
                x = base_position[0]
                y = base_position[1]

                if ((center_x - self.building_tolerance < x < center_x + self.building_tolerance) and
                        (center_y - self.building_tolerance < y < center_y + self.building_tolerance)):
                    for i in range(len(positions)):
                        p1 = positions[i]
                        p2 = positions[(i + 1) % len(positions)]
                        offset_position1 = Point3(p1[0], p1[1], 0) - base_position
                        offset_position2 = Point3(p2[0], p2[1], 0) - base_position

                        # ワイヤーフレーム
                        if i % self.interval_drawing_pillar == 0:
                            draw_line_between_two_points(
                                offset_position1,
                                offset_position1 + Point3(0, 0, height),
                                (1, 0, 0),
                                building_node,
                                node_name='pillar_line_node'
                            )

                        draw_line_between_two_points(
                            offset_position1 + Point3(0, 0, height),
                            offset_position2 + Point3(0, 0, height),
                            (0, 1, 0),
                            building_node,
                            node_name='ceil_line_node',
                        )

                        draw_line_between_two_points(
                            offset_position1,
                            offset_position2,
                            (0, 0, 1),
                            building_node,
                            node_name='floor_line_node'
                        )

                    if name:
                        # print(name)
                        name_position = Point3(0, 0, height + 20)
                        draw_line_between_two_points(
                            Point3(0, 0, 0),
                            name_position,
                            (1, 0, 1),
                            building_node
                        )
                        self.draw_3d_text(name, name_position, building_node, fg=(1, 0, 1, 1), bg=(1,1,1,0.5))
                        self.draw_3d_text(name, name_position, building_node, heading=180, fg=(1, 0, 1, 1), bg=(1,1,1,0.5))

        # 道路
        for attributes in self.road_attributes_list:
            positions = attributes['positions']
            # print(positions)
            x = positions[0][0]
            y = positions[0][1]
            if ((center_x - self.road_tolerance < x < center_x + self.road_tolerance) and
                    (center_y - self.road_tolerance < y < center_y + self.road_tolerance)):
                for i in range(len(positions)):
                    start_position = Point3(*positions[i])
                    end_position = Point3(*positions[(i + 1) % len(positions)])

                    if start_position[0] == float('inf') or end_position[0] == float('inf'):
                        continue
                    draw_line_between_two_points(
                        start_position,
                        end_position,
                        (1, 1, 1),
                        self.map_node
                    )
