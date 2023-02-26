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


def get_road_attributes_list(settings, db, db_cursor):
    mesh3_list = settings['road_mesh3_list']
    road_crs_from = settings['road_crs_from']
    if len(road_crs_from.split('_')) > 1:
        _road_crs_from = road_crs_from.split('_')[0]
    else:
        _road_crs_from = road_crs_from
    all_road_attributes_list = []
    count = 0
    count2 = 0

    for mesh3 in mesh3_list:
        road_attributes_list = []
        file_name = (f'{settings["bldg_mesh1"]}{settings["bldg_mesh2"]}{mesh3}'
                     f'_tran_{settings["road_crs_from"]}_op')
        output_file_path = f'output/{file_name}.txt'

        if os.path.exists(output_file_path):
            print('file exists:', output_file_path)

            decoder = json.JSONDecoder()
            with open(output_file_path, 'r') as f:
                line = f.readline()
                while line:
                    attributes = decoder.raw_decode(line)[0]
                    attributes['positions'] = [list(map(float, p.split('/'))) for p in
                                               attributes['positions'].split('|')]
                    road_attributes_list.append(attributes)
                    line = f.readline()

            all_road_attributes_list += road_attributes_list
        else:
            print('not fount:', output_file_path)
            count = 0
            file_path = f'data/{file_name}.gml'

            if not os.path.exists(file_path):
                print('not found:', file_path)
                return
            else:
                print('file exists:', file_path)

            # XMLファイルを解析
            tree = ET.parse(file_path)

            # XMLを取得
            root = tree.getroot()

            # 接頭辞の辞書
            ns = {
                'core': 'http://www.opengis.net/citygml/2.0',
                'bldg': 'http://www.opengis.net/citygml/building/2.0',
                'gml': 'http://www.opengis.net/gml',
                'gen': 'http://www.opengis.net/citygml/generics/2.0',
                'tran': 'http://www.opengis.net/citygml/transportation/2.0'
            }

            for road in root.findall('core:cityObjectMember/tran:Road', ns):
                # print(road.tag, road.attrib)
                # print(road)
                road_lod1 = road.find('tran:lod1MultiSurface', ns)

                if road_lod1:
                    geo_text = road_lod1[0][0][0][0][0][0].text
                else:
                    geo_text = road[0][0][0][0][0][0].text

                positions = get_road_positions(geo_text, _road_crs_from, settings['crs_to'])
                if positions:
                    count += 1
                    print('count:', count)
                    road_attributes = {
                        'id': count,
                        'positions': positions
                    }
                    road_attributes_list.append(road_attributes)

                    # データベース保存
                    positions_text = \
                        '|'.join(['/'.join([str(v) for v in l]) for l in road_attributes['positions']])
                    inserts = (
                        settings['bldg_mesh1'],
                        settings['bldg_mesh2'],
                        mesh3,
                        positions_text
                    )

                    db_cursor.execute(
                        'INSERT INTO buildings(mesh1, mesh2, mesh3, positions) '
                        'values(?, ?, ?, ?)',
                        inserts)

            # with open(output_file_path, 'w') as f:
            #     attributes_list = copy.deepcopy(road_attributes_list)
            #     for attributes in attributes_list:
            #         name = attributes['name']
            #         bldg_id = attributes['bldg_id']
            #         height = attributes['height']
            #         positions = '|'.join(['/'.join([str(v) for v in l]) for l in attributes['positions']])
            #         attributes['positions'] = \
            #             '|'.join(['/'.join([str(v) for v in l]) for l in attributes['positions']])
            #
            #     l = [json.dumps(attributes) for attributes in attributes_list]
            #     f.write('\n'.join(l))

            all_road_attributes_list += road_attributes_list

    db.commit()

    return all_road_attributes_list


def table_is_exist(db_cursor, table_name):
    print(f"""
        SELECT COUNT(*) FROM sqlite_master 
        WHERE TYPE='table' AND name='{table_name}'
        """)
    db_cursor.execute(f"""
        SELECT COUNT(*) FROM sqlite_master 
        WHERE TYPE='table' AND name='{table_name}'
        """)
    if db_cursor.fetchone()[0] == 0:
        return False
    return True


def get_building_attributes_list(settings, db, db_cursor):
    mesh3_list = settings['bldg_mesh3_list']
    bldg_crs_from = settings['bldg_crs_from']
    if len(bldg_crs_from.split('_')) > 1:
        _bldg_crs_from = bldg_crs_from.split('_')[0]
    else:
        _bldg_crs_from = bldg_crs_from
    all_building_attributes_list = []

    for mesh3 in mesh3_list:
        table_name = (f'plateau_{settings["bldg_mesh1"]}{settings["bldg_mesh2"]}{mesh3}'
                     f'_bldg_{bldg_crs_from}_op')
        building_attributes_list = []

        # ワールドを保存
        if table_is_exist(db_cursor, table_name):
            print('database exists:', table_name)

            decoder = json.JSONDecoder()
            with open(output_file_path, 'r') as f:
                line = f.readline()
                while line:
                    attributes = decoder.raw_decode(line)[0]
                    attributes['positions'] = [list(map(float, p.split('/'))) for p in
                                               attributes['positions'].split('|')]
                    # print(attributes['center_position'])
                    attributes['center_position'] = list(map(float, attributes['center_position'].split('/')))
                    building_attributes_list.append(attributes)
                    line = f.readline()
        else:
            print('not fount:', output_file_path)
            count = 0

            file_path = f'data/{file_name}.gml'
            if not os.path.exists(file_path):
                print('not found:', file_path)
                return
            else:
                print('file exists:', file_path)
                db_cursor.execute(
                    f'CREATE TABLE IF NOT EXISTS {file_name}('
                    'building_id TEXT PRIMARY KEY UNIQUE, '
                    'name TEXT, '
                    'height TEXT, '
                    'positions TEXT, '
                    'center_position TEXT, '
                    'created_at TEXT NOT NULL DEFAULT (DATETIME(\'now\', \'localtime\')), '
                    'updated_at TEXT NOT NULL DEFAULT (DATETIME(\'now\', \'localtime\')))'
                )

            # XMLファイルを解析
            tree = ET.parse(file_path)

            # XMLを取得
            root = tree.getroot()

            # 接頭辞の辞書
            ns = {
                'core': 'http://www.opengis.net/citygml/2.0',
                'bldg': 'http://www.opengis.net/citygml/building/2.0',
                'gml': 'http://www.opengis.net/gml',
                'gen': 'http://www.opengis.net/citygml/generics/2.0',
            }

            for building in root.findall('core:cityObjectMember/bldg:Building', ns):
                building_attributes = {
                    'name': '',
                    'building_id': '',
                    'height': 0,
                }
                positions = None
                for child in building:
                    if child.tag == '{http://www.opengis.net/gml}name':
                        building_attributes['name'] = child.text
                    if 'name' in child.attrib and child.attrib['name'] == '建物ID':
                        building_attributes['building_id'] = child[0].text
                    if child.tag == '{http://www.opengis.net/citygml/building/2.0}lod1Solid':
                        geo_text = child[0][0][0][0][0][0][0][0].text
                        positions = get_building_positions(geo_text, _bldg_crs_from, settings['crs_to'])

                    # heightは2つの方法のどちらかで取得できる
                    if 'name' in child.attrib and child.attrib['name'] == '建物高さ':
                        building_attributes['height'] = float(child[0].text)
                    if child.tag == '{http://www.opengis.net/citygml/building/2.0}measuredHeight':
                        building_attributes['height'] = float(child.text)

                # print(building_attribute)
                if positions:
                    count += 1
                    print('count:', count)
                    building_attributes['id'] = count

                    building_attributes['positions'] = positions
                    x0 = sum([position[0] for position in positions]) / len(positions)
                    y0 = sum([position[1] for position in positions]) / len(positions)
                    building_attributes['center_position'] = [x0, y0, 0]

                    building_attributes_list.append(building_attributes)

                    # データベース保存
                    positions_text = \
                        '|'.join(['/'.join([str(v) for v in l]) for l in building_attributes['positions']])
                    center_position_text = '/'.join(map(str, building_attributes['center_position']))
                    inserts = (
                        building_attributes['building_id'],
                        building_attributes['name'],
                        building_attributes['height'],
                        positions_text,
                        center_position_text
                    )

                    db_cursor.execute(
                        'INSERT INTO buildings(building_id, name, height, positions, center_position) '
                        'values(?, ?, ?, ?, ?)',
                        inserts)

            # with open(output_file_path, 'w') as f:
            #     attributes_list = copy.deepcopy(building_attributes_list)
            #     for attributes in attributes_list:
            #         attributes['positions'] = \
            #             '|'.join(['/'.join([str(v) for v in l]) for l in attributes['positions']])
            #         attributes['center_position'] ='/'.join([str(v) for v in attributes['center_position']])
            #
            #     l = [json.dumps(attributes) for attributes in attributes_list]
            #     f.write('\n'.join(l))

        all_building_attributes_list += building_attributes_list

    db.commit()

    return all_building_attributes_list


def get_min_and_max_position(attributes_list):
    # print(attributes_list[0])
    # print(attributes_list[1])
    x_positions = [attributes['positions'][0][0] for attributes in attributes_list if attributes['positions']]
    y_positions = [attributes['positions'][0][1] for attributes in attributes_list if attributes['positions']]
    # print(x_positions)
    # print(y_positions)
    min_position = Point3(min(x_positions), min(y_positions), 0)
    max_position = Point3(max(x_positions), max(y_positions), 0)

    return min_position, max_position


if __name__ == '__main__':
    # location = (35.89501065742873, 139.63187403357193)
    # print(change_to_cartesian(*location))

    attributes_list = get_building_attributes_list()
    # print(attributes_list)
    # print(len(attributes_list))

    # road_attributes_list = get_road_attributes_list()
    # # print(road_attributes_list)
    # print(len(road_attributes_list))
