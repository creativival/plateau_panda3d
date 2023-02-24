from direct.showbase.ShowBase import ShowBase
from src import (
    ReadBuilding, DrawText, Window, Camera, Axis, CelestialSphere, Ground, WireFrame, SolidModel, Player, Mobs
)
import constants


class OpenWorld(ShowBase, DrawText, Window, Camera, Player, Mobs):
    def __init__(self, title, window_title, plateau_settings, has_celestial, has_wire_frame, has_solid_model, has_player, has_mobs):
        # PCの能力により調整
        self.building_tolerance = 200  # 建物を描画する範囲
        self.road_tolerance = 400  # 道路を描画する範囲
        self.min_surface_height = 100  # 壁を描画する最低の高さ
        self.celestial_radius = 2000  # 天球の半径
        self.max_camera_radius_to_render_surface = 1000  # 面を表示する最大のカメラ半径
        self.interval_drawing_pillar = 2  # 縦の線を何本おきに描画するか

        ShowBase.__init__(self)
        ReadBuilding.__init__(self, plateau_settings)
        DrawText.__init__(self)
        Window.__init__(self, title, window_title)
        Camera.__init__(self)
        Axis.__init__(self)
        Ground.__init__(self)
        if has_celestial:
            # self.sky_texture = self.loader.loadTexture('models/maps/sky_1024x512.jpg')
            # self.sky_texture = self.loader.loadTexture('models/maps/cloud_1024x512.jpg')
            self.sky_texture = self.loader.loadTexture('models/maps/star_sky_1024x512.jpg')
            CelestialSphere.__init__(self)
        if has_wire_frame:
            WireFrame.__init__(self)
        if has_solid_model:
            SolidModel.__init__(self)
        if has_player:
            Player.__init__(self)
        if has_mobs:
            Mobs.__init__(self, constants.mob_dic_list)


if __name__ == '__main__':
    # メッシュコード
    # https://www.mlit.go.jp/plateau/learning/tpc03-1/#p3_2_4

    # 座標系
    # https://www.mlit.go.jp/plateau/learning/tpc03-4/

    # # 札幌大通郵便局
    # plateau_settings = {
    #     'bldg_mesh1': '6441',
    #     'bldg_mesh2': '42',
    #     'bldg_mesh3_list': ['78'],
    #     'road_mesh3_list': ['78'],
    #     # 日本測地系2011 における経緯度座標系と東京湾平均海面を基準とする標高の複合座標参照系
    #     'bldg_crs_from': '6697',
    #     # 日本測地系2011 における経緯度座標系
    #     'road_crs_from': '6668',
    #     # 平面直角座標系
    #     'crs_to': '6677',  # 関東圏（9系）
    # }
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
    # # 大宮駅
    # plateau_settings = {
    #     'bldg_mesh1': '5339',
    #     'bldg_mesh2': '64',
    #     'bldg_mesh3_list': ['89'],
    #     'road_mesh3_list': [''],
    #     # 日本測地系2011 における経緯度座標系と東京湾平均海面を基準とする標高の複合座標参照系
    #     'bldg_crs_from': '6697',
    #     # 日本測地系2011 における経緯度座標系
    #     'road_crs_from': '6668',
    #     # 平面直角座標系
    #     'crs_to': '6677',  # 関東圏（9系）
    # }
    # # 渋谷駅
    # plateau_settings = {
    #     'bldg_mesh1': '5339',
    #     'bldg_mesh2': '35',
    #     'bldg_mesh3_list': ['85', '86', '95', '96'],
    #     # 'bldg_mesh3_list': ['85'],
    #     'road_mesh3_list': [''],
    #     # 日本測地系2011 における経緯度座標系と東京湾平均海面を基準とする標高の複合座標参照系
    #     'bldg_crs_from': '6697_2',
    #     # 日本測地系2011 における経緯度座標系
    #     'road_crs_from': '6697',
    #     # 平面直角座標系
    #     'crs_to': '6677',  # 関東圏（9系）
    # }

    # app = OpenWorld(
    #     title='Wire Frame',
    #     window_title='PLATEAU World',
    #     plateau_settings=plateau_settings,
    #     has_celestial=False,
    #     has_wire_frame=True,
    #     has_solid_model=False,
    #     has_player=False,
    #     has_mobs=False,
    # )

    # app = OpenWorld(
    #     title='Solid Model',
    #     window_title='PLATEAU World',
    #     plateau_settings=plateau_settings,
    #     has_celestial=False,
    #     has_wire_frame=True,
    #     has_solid_model=True,
    #     has_player=False,
    #     has_mobs=False,
    # )

    app = OpenWorld(
        title='Map only',  # タイトル
        window_title='PLATEAU World',  # ウインドウタイトル
        plateau_settings=plateau_settings,  # PLATEAUデータ設定
        has_celestial=False,  # 天球を表示
        has_wire_frame=True,  # ワイヤーフレームを表示
        has_solid_model=True,  # 面を表示
        has_player=False, # プレイヤーを表示
        has_mobs=False,  # モブを表示
    )
    app.run()
