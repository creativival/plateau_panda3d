import sys
from panda3d.core import *
from . import draw_line_between_two_points


class Building:
    def __init__(self):
        # 建物、道路を配置
        self.map_node = self.render.attachNewNode(PandaNode('map_node'))

        # 建物のベースノードを作っておく
        settings = self.settings
        mesh3_list = settings['bldg_mesh3_list']
        for mesh3 in mesh3_list:
            file_name = (f'{settings["bldg_mesh1"]}{settings["bldg_mesh2"]}{mesh3}'
                          f'_bldg_{settings["bldg_crs_from"]}_op')
            table_name = f'plateau_{file_name}'

            self.db_cursor.execute(
                f'SELECT building_id, height, center_position FROM {table_name}'
            )

            for tuple_value in self.db_cursor.fetchall():
                building_id, height, center_position = tuple_value
                base_position = Point3(*map(float, center_position.split('/')))

                building_node = self.map_node.attachNewNode(PandaNode(building_id))
                building_node.setPos(base_position)
                building_node.setTag('height', str(height))
