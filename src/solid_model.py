from panda3d.core import *

from . import draw_triangles


class SolidModel:
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

                    offset_positions = [Point3(x, y, 0) - base_position for x, y, _ in positions]
                    offset_ceil_positions = [Point3(x, y, height) - base_position for x, y, _ in positions]

                    for i in range(len(positions)):
                        next_index = (i + 1) % len(positions)
                        # offset_x1, offset_y1, _ = offset_positions[i]
                        # offset_x2, offset_y2, _ = offset_positions[next_index]

                        # サーフェース（側面）
                        if height > self.min_surface_height:
                            vertices = [Vec3(*offset_positions[i]), Vec3(*offset_ceil_positions[i]),
                                        Vec3(*offset_ceil_positions[next_index]), Vec3(*offset_positions[next_index])]
                            # colors=[Vec4(0.2, 0.2, 0.2, 1), Vec4(0.4, 0.4, 0.4, 1), Vec4(0.6, 0.6, 0.6, 1),
                            #         Vec4(0.8, 0.8, 0.8, 1)]
                            colors = [Vec4(0.8, 0.8, 0.8, 0.3), Vec4(0.8, 0.8, 0.8, 0.3), Vec4(0.8, 0.8, 0.8, 0.3),
                                      Vec4(0.8, 0.8, 0.8, 0.3)]
                            draw_triangles(vertices, colors, building_node, node_name='side_node')

                        # サーフェース（天井）
                        diff_color = 0.8 / len(positions)
                        vertices = offset_ceil_positions
                        # colors=[Vec4(0.2 + diff_color * i, 0.2 + diff_color * i, 0.2 + diff_color * i, 1) for i in range(len(positions))]
                        colors = [Vec4(0.8, 0.8, 0.8, 0.3) for _ in range(len(positions))]
                        draw_triangles(vertices, colors, building_node, direction='reverse', node_name='ceil_node')

        # 道路
        for attributes in self.road_attributes_list:
            positions = attributes['positions']
            x = positions[0][0]
            y = positions[0][1]
            if ((center_x - self.road_tolerance < x < center_x + self.road_tolerance) and
                    (center_y - self.road_tolerance < y < center_y + self.road_tolerance)):
                # print(x, y)
                vertices = [Point3(p[0], p[1], 0) for p in positions]
                print(vertices[:3])
                # colors=[Vec4(0.2 + diff_color * i, 0.2 + diff_color * i, 0.2 + diff_color * i, 1) for i in range(len(positions))]
                colors = [Vec4(0.2, 0.2, 0.2, 0.3) for _ in range(len(positions))]
                draw_triangles(vertices, colors, self.map_node, node_name='road_node')
