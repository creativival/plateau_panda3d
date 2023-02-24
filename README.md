# PLATEAU Panda3D

PythonのライブラリPanda3Dを使って、日本全国の3D都市モデルの整備、活用、オープンデータ化プロジェクト PLATEAUのモデルを3Dゲームに変換します。

![image_top](https://github.com/creativival/plateau_panda3d/blob/main/image/plateau_panda3d_image_top.png)

## 開発環境

MacBook Air (M1)
PyCharm Professional
Python 3.9 (venv)
Panda3D 1.10.13
PyProj

## ライブラリのインストール

```text
% pip install panda3d
% pip install pyproj
```

## ディレクトリ構成

```text
root/
 ├ data/                     PLATEAUのオープンソースデータ
 │     ├ 53396570_bldg_6697_op.gml  # ビルのデータ
 │     ├ 533965_tran_6668_op.gml  # 道路のデータ
 │
 ├ models/                      3Dモデル
 │     ├ maps                 テクスチャー
 │     │     ├ cat.png  # キャラクター
 │     │     ├ sky_1024x512.png  # 天球の内面
 │     │
 │     ├ egg_surface.egg  # キャラクター
 │     ├ sphere_uv_reverse.egg.egg  # 天球（テクスチャー反転）
 │
 ├ output/                 アウトプット
 ├ tmp/                    一時ファイル
 ├ src/                     パッケージ
 │     ├ __init__.py  # 初期化モジュール
 │     ├ axis.py  # 座標軸表示
 │     ├ camera.py  # カメラ
 │     ├ celestial_sphere.py  # 天球
 │     ├ draw_text.py  # テキスト表示
 │     ├ geometry.py  # ジオメトリ
 │     ├ ground.py  # グラウンド
 │     ├ mod.py  # モブ
 │     ├ mobs.py  # モブを管理
 │     ├ plateau_util.py  # データ変換
 │     ├ player.py  # プレイヤー
 │     ├ read_building.py  # データ読み込み
 │     ├ solid_model.py  # 建築物の面を作成
 │     ├ vector.py  # ベクトル変換
 │     ├ window.py  # ウインドウ
 │     ├ wire_frame.py  # 建築物の線を作成
 │     ├
 │
 ├ Config.prc  # Panda3Dの設定
 ├ constants.js  # 定数
 ├ main.js  # 起動ファイル
 ├ README.md  # リードミー
```

## 使い方

PLATEAU Webサイト（参照）

[TOPIC 3｜3D都市モデルデータの基本[1/4]｜3D都市モデルの入手方法とデータ形式](https://www.mlit.go.jp/plateau/learning/tpc03-1/)

### 例　さいたまスーパーアリーナ


[地図で見る統計（jSTAT MAP）](https://jstatmap.e-stat.go.jp/trialstart.html)

ログインしないで始める

![image1](https://github.com/creativival/plateau_panda3d/blob/main/image/plateau_panda3d_image1.png)

「さいたまスーパーアリーナ」で検索し、メッシュ番号「53396570」を得る。


[3D都市モデル（Project PLATEAU）ポータルサイト](http://test.geospatial.jp/ckan/dataset/plateau)


![image1](https://github.com/creativival/plateau_panda3d/blob/main/image/plateau_panda3d_image2.png)

さいたま市のデータをダウンロード

```text
root/
 ├ data/                     PLATEAUのオープンソースデータ
 │     ├ 53396570_bldg_6697_op.gml  # ビルのデータ
 │     ├ 533965_tran_6668_op.gml  # 道路のデータ
 │
```

dataフォルダーに必要なオープンシースデータをコピー

以上で、準備は完了です。

```main.py
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
```

main.py（起動ファイル）の設定を変更します。

plateau_settingsに、先ほどダウンロードしたオープンデータを読み込む設定を行います。  
メッシュ番号を「bldg_mesh1」「bldg_mesh2」「bldg_mesh3」に分割して、記載します「bldg_mesh3」は、リスト形式になっており、広い範囲を選択するときは、複数の番号を入れることが可能です。 
座標参照系「bldg_crs_frm」「road_crs_from」は、ファイル名の最後に記載してある数字を入力します。  

![平面直角座標系](https://www.mlit.go.jp/plateau/uploads/2022/11/zu03-25.png)

PLATEAY Webサイトより引用（https://www.mlit.go.jp/plateau/learning/tpc03-4/）

平面直角座標系「crs_to」は、誤差を少なくするために全国を9つのエリアに分割しているので、さいたま市が含まれる「9系（6677）」を入力します。

```text
% python main.py
```

起動ファイルを実行します。初回起動時は、データ変換のため時間がかかります。そのまま変換が終了するまで、お待ちください。  
2度目の起動からは、変換後データを読み込みますので、起動は早くなります。


![PLATEAU Panda3D](https://github.com/creativival/plateau_panda3d/blob/main/image/plateau_panda3d_image3.png)

## 操作方法

遠景カメラビュー

```text
WASDで平行移動
矢印キーで回転
マウスホイールで遠近
```

プレイヤービュー

```text
Tでカメラの切り替え
WASDで平行移動
マウスで回転
```

## パフォーマンス調整

本プログラムは、多数のオブジェクトを画面に表示するため、パソコンに大きな負荷がかかります。  
FPSは画面右上に表示されているので、その数字を見て、パフォーマンスを調整してください。  

```main.py
        # PCの能力により調整
        self.building_tolerance = 200  # 建物を描画する範囲
        self.road_tolerance = 400  # 道路を描画する範囲
        self.min_surface_height = 100  # 壁を描画する最低の高さ
        self.celestial_radius = 2000  # 天球の半径
        self.max_camera_radius_to_render_surface = 1000  # 面を表示する最大のカメラ半径
        self.interval_drawing_pillar = 2  # 縦の線を何本おきに描画するか
```

main.pyの設定項目を編集して、パソコンの描画範囲を調整できます。

## 開発上の注意

- 開発は基本developブランチでおこなう。大きな変更があるときはfeature/\*ブランチを切る。
- 本番環境にデプロイされるのはmasterブランチ。リリースしたいときはdevelopでの変更をmasterにmergeする。
- 起動ファイルは、main.pyをコピーしたdev_main.pyで各自の設定により行う。dev_main.pyをgitに含めない。

## ライセンス

[MIT](https://github.com/creativival/plateau_panda3d/blob/master/LICENSE.txt)





