from math import sqrt
import sqlite3
import os
import xml.etree.ElementTree as ET
from panda3d.core import *
from . import get_building_positions, get_road_positions


class Database:
    def __init__(self):
        self.db = sqlite3.connect('output/plateau_panda3d.sqlite3')
        self.db_cursor = self.db.cursor()
        # データベースの作成
        self.road_count = 0
        self.create_road_table()
        self.create_building_table()
        self.area_center = self.get_area_center()

    def table_is_exist(self, table_name):
        self.db_cursor.execute(
            'SELECT COUNT(*) FROM sqlite_master '
            f'WHERE TYPE="table" AND name="{table_name}"'
        )
        if self.db_cursor.fetchone()[0] == 0:
            return False
        return True

    def get_area_center(self):
        settings = self.settings
        mesh3_list = settings['bldg_mesh3_list']
        x_positions = []
        y_positions = []
        for mesh3 in mesh3_list:
            file_name = (f'{settings["bldg_mesh1"]}{settings["bldg_mesh2"]}{mesh3}'
                         f'_bldg_{settings["bldg_crs_from"]}_op')
            table_name = f'plateau_{file_name}'

            # ワールド名のリストを取得
            self.db_cursor.execute(
                f'SELECT center_position FROM {table_name}'
            )
            center_positions = [tuple_value[0].split('/') for tuple_value in self.db_cursor.fetchall()]
            # print(center_positions)

            # print(attributes_list[0])
            # print(attributes_list[1])
            x_positions += [float(position[0]) for position in center_positions]
            y_positions += [float(position[1]) for position in center_positions]
            # print(x_positions)
            # print(y_positions)

        min_position = Point3(min(x_positions), min(y_positions), 0)
        max_position = Point3(max(x_positions), max(y_positions), 0)

        return (min_position + max_position) / 2

    def create_building_table(self):
        settings = self.settings
        mesh3_list = settings['bldg_mesh3_list']
        bldg_crs_from = settings['bldg_crs_from']
        if len(bldg_crs_from.split('_')) > 1:
            _bldg_crs_from = bldg_crs_from.split('_')[0]
        else:
            _bldg_crs_from = bldg_crs_from

        for mesh3 in mesh3_list:
            file_name = (f'{settings["bldg_mesh1"]}{settings["bldg_mesh2"]}{mesh3}'
                         f'_bldg_{settings["bldg_crs_from"]}_op')
            table_name = f'plateau_{file_name}'

            # 建物を保存
            if self.table_is_exist(table_name):
                print('database exists:', table_name)
            else:
                print('not fount:', table_name)
                count = 0
                file_path = f'data/{file_name}.gml'

                if not os.path.exists(file_path):
                    print('not found:', file_path)
                    return
                else:
                    print('file exists:', file_path)
                    self.db_cursor.execute(
                        f'CREATE TABLE IF NOT EXISTS {table_name}('
                        'building_id TEXT PRIMARY KEY UNIQUE, '
                        'name TEXT, '
                        'height TEXT, '
                        'positions TEXT, '
                        'center_position TEXT, '
                        'max_distance REAL, '
                        'min_distance REAL, '
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
                    name = ''
                    building_id = ''
                    height = 0
                    positions = None
                    for child in building:
                        if child.tag == '{http://www.opengis.net/gml}name':
                            name = child.text
                        if 'name' in child.attrib and child.attrib['name'] == '建物ID':
                            building_id = child[0].text
                        if child.tag == '{http://www.opengis.net/citygml/building/2.0}lod1Solid':
                            geo_text = child[0][0][0][0][0][0][0][0].text
                            positions = get_building_positions(geo_text, _bldg_crs_from, settings['crs_to'])

                        # heightは2つの方法のどちらかで取得できる
                        if 'name' in child.attrib and child.attrib['name'] == '建物高さ':
                            height = float(child[0].text)
                        if child.tag == '{http://www.opengis.net/citygml/building/2.0}measuredHeight':
                            height = float(child.text)

                    if positions and height:
                        count += 1
                        print('count:', count)

                        x0 = sum([position[0] for position in positions]) / len(positions)
                        y0 = sum([position[1] for position in positions]) / len(positions)
                        center_position = [x0, y0, 0]

                        distances_from_center = [sqrt((x - x0)**2 + (y - y0)**2) for x, y, _ in positions]
                        max_distance = max(distances_from_center)
                        min_distance = min(distances_from_center)

                        # データベース保存
                        positions_text = \
                            '|'.join(['/'.join([str(v) for v in l]) for l in positions])
                        center_position_text = '/'.join(map(str, center_position))
                        inserts = (
                            building_id,
                            name,
                            height,
                            positions_text,
                            center_position_text,
                            max_distance,
                            min_distance
                        )

                        self.db_cursor.execute(
                            f'INSERT INTO {table_name}'
                            f'(building_id, name, height, positions, center_position, max_distance, min_distance) '
                            'values(?, ?, ?, ?, ?, ?, ?)',
                            inserts)

        self.db.commit()

    def create_road_table(self):
        settings = self.settings
        mesh3_list = settings['road_mesh3_list']
        road_crs_from = settings['road_crs_from']
        if len(road_crs_from.split('_')) > 1:
            self.road_crs_from = road_crs_from.split('_')[0]
        else:
            self.road_crs_from = road_crs_from

        for mesh3 in mesh3_list:
            file_name = (f'{settings["bldg_mesh1"]}{settings["bldg_mesh2"]}{mesh3}'
                         f'_tran_{settings["road_crs_from"]}_op')
            table_name = f'plateau_{file_name}'

            # 道路を保存
            if self.table_is_exist(table_name):
                print('database exists:', table_name)
            else:
                print('not found:', table_name)
                self.road_count = 0
                file_path = f'data/{file_name}.gml'

                if not os.path.exists(file_path):
                    print('not found:', file_path)
                    return
                else:
                    print('file exists:', file_path)
                    self.db_cursor.execute(
                        f'CREATE TABLE IF NOT EXISTS {table_name}('
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
                    'tran': 'http://www.opengis.net/citygml/transportation/2.0'
                }

                for road in root.findall('core:cityObjectMember/tran:Road', ns):
                    # print(road.tag, road.attrib)
                    road_lod1 = road.find('tran:lod1MultiSurface', ns)

                    if road_lod1:
                        for _road in road_lod1.findall('gml:MultiSurface/gml:surfaceMember', ns):
                            # print(_road.tag, _road.attrib)
                            geo_text = _road[0][0][0][0].text
                            self.write_road(geo_text, table_name)
                    else:
                        geo_text = road[0][0][0][0][0][0].text
                        self.write_road(geo_text, table_name)

        self.db.commit()

    def write_road(self, geo_text, table_name):
        settings = self.settings
        positions = get_road_positions(geo_text, self.road_crs_from, settings['crs_to'])
        if positions:
            self.road_count += 1
            print('count:', self.road_count)

            x0 = sum([position[0] for position in positions]) / len(positions)
            y0 = sum([position[1] for position in positions]) / len(positions)
            center_position = [x0, y0, 0]

            # データベース保存
            positions_text = \
                '|'.join(['/'.join([str(v) for v in l]) for l in positions])
            center_position_text = '/'.join(map(str, center_position))
            inserts = (
                positions_text,
                center_position_text
            )

            self.db_cursor.execute(
                f'INSERT INTO {table_name}(positions, center_position) '
                'values(?, ?)',
                inserts)
