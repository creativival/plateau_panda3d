"""src/menu.py"""
import os
import sys
import sqlite3
from panda3d.core import *
from .gui_parts import *


class Menu:
    def __init__(self):
        self.menu_node = self.aspect2d.attachNewNode('menu_node')
        self.menu_node.stash()
        self.save_node = self.aspect2d.attachNewNode('save_node')
        self.save_node.stash()
        self.load_node = self.aspect2d.attachNewNode('load_node')
        self.load_node.stash()
        self.join_node = self.aspect2d.attachNewNode('join_node')
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
            parent=self.menu_node,
            model=self.button_model,
            text='ゲームに戻る',
            font=self.font,
            pos=(0, 0, 0.4),
            command=self.toggle_menu
        )
        self.toggle_save_button = DrawMappedButton(
            parent=self.menu_node,
            model=self.button_model,
            text='ゲームをセーブ',
            font=self.font,
            pos=(0, 0, 0.24),
            command=self.toggle_save
        )
        self.toggle_load_button = DrawMappedButton(
            parent=self.menu_node,
            model=self.button_model,
            text='ゲームをロード',
            font=self.font,
            pos=(0, 0, 0.08),
            command=self.toggle_load
        )
        self.server_button = DrawMappedButton(
            parent=self.menu_node,
            model=self.button_model,
            text='サーバーを開始',
            font=self.font,
            pos=(0, 0, -0.08),
            command=self.open_server
        )
        self.toggle_join_button = DrawMappedButton(
            parent=self.menu_node,
            model=self.button_model,
            text='サーバーに接続',
            font=self.font,
            pos=(0, 0, -0.24),
            command=self.toggle_join
        )
        self.exit_button = DrawMappedButton(
            parent=self.menu_node,
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
            command=self.toggle_save
        )

        # ユーザー操作
        self.accept('f12', self.f12_key)

    def f12_key(self):
        if (self.save_node.isStashed() and
                self.load_node.isStashed() and
                self.join_node.isStashed()):
            self.toggle_menu()

    def toggle_menu(self):
        if self.menu_node.isStashed():
            self.menu_node.unstash()
            self.menu_background_node.unstash()
        else:
            self.menu_node.stash()
            self.menu_background_node.stash()

    def toggle_save(self):
        if self.save_node.isStashed():
            self.menu_node.stash()
            self.save_node.unstash()
            self.save_notification_text.setText('')
        else:
            self.menu_node.unstash()
            self.save_node.stash()

    def toggle_load(self):
        if self.load_node.isStashed():
            self.menu_node.stash()
            self.load_node.unstash()
            self.load_notification_text.setText('')
            self.add_list_items()
        else:
            self.menu_node.unstash()
            self.load_node.stash()

    def toggle_join(self):
        if self.join_node.isStashed():
            self.menu_node.stash()
            self.join_node.unstash()
            self.join_notification_text.setText('')
        else:
            self.menu_node.unstash()
            self.join_node.stash()

    def get_world_id_from_name(self, world_name):
        self.save_db_cursor.execute(
            'SELECT id from worlds where name = ?',
            (world_name,)
        )
        world_id = self.save_db_cursor.fetchone()[0]

        return world_id

    def save_world(self):
        world_name = self.save_input_field.get(True)
        if world_name:
            settings = self.settings

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
                    settings['sky_texture'],
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
                    settings['sky_texture'],
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
        # # ブロックを全て削除
        self.block_node.removeNode()

        # ブロックを復元
        self.block_node = self.render.attachNewNode(PandaNode('block_node'))
        world_id = self.get_world_id_from_name(world_name)
        self.save_db_cursor.execute('SELECT * FROM blocks WHERE world_id = ?', (world_id,))
        recorded_blocks = self.save_db_cursor.fetchall()
        for block in recorded_blocks:
            _, x, y, z, block_id, _ = block
            self.block.add_block(x, y, z, block_id)

        # プレイヤーを更新
        self.save_db_cursor.execute(
            'SELECT x, y, z, direction_x, direction_y, direction_z FROM characters WHERE world_id = ? AND character_type = ?',
            (world_id, 'player')
        )
        # print(self.save_db_cursor.fetchall())
        x, y, z, direction_x, direction_y, direction_z = self.save_db_cursor.fetchall()[0]
        self.player.position = Point3(x, y, z)
        self.player.direction = Vec3(direction_x, direction_y, direction_z)
