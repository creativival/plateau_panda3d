from panda3d.core import *
from . import (
    get_building_attributes_list, get_min_and_max_position, get_road_attributes_list
)


class ReadBuilding:
    def __init__(self, plateau_settings):
        self.building_attributes_list = get_building_attributes_list(plateau_settings)
        self.road_attributes_list = get_road_attributes_list(plateau_settings)
        min_position, max_position = get_min_and_max_position(self.building_attributes_list)
        area_center = (min_position + max_position) / 2
        self.area_center = Point3(*area_center)
        print(area_center)
