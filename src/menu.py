"""src/menu.py"""
import os
import sys
import sqlite3
from panda3d.core import *
from .ground import Ground
from .building import Building
from .collision import Collision
from .celestial_sphere import CelestialSphere
from .wire_frame import WireFrame
from .solid_model import SolidModel
from .gui_parts import *


class Menu:
    def __init__(self):
        self.menu_node = self.aspect2d.attachNewNode('menu_node')
        self.menu_node.stash()
        self.select_menu_node = self.menu_node.attachNewNode('select_menu_node')
        self.select_menu_node.stash()
        self.save_node = self.menu_node.attachNewNode('save_node')
        self.save_node.stash()
        self.load_node = self.menu_node.attachNewNode('load_node')
        self.load_node.stash()
        self.join_node = self.menu_node.attachNewNode('join_node')
        self.join_node.stash()

        menu_cm = CardMaker('menu_card')
        menu_cm.setFrame(-1.5, 1.5, -1, 1)
        self.menu_background_node = self.render2d.attachNewNode(menu_cm.generate())
        self.menu_background_node.setTransparency(1)
        self.menu_background_node.setColor(0, 0, 0, 0.5)
        self.menu_background_node.stash()

        self.button_model = self.loader.loadModel('models/button_maps')
        self.frame_texture = self.loader.loadTexture('models/maps/button/button_up.png')

        # Menu Screen
        self.resume_button = DrawMappedButton(
            parent=self.select_menu_node,
            model=self.button_model,
            text='ゲームに戻る',
            font=self.font,
            pos=(0, 0, 0.4),
            command=self.toggle_menu
        )
        self.toggle_save_button = DrawMappedButton(
            parent=self.select_menu_node,
            model=self.button_model,
            text='ゲームをセーブ',
            font=self.font,
            pos=(0, 0, 0.24),
            command=self.toggle_save
        )
        self.toggle_load_button = DrawMappedButton(
            parent=self.select_menu_node,
            model=self.button_model,
            text='ゲームをロード',
            font=self.font,
            pos=(0, 0, 0.08),
            command=self.toggle_load
        )
        self.server_button = DrawMappedButton(
            parent=self.select_menu_node,
            model=self.button_model,
            text='サーバーを開始',
            font=self.font,
            pos=(0, 0, -0.08),
            command=self.open_server
        )
        self.toggle_join_button = DrawMappedButton(
            parent=self.select_menu_node,
            model=self.button_model,
            text='サーバーに接続',
            font=self.font,
            pos=(0, 0, -0.24),
            command=self.toggle_join
        )
        self.exit_button = DrawMappedButton(
            parent=self.select_menu_node,
            model=self.button_model,
            text='ゲームを終了',
            font=self.font,
            pos=(0, 0, -0.4),
            command=self.exit_game
        )

        # Save Screen
        self.save_input_field = DrawEntry(
            parent=self.save_node,
            frame_texture=self.frame_texture,
            initial_text='My World',
            font=self.font,
            pos=(-0.6, 0, 0.1),
            command=self.save_world,
        )
        self.save_text = DrawLabel(
            parent=self.save_node,
            text='セーブする「ワールドの名前」を入力',
            font=self.font,
            pos=(0, 0, 0.35),
            scale=0.075
        )
        self.save_notification_text = DrawLabel(
            parent=self.save_node,
            text='',
            font=self.font,
            pos=(0, 0, -0.45),
            scale=0.06
        )
        self.save_button = DrawMappedButton(
            parent=self.save_node,
            model=self.button_model,
            text='セーブする',
            font=self.font,
            pos=(0, 0, -0.1),
            command=self.save_world
        )
        self.save_back_button = DrawMappedButton(
            parent=self.save_node,
            model=self.button_model,
            text='メニューに戻る',
            font=self.font,
            pos=(0, 0, -0.25),
            command=self.toggle_save
        )

        # # Load Screen
        self.load_list = DrawScrolledList(
            parent=self.load_node,
            model=self.button_model,
            frame_texture=self.frame_texture,
            pos=(-0.45, 0, -0.25),
            scale=1.25,
            num_items_visible=3,
            item_height=0.15,
        )
        self.load_text = DrawLabel(
            parent=self.load_node,
            text='ロードする「ワールドの名前」を選ぶ',
            font=self.font,
            pos=(0, 0, 0.55),
            scale=0.075
        )
        self.load_notification_text = DrawLabel(
            parent=self.load_node,
            text='',
            font=self.font,
            pos=(0, 0, -0.7),
            scale=0.075
        )
        self.load_back_button = DrawMappedButton(
            parent=self.load_node,
            model=self.button_model,
            text='メニューに戻る',
            font=self.font,
            pos=(0, 0, -0.5),
            command=self.toggle_load
        )

        # Join Screen
        self.join_input_field = DrawEntry(
            parent=self.join_node,
            frame_texture=self.frame_texture,
            initial_text='localhost',
            font=self.font,
            pos=(-0.6, 0, 0.1),
            command=self.connect_as_client,
        )
        self.join_text = DrawLabel(
            parent=self.join_node,
            text='「サーバーのURL」を入力',
            font=self.font,
            pos=(0, 0, 0.35),
            scale=0.075
        )
        self.join_notification_text = DrawLabel(
            parent=self.join_node,
            text='',
            font=self.font,
            pos=(0, 0, -0.45),
            scale=0.06
        )
        self.join_button = DrawMappedButton(
            parent=self.join_node,
            model=self.button_model,
            text='サーバーに接続',
            font=self.font,
            pos=(0, 0, -0.1),
            command=self.connect_as_client
        )
        self.join_back_button = DrawMappedButton(
            parent=self.join_node,
            model=self.button_model,
            text='メニューに戻る',
            font=self.font,
            pos=(0, 0, -0.25),
            command=self.toggle_join
        )

        # ユーザー操作
        self.accept('f12', self.f12_key)

    def f12_key(self):
        self.toggle_menu()

    def toggle_menu(self):
        if self.menu_node.isStashed():
            self.menu_node.unstash()
            self.select_menu_node.unstash()
            self.save_node.stash()
            self.load_node.stash()
            self.join_node.stash()
            self.menu_background_node.unstash()
        else:
            self.menu_node.stash()
            self.select_menu_node.stash()
            self.save_node.stash()
            self.load_node.stash()
            self.join_node.stash()
            self.menu_background_node.stash()

    def toggle_save(self):
        if self.save_node.isStashed():
            self.select_menu_node.stash()
            self.save_node.unstash()
            self.save_notification_text.setText('')
        else:
            self.select_menu_node.unstash()
            self.save_node.stash()

    def toggle_load(self):
        if self.load_node.isStashed():
            self.select_menu_node.stash()
            self.load_node.unstash()
            self.load_notification_text.setText('')
            self.add_list_items()
        else:
            self.select_menu_node.unstash()
            self.load_node.stash()

    def toggle_join(self):
        if self.join_node.isStashed():
            self.select_menu_node.stash()
            self.join_node.unstash()
            self.join_notification_text.setText('')
        else:
            self.select_menu_node.unstash()
            self.join_node.stash()

    def get_world_id_from_name(self, world_name):
        self.save_db_cursor.execute(
            'SELECT id from worlds where name = ?',
            (world_name,)
        )
        result = self.save_db_cursor.fetchone()

        if result:
            return result[0]
        else:
            return None

    def save_world(self):
        world_name = self.save_input_field.get(True)
        if world_name:
            settings = self.settings['plateau_settings']

            # セーブ処理
            self.save_db_cursor.execute(
                'SELECT COUNT(*) FROM worlds WHERE name = ?',
                (world_name,))
            has_same_world_name = self.save_db_cursor.fetchone()[0]
            # print(has_same_world_name)

            # ワールドを保存
            if has_same_world_name:
                print('update')
                self.save_notification_text['text'] = 'アップデートしています...'
                world_data = (
                    settings['bldg_mesh1'],
                    settings['bldg_mesh2'],
                    ','.join(settings['bldg_mesh3_list']),
                    ','.join(settings['road_mesh3_list']),
                    settings['bldg_crs_from'],
                    settings['road_crs_from'],
                    settings['crs_to'],
                    self.settings['sky_texture'],
                    world_name,
                )
                self.save_db_cursor.execute(
                    'UPDATE worlds SET '
                    'bldg_mesh1 = ?, '
                    'bldg_mesh2 = ?, '
                    'bldg_mesh3_list = ?, '
                    'road_mesh3_list = ?, '
                    'bldg_crs_from = ?, '
                    'road_crs_from = ?, '
                    'crs_to = ?, '
                    'sky_texture = ? '
                    'WHERE name = ? ',
                    world_data
                )
            else:
                print('save')
                self.save_notification_text['text'] = 'セーブしています...'
                world_data = (
                    world_name,
                    settings['bldg_mesh1'],
                    settings['bldg_mesh2'],
                    ','.join(settings['bldg_mesh3_list']),
                    ','.join(settings['road_mesh3_list']),
                    settings['bldg_crs_from'],
                    settings['road_crs_from'],
                    settings['crs_to'],
                    self.settings['sky_texture'],
                )
                self.save_db_cursor.execute(
                    'INSERT INTO worlds('
                    'name, bldg_mesh1, bldg_mesh2, bldg_mesh3_list, road_mesh3_list, '
                    'bldg_crs_from, road_crs_from, crs_to, sky_texture) '
                    'values(?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    world_data
                )

            # world_id を取得
            world_id = self.get_world_id_from_name(world_name)

            # ビルデータを初期化
            self.save_db_cursor.execute(
                'DELETE FROM buildings where world_id = ?',
                (world_id,)
            )

            # ビルデータを保存
            inserts = []
            for key, value in self.database_buildings.items():
                building_id = key
                removed = value['removed']
                hidden = value['hidden']
                inserts.append((building_id, removed, hidden, world_id))
            print(self.database_buildings)
            print(inserts)
            self.save_db_cursor.executemany(
                'INSERT INTO buildings(building_id, removed, hidden, world_id) values(?, ?, ?, ?)',
                inserts
            )
            #
            # # プレイヤーを初期化
            # self.save_db_cursor.execute(
            #     'DELETE FROM characters where world_id = ?',
            #     (world_id,)
            # )
            #
            # # プレイヤー情報を保存
            # character_type = 'player'
            # x, y, z = self.player.position
            # direction_x, direction_y, direction_z = self.player.direction
            # self.save_db_cursor.execute(
            #     'INSERT INTO characters(character_type, x, y, z, direction_x, direction_y, direction_z, world_id) '
            #     'values(?, ?, ?, ? ,?, ?, ?, ?)',
            #     (character_type, x, y, z, direction_x, direction_y, direction_z, world_id)
            # )

            self.save_db.commit()
            if has_same_world_name:
                self.save_notification_text['text'] = 'アップデート完了！'
            else:
                self.save_notification_text['text'] = 'セーブ完了！'
        else:
            self.save_notification_text['text'] = 'ワールド名を入力してください。'

    def get_world_names(self):
        # ワールド名のリストを取得
        self.save_db_cursor.execute(
            'SELECT name FROM worlds ORDER BY updated_at DESC'
        )
        world_names = [value[0] for value in self.save_db_cursor.fetchall()]

        return world_names

    def add_list_items(self):
        self.load_list.removeAndDestroyAllItems()

        world_names = self.get_world_names()
        for name in world_names:
            list_item = DrawMappedButton(
                parent=None,
                model=self.button_model,
                text=name,
                font=self.font,
                pos=(0, 0, -0.75),
                command=self.load_world,
                extra_args=[name]
            )
            self.load_list.addItem(list_item)

    def load_world(self, world_name):
        # ロード処理
        self.save_db_cursor.execute(
            'SELECT bldg_mesh1,bldg_mesh2, bldg_mesh3_list, road_mesh3_list, '
            'bldg_crs_from, road_crs_from, crs_to, sky_texture '
            'FROM worlds WHERE name = ?',
            (world_name,)
        )
        (bldg_mesh1, bldg_mesh2, bldg_mesh3_list, road_mesh3_list, bldg_crs_from, road_crs_from, crs_to,
         sky_texture) = self.save_db_cursor.fetchone()

        plateau_settings = self.settings['plateau_settings']
        plateau_settings['bldg_mesh1'] = bldg_mesh1
        plateau_settings['bldg_mesh2'] = bldg_mesh2
        plateau_settings['bldg_mesh3_list'] = bldg_mesh3_list.split(',')
        plateau_settings['road_mesh3_list'] = road_mesh3_list.split(',')
        plateau_settings['bldg_crs_from'] = bldg_crs_from
        plateau_settings['road_crs_from'] = road_crs_from
        plateau_settings['crs_to'] = crs_to
        self.settings['sky_texture'] = sky_texture

        # ワールドの中心座標
        self.area_center = self.get_area_center()
        self.camera_base_node.setPos(self.area_center)
        self.axis_node.setPos(self.area_center)
        self.ground_node.setPos(self.area_center)
        self.players_node.setPos(self.area_center)
        self.mobs_node.setPos(self.area_center)

        # 初期化
        self.map_node.removeNode()
        # 再構築
        Building.__init__(self)
        Collision.__init__(self)
        CelestialSphere.__init__(self)
        WireFrame.__init__(self)
        SolidModel.__init__(self)

        # # ビルを復元
        world_id = self.get_world_id_from_name(world_name)

        if world_id:
            self.save_db_cursor.execute('SELECT * FROM buildings WHERE world_id = ?', (world_id,))
            buildings = self.save_db_cursor.fetchall()
            for building in buildings:
                # print(building)
                _, building_id, removed, hidden, _ = building

                if building_id[:6] == 'build ':
                    self.build_shape(building_id)

                building_node = self.map_node.find(building_id)

                if removed:
                    self.all_buildings.remove(building_node)
                    building_node.removeNode()
                    self.database_buildings[building_id] = {'removed': 1, 'hidden': 0}

                if hidden:
                    building_node.hide()
                    building_node.setPythonTag('is_hidden', True)
                    self.database_buildings[building_id] = {'removed': 0, 'hidden': 1}

            # # プレイヤーを更新
            # self.save_db_cursor.execute(
            #     'SELECT x, y, z, direction_x, direction_y, direction_z FROM characters WHERE world_id = ? AND character_type = ?',
            #     (world_id, 'player')
            # )
            # # print(self.save_db_cursor.fetchall())
            # x, y, z, direction_x, direction_y, direction_z = self.save_db_cursor.fetchall()[0]
            # self.player.position = Point3(x, y, z)
            # self.player.direction = Vec3(direction_x, direction_y, direction_z)
            self.load_notification_text['text'] = 'ロードが完了しました。'
        else:
            self.load_notification_text['text'] = 'ロードできませんでした。'
