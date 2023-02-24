# PLATEAU Panda3D

PythonのライブラリPanda3Dを使って、日本全国の3D都市モデルの整備、活用、オープンデータ化プロジェクト PLATEAUのモデルを3Dゲームに変換します。

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

![image1](https://github.com/creativival/plateau_panda3d/image/plateau_panda3d_image1.png)

「さいたまスーパーアリーナ」で検索し、「53396570」を得る。


[3D都市モデル（Project PLATEAU）ポータルサイト](http://test.geospatial.jp/ckan/dataset/plateau)


![image1](https://github.com/creativival/plateau_panda3d/image/plateau_panda3d_image1.png)

さいたま市のデータをダウンロード






