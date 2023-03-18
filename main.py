from direct.showbase.ShowBase import ShowBase
from src import (
    Database, Sound, DrawText, Window, TextField, Menu,
    Building, Collision, KeyMap, Camera, Axis, CelestialSphere,
    Ground, WireFrame, SolidModel, Players, Mobs
)
from network import Message, Connect
import constants


class OpenWorld(ShowBase, Database, DrawText, Window, Message, TextField, Menu, Collision, KeyMap, Camera, Players,
                Mobs, Connect):
    def __init__(self, window_title, settings, sky_texture, has_wire_frame, has_solid_model,
                 has_player, has_mobs, character_color):
        self.settings = settings
        self.character_color = character_color
        # PCの能力により調整
        self.building_tolerance = 400  # 建物を描画する範囲
        self.road_tolerance = 400  # 道路を描画する範囲
        self.min_surface_height = 0  # 壁を描画する最低の高さ
        self.celestial_radius = 1000  # 天球の半径
        self.max_camera_radius_to_render_surface = 1000  # 背の低いビルを非表示にする最大のカメラ半径
        self.max_building_height_to_hide = 10  # 非表示にする背の低いビルの最大高さ
        self.interval_drawing_pillar = 5  # 縦の線を何本おきに描画するか

        ShowBase.__init__(self)
        Database.__init__(self)
        Sound.__init__(self)
        DrawText.__init__(self)
        Connect.__init__(self)
        Window.__init__(self, window_title)
        Message.__init__(self)
        TextField.__init__(self)
        Menu.__init__(self)
        Building.__init__(self)
        Collision.__init__(self)
        KeyMap.__init__(self)
        Camera.__init__(self)
        Axis.__init__(self)
        Ground.__init__(self)
        if sky_texture:
            CelestialSphere.__init__(self, sky_texture)
        if has_wire_frame:
            WireFrame.__init__(self)
        if has_solid_model:
            SolidModel.__init__(self)
        if has_player:
            Players.__init__(self)
        if has_mobs:
            Mobs.__init__(self, constants.mob_dic_list)


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
        window_title='PLATEAU World',
        settings=plateau_settings,
        # sky_texture='sky_1024x1024.png',
        sky_texture='cloud_sky_1024x1024.png',
        # sky_texture='star_sky_1024x1024.png',
        has_wire_frame=True,
        has_solid_model=True,
        has_player=True,
        has_mobs=True,
        character_color=(1, 1, 0, 1),
    )
    app.run()
