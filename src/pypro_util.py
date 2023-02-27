from pyproj import Transformer
import xml.etree.ElementTree as ET
import os
import json
import copy
from math import *
from panda3d.core import *


def change_to_cartesian(lat, lng, crs_from, crs_to):
    # 緯度経度を変換
    # 基準点からのメートル
    transformer = Transformer.from_crs(crs_from, crs_to)
    x, y = transformer.transform(lat, lng)
    # 北がX軸、東がY軸のため、座標変換
    return y, x


def get_road_positions(geo_text, crs_from, crs_to):
    geo_array = geo_text.split()
    geo_locations = [geo_array[i * 3:i * 3 + 3] for i in range(len(geo_array) // 3)]

    cartesian_locations = []
    for geo_location in geo_locations:
        _geo_location = [float(value) for value in geo_location]
        # print(_geo_location)
        x, y = change_to_cartesian(_geo_location[0], _geo_location[1], crs_from, crs_to)
        cartesian_location = (x, y, 0)
        cartesian_locations.append(cartesian_location)

    return tuple(cartesian_locations)


def get_building_positions(geo_text, crs_from, crs_to):
    geo_array = geo_text.split()
    geo_locations = [geo_array[i * 3:i * 3 + 3] for i in range(len(geo_array) // 3)]

    cartesian_locations = []
    for geo_location in geo_locations:
        _geo_location = [float(value) for value in geo_location]
        # print(_geo_location)
        lat, lng = change_to_cartesian(_geo_location[0], _geo_location[1], crs_from, crs_to)
        cartesian_location = (lat, lng, _geo_location[2])
        cartesian_locations.append(cartesian_location)

    return tuple(cartesian_locations)


if __name__ == '__main__':
    pass
    # location = (35.89501065742873, 139.63187403357193)
    # print(change_to_cartesian(*location))
