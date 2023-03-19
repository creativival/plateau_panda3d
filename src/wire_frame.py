from panda3d.core import *

from . import draw_line_between_two_points


class WireFrame:
    def __init__(self):
        if self.settings['has_wire_frame']:
            center_x = self.area_center[0]
            center_y = self.area_center[1]

            # 建物
            settings = self.settings['plateau_settings']
            mesh3_list = settings['bldg_mesh3_list']
            for mesh3 in mesh3_list:
                file_name = (f'{settings["bldg_mesh1"]}{settings["bldg_mesh2"]}{mesh3}'
                             f'_bldg_{settings["bldg_crs_from"]}_op')
                table_name = f'plateau_{file_name}'

                self.db_cursor.execute(
                    f'SELECT building_id, name, height, positions, center_position FROM {table_name}'
                )

                for tuple_value in self.db_cursor.fetchall():
                    building_id, name, height, positions, center_position = tuple_value
                    base_position = Point3(*map(float, center_position.split('/')))
                    x = base_position[0]
                    y = base_position[1]

                    if ((center_x - self.building_tolerance < x < center_x + self.building_tolerance) and
                            (center_y - self.building_tolerance < y < center_y + self.building_tolerance)):
                        positions = [list(map(float, p.split('/'))) for p in positions.split('|')]
                        height = float(height)
                        building_node = self.map_node.find(building_id)

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
                            self.draw_3d_text(name, name_position, building_node, fg=(1, 0, 1, 1), bg=(1, 1, 1, 0.5))
                            self.draw_3d_text(name, name_position, building_node, heading=180, fg=(1, 0, 1, 1),
                                              bg=(1, 1, 1, 0.5))

            # 道路
            mesh3_list = settings['road_mesh3_list']
            for mesh3 in mesh3_list:
                file_name = (f'{settings["bldg_mesh1"]}{settings["bldg_mesh2"]}{mesh3}'
                             f'_tran_{settings["road_crs_from"]}_op')
                table_name = f'plateau_{file_name}'

                self.db_cursor.execute(
                    f'SELECT positions, center_position FROM {table_name}'
                )

                for tuple_value in self.db_cursor.fetchall():
                    positions, center_position = tuple_value
                    base_position = Point3(*map(float, center_position.split('/')))
                    x = base_position[0]
                    y = base_position[1]

                    if ((center_x - self.road_tolerance < x < center_x + self.road_tolerance) and
                            (center_y - self.road_tolerance < y < center_y + self.road_tolerance)):
                        positions = [list(map(float, p.split('/'))) for p in positions.split('|')]

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
