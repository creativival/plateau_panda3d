from math import degrees
from panda3d.core import *
from . import draw_line_between_two_points


class Building:
    def __init__(self):
        # 建物、道路を配置
        self.map_node = self.render.attachNewNode(PandaNode('map_node'))

        # 建物のベースノード
        self.all_buildings = []
        settings = self.settings
        mesh3_list = settings['bldg_mesh3_list']
        for mesh3 in mesh3_list:
            file_name = (f'{settings["bldg_mesh1"]}{settings["bldg_mesh2"]}{mesh3}'
                          f'_bldg_{settings["bldg_crs_from"]}_op')
            table_name = f'plateau_{file_name}'

            self.db_cursor.execute(
                f'SELECT building_id, height, center_position, min_distance, min_angle FROM {table_name}'
            )

            for tuple_value in self.db_cursor.fetchall():
                building_id, height, center_position, min_distance, min_angle = tuple_value
                base_position = Point3(*map(float, center_position.split('/')))

                building_node = self.map_node.attachNewNode(PandaNode(building_id))
                # print(building_node.getName())
                building_node.setPos(base_position)
                building_node.setTag('height', str(height))
                building_node.setTag('building_id', building_id)
                # Create a collision node for this object.
                collision_node = CollisionNode(building_id)
                # Attach a collision sphere solid to the collision node.
                # collision_node.addSolid(CollisionSphere(0, 0, 0, float(height)))
                collision_node.addSolid(CollisionBox(Point3(0, 0, height / 2), min_distance * 0.7, min_distance * 0.7, height / 2))
                # Attach the collision node to the object's model.
                collision_base_node = building_node.attachNewNode(PandaNode(f'collision_{building_id}'))
                collision_base_node.setH(degrees(min_angle) + 45)
                building_collision = collision_base_node.attachNewNode(collision_node)
                # Set the object's collision node to render as visible.
                # building_collision.show()

                self.all_buildings.append(building_node)
