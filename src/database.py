from math import sqrt, atan2
import sqlite3
import os
import xml.etree.ElementTree as ET
from panda3d.core import *
from . import get_building_positions, get_road_positions


class Database:
    def __init__(self):
        # ビル・道路のデータ
        self.db = sqlite3.connect('output/plateau_panda3d.sqlite3')
        self.db_cursor = self.db.cursor()
        self.road_count = None
        self.create_road_table()
        self.create_building_table()

        # ワールドの中心座標
        self.area_center = self.get_area_center()

        # セーブ
        self.save_db = sqlite3.connect('output/save.sqlite3')
        self.save_db_cursor = self.save_db.cursor()
        self.create_save_tables()

    def table_is_exist(self, table_name):
        self.db_cursor.execute(
            'SELECT COUNT(*) FROM sqlite_master '
            f'WHERE TYPE="table" AND name="{table_name}"'
        )
        if self.db_cursor.fetchone()[0] == 0:
            return False
        return True

    def get_area_center(self):
        settings = self.settings['plateau_settings']
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
        settings = self.settings['plateau_settings']
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
            file_path = f'data/{file_name}.gml'
            count = 0

            # 建物を保存
            if self.table_is_exist(table_name):
                print('database exists:', table_name)
                self.db_cursor.execute(
                    f'SELECT count(*) from {table_name}'
                )
                result = self.db_cursor.fetchone()
                if result[0] > 1:
                    print('record count:', result[0])
                    return
            else:
                print('not fount:', table_name)

                if not os.path.exists(file_path):
                    print('not found:', file_path)
                    return
                else:
                    print('file exists:', file_path)
                    self.db_cursor.execute(
                        f'CREATE TABLE IF NOT EXISTS {table_name}('
                        'building_id TEXT PRIMARY KEY UNIQUE, '
                        'name TEXT, '
                        'height REAL, '
                        'positions TEXT, '
                        'center_position TEXT, '
                        'max_distance REAL, '
                        'min_distance REAL, '
                        'max_angle REAL, '
                        'min_angle REAL, '
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
                    max_x, max_y, _ = positions[distances_from_center.index(max_distance)]
                    max_angle = atan2((max_y - y0), (max_x - x0))
                    min_distance = min(distances_from_center)
                    min_x, min_y, _ = positions[distances_from_center.index(min_distance)]
                    min_angle = atan2((min_y - y0), (min_x - x0))

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
                        min_distance,
                        max_angle,
                        min_angle
                    )

                    self.db_cursor.execute(
                        f'INSERT INTO {table_name}'
                        '(building_id, name, height, positions, center_position, '
                        'max_distance, min_distance, max_angle, min_angle) '
                        'values(?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        inserts)

        self.db.commit()

    def create_road_table(self):
        settings = self.settings['plateau_settings']
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
            file_path = f'data/{file_name}.gml'
            self.road_count = 0

            # 道路を保存
            if self.table_is_exist(table_name):
                print('database exists:', table_name)
                self.db_cursor.execute(
                    f'SELECT count(*) from {table_name}'
                )
                result = self.db_cursor.fetchone()
                if result[0] > 1:
                    print('record count:', result[0])
                    return
            else:
                print('not found:', table_name)

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
        settings = self.settings['plateau_settings']
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

    def create_save_tables(self):
        self.save_db_cursor.execute(
            'CREATE TABLE IF NOT EXISTS worlds('
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'name TEXT UNIQUE, '
            'bldg_mesh1 TEXT, '
            'bldg_mesh2 TEXT, '
            'bldg_mesh3_list TEXT, '
            'road_mesh3_list TEXT, '
            'bldg_crs_from TEXT, '
            'road_crs_from TEXT, '
            'crs_to TEXT, '
            'sky_texture TEXT, '
            'created_at TEXT NOT NULL DEFAULT (DATETIME(\'now\', \'localtime\')), '
            'updated_at TEXT NOT NULL DEFAULT (DATETIME(\'now\', \'localtime\')))'
        )
        self.save_db_cursor.execute(
            'CREATE TRIGGER IF NOT EXISTS trigger_worlds_updated_at AFTER UPDATE ON worlds '
            'BEGIN'
            '   UPDATE worlds SET updated_at = DATETIME(\'now\', \'localtime\') WHERE rowid == NEW.rowid;'
            'END'
        )
        self.save_db_cursor.execute(
            'CREATE TABLE IF NOT EXISTS characters('
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'character_type TEXT, '
            'x INTEGER, '
            'y INTEGER, '
            'z INTEGER, '
            'direction_x INTEGER, '
            'direction_y INTEGER, '
            'direction_z INTEGER, '
            'world_id INTEGER)'
        )
        self.save_db_cursor.execute(
            'CREATE TABLE IF NOT EXISTS buildings('
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'building_id TEXT, '
            'removed INTEGER DEFAULT 0, '
            'hidden INTEGER DEFAULT 0, '
            'world_id INTEGER)'
        )
