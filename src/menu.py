"""src/menu.py"""
import os
import sys
import sqlite3
from panda3d.core import *
from .gui_util import *


class Menu:
    save_path = 'saves'
    db_name = 'pynecrafter'

    def __init__(self):
        # sqlite3データベース
        self.db = None
        self.cursor = None

        self.menu_node = self.aspect2d.attachNewNode('menu_node')
        self.menu_node.stash()
        self.save_node = self.aspect2d.attachNewNode('save_node')
        self.save_node.stash()
        self.load_node = self.aspect2d.attachNewNode('load_node')
        self.load_node.stash()

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
        self.save_button = DrawMappedButton(
            parent=self.menu_node,
            model=self.button_model,
            text='ゲームをセーブ',
            font=self.font,
            pos=(0, 0, 0.24),
            command=self.toggle_save
        )
        self.load_button = DrawMappedButton(
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
        self.join_button = DrawMappedButton(
            parent=self.menu_node,
            model=self.button_model,
            text='サーバーに接続',
            font=self.font,
            pos=(0, 0, -0.24),
            command=self.join_server
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

        # ユーザー操作
        self.accept('f12', self.toggle_menu)

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

    def connect_db(self):
        path = Menu.save_path
        db_name = Menu.db_name
        if not os.path.exists(path):
            os.makedirs(path)
        if self.db is None:
            self.db = sqlite3.connect(f'{path}/{db_name}.sqlite3')
            self.cursor = self.db.cursor()

    def create_tables(self):
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS worlds('
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'name TEXT UNIQUE, '
            'ground_size INTEGER, '
            'game_mode TEXT, '
            'created_at TEXT NOT NULL DEFAULT (DATETIME(\'now\', \'localtime\')), '
            'updated_at TEXT NOT NULL DEFAULT (DATETIME(\'now\', \'localtime\')))'
        )
        self.cursor.execute(
            'CREATE TRIGGER IF NOT EXISTS trigger_worlds_updated_at AFTER UPDATE ON worlds '
            'BEGIN'
            '   UPDATE test SET updated_at = DATETIME(\'now\', \'localtime\') WHERE rowid == NEW.rowid;'
            'END'
        )
        self.cursor.execute(
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
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS blocks('
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'x INTEGER, '
            'y INTEGER, '
            'z INTEGER, '
            'block_id INTEGER, '
            'world_id INTEGER)'
        )

    def get_world_id_from_name(self, world_name):
        self.cursor.execute(
            'SELECT id from worlds where name = ?',
            (world_name,)
        )
        world_id = self.cursor.fetchone()[0]

        return world_id

    def save_world(self):
        world_name = self.save_input_field.get(True)
        if world_name:
            self.save_notification_text['text'] = 'セーブしています...'

            # セーブ処理
            self.connect_db()
            self.create_tables()
            self.cursor.execute('SELECT COUNT(*) FROM worlds WHERE name = ?', (world_name,))
            has_same_world_name = self.cursor.fetchone()[0]
            # print(has_same_world_name)

            # ワールドを保存
            if has_same_world_name:
                self.cursor.execute(
                    'UPDATE worlds SET ground_size = ?, game_mode = ? ',
                    (self.ground_size, self.mode)
                )
            else:
                self.cursor.execute(
                    'INSERT INTO worlds(name, ground_size, game_mode) values(?, ?, ?)',
                    (world_name, self.ground_size, self.mode)
                )

            # world_id を取得
            world_id = self.get_world_id_from_name(world_name)

            # ブロックデータを初期化
            self.cursor.execute(
                'DELETE FROM blocks where world_id = ?',
                (world_id,)
            )

            # ブロックデータを保存
            inserts = []
            for key, value in self.block.block_dictionary.items():
                x, y, z = key.split('_')
                block_id = value
                inserts.append((x, y, z, block_id, world_id))
            self.cursor.executemany(
                'INSERT INTO blocks(x, y, z, block_id, world_id) values(?, ?, ?, ? ,?)',
                inserts
            )

            # プレイヤーを初期化
            self.cursor.execute(
                'DELETE FROM characters where world_id = ?',
                (world_id,)
            )

            # プレイヤー情報を保存
            character_type = 'player'
            x, y, z = self.player.position
            direction_x, direction_y, direction_z = self.player.direction
            self.cursor.execute(
                'INSERT INTO characters(character_type, x, y, z, direction_x, direction_y, direction_z, world_id) '
                'values(?, ?, ?, ? ,?, ?, ?, ?)',
                (character_type, x, y, z, direction_x, direction_y, direction_z, world_id)
            )

            self.db.commit()
            self.save_notification_text['text'] = 'セーブ完了！'
        else:
            self.save_notification_text['text'] = 'ワールド名を入力してください。'

    def get_world_names(self):
        self.connect_db()
        self.create_tables()

        # ワールド名のリストを取得
        self.cursor.execute(
            'SELECT name FROM worlds ORDER BY updated_at DESC'
        )
        world_names = [value[0] for value in self.cursor.fetchall()]

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
        self.cursor.execute('SELECT * FROM blocks WHERE world_id = ?', (world_id,))
        recorded_blocks = self.cursor.fetchall()
        for block in recorded_blocks:
            _, x, y, z, block_id, _ = block
            self.block.add_block(x, y, z, block_id)

        # プレイヤーを更新
        self.cursor.execute(
            'SELECT x, y, z, direction_x, direction_y, direction_z FROM characters WHERE world_id = ? AND character_type = ?',
            (world_id, 'player')
        )
        # print(self.cursor.fetchall())
        x, y, z, direction_x, direction_y, direction_z = self.cursor.fetchall()[0]
        self.player.position = Point3(x, y, z)
        self.player.direction = Vec3(direction_x, direction_y, direction_z)

    def exit_game(self):
        # 終了
        if self.db:
            self.db_cursor.close()
            self.db.close()
        sys.exit()

    def open_server(self):
        pass

    def join_server(self):
        pass
