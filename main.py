from direct.showbase.ShowBase import ShowBase
from src import (
    Database, Sound, DrawText, Window, Building, KeyMap, Camera, Axis, CelestialSphere, Ground, WireFrame, SolidModel,
    Players, Mobs
)
from network import Message, Connect
import constants


class OpenWorld(ShowBase, Database, DrawText, Window, KeyMap, Camera, Players, Mobs, Message, Connect):
    def __init__(self, window_title, settings, has_celestial, has_wire_frame, has_solid_model,
                 has_player, has_mobs, character_color):
        self.settings = settings
        self.character_color = character_color
        # PCの能力により調整
        self.building_tolerance = 200  # 建物を描画する範囲
        self.road_tolerance = 400  # 道路を描画する範囲
        self.min_surface_height = 10  # 壁を描画する最低の高さ
        self.celestial_radius = 500  # 天球の半径
        self.max_camera_radius_to_render_surface = 2000  # 面を表示する最大のカメラ半径
        self.interval_drawing_pillar = 10  # 縦の線を何本おきに描画するか

        ShowBase.__init__(self)
        Database.__init__(self)
        Sound.__init__(self)
        DrawText.__init__(self)
        Window.__init__(self, window_title)
        Building.__init__(self)
        KeyMap.__init__(self)
        Camera.__init__(self)
        Axis.__init__(self)
        Ground.__init__(self)
        if has_celestial:
            # self.sky_texture = self.loader.loadTexture('models/maps/sky_1024x1024.png')
            self.sky_texture = self.loader.loadTexture('models/maps/cloud_sky_1024x1024.png')
            # self.sky_texture = self.loader.loadTexture('models/maps/star_sky_1024x1024.png')
            CelestialSphere.__init__(self)
        if has_wire_frame:
            WireFrame.__init__(self)
        if has_solid_model:
            SolidModel.__init__(self)
        if has_player:
            Players.__init__(self)
        if has_mobs:
            Mobs.__init__(self, constants.mob_dic_list)

        # マルチプレイ
        Message.__init__(self)
        # F10 サーバー開始 / F11 クライエントとして接続
        Connect.__init__(self)


if __name__ == '__main__':
    # メッシュコード
    # https://www.mlit.go.jp/plateau/learning/tpc03-1/#p3_2_4

    # 座標系
    # https://www.mlit.go.jp/plateau/learning/tpc03-4/

    # さいたスーパーアリーナ
    plateau_settings = {
        'bldg_mesh1': '5339',
        'bldg_mesh2': '65',
        'bldg_mesh3_list': ['70'],
        # 'bldg_mesh3_list': ['60', '61', '70', '71'],
        'road_mesh3_list': [''],
        # 日本測地系2011 における経緯度座標系と東京湾平均海面を基準とする標高の複合座標参照系
        'bldg_crs_from': '6697',
        # 日本測地系2011 における経緯度座標系
        'road_crs_from': '6668',
        # 平面直角座標系
        'crs_to': '6677',  # 関東圏（9系）
    }

    app = OpenWorld(
        window_title='PLATEAU World',  # ウインドウタイトル
        settings=plateau_settings,  # PLATEAUデータ設定
        has_celestial=False,  # 天球を表示
        has_wire_frame=True,  # ワイヤーフレームを表示
        has_solid_model=True,  # 面を表示
        has_player=False,  # プレイヤーを表示
        has_mobs=False,  # モブを表示
        character_color=(1, 1, 0, 1),  # キャラクターの色を変更
    )
    app.run()
