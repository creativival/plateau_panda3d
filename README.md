# PLATEAU Panda3D

PythonのライブラリPanda3Dを使って、日本全国の3D都市モデルの整備、活用、オープンデータ化プロジェクト PLATEAUのモデルを3Dゲームに変換します。

https://user-images.githubusercontent.com/33368327/221376187-bf98d0f3-9b3e-4954-914f-3766a53690f2.mp4


## 開発環境

- MacBook Air (M1)
- PyCharm Professional
- Python 3.9 (venv)
- Panda3D 1.10.13
- PyProj 3.4.1
- sqlite3 3.39.5（開発環境にインストールしておく）

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
 │     │     ├ sky_1024x1024.png  # 天球の内面
 │     │
 │     ├ egg_surface.egg  # キャラクター
 │     ├ sphere_uv_reverse.egg  # 天球（テクスチャー反転）
 │
 ├ music/                 音源
 ├ network/                     マルチプレイ
 │     ├ __init__.py  # 初期化モジュール
 │     ├ client.py  # ネットワーク（クライエント）
 │     ├ client_protocol.py  # プロトコル（クライエント）
 │     ├ connect.py  # サーバー/クライエント接続
 │     ├ message.py  # メッセージ送受信
 │     ├ net_common.py  # ネットワーク
 │     ├ protocol.py  # プロトコル
 │     ├ server.py  # ネットワーク（サーバー）
 │     ├ server_protocol.py  # プロトコル（サーバー）
 │     ├
 │
 ├ output/                 アウトプット（sqlite3データベースファイル）
 ├ tmp/                    一時ファイル
 ├ src/                     パッケージ
 │     ├ __init__.py  # 初期化モジュール
 │     ├ axis.py  # 座標軸
 │     ├ building.py  # ビルディング
 │     ├ camera.py  # カメラ
 │     ├ celestial_sphere.py  # 天球
 │     ├ database.py  # データベース（sqlite3）
 │     ├ draw_text.py  # テキスト表示
 │     ├ geometry_util.py  # ジオメトリ
 │     ├ ground.py  # グラウンド
 │     ├ mod.py  # モブ
 │     ├ mobs.py  # モブを管理
 │     ├ player.py  # プレイヤー
 │     ├ players.py  # プレイヤー管理
 │     ├ pypro_util.py  # 座標変換
 │     ├ solid_model.py  # 建築物の面を作成
 │     ├ sound.py  # サウンド
 │     ├ vector.py  # ベクトル変換
 │     ├ window.py  # ウインドウ
 │     ├ wire_frame.py  # 建築物の線を作成
 │     ├
 │
 ├ texture/                     テクスチャー
 ├ Config.prc  # Panda3Dの設定（FPSを表示）
 ├ constants.js  # 定数
 ├ dev_main.js  # 開発用の起動ファイル（main.pyをコピーして使用）
 ├ main.js  # 起動ファイル
 ├ README.md  # リードミー
```

## 使い方

PLATEAU Webサイトの以下のページを参照してください。表示したい都市データを探す方法が書かれています。

[TOPIC 3｜3D都市モデルデータの基本[1/4]｜3D都市モデルの入手方法とデータ形式](https://www.mlit.go.jp/plateau/learning/tpc03-1/)

### 例　さいたまスーパーアリーナ

具体例として、さいたまスーパーアリーナを表示する方法を説明します。

メッシュコードを調べます。

[地図で見る統計（jSTAT MAP）](https://jstatmap.e-stat.go.jp/trialstart.html)

「ログインしないで始める」をクリックする。

![image2](https://github.com/creativival/plateau_panda3d/blob/main/image/plateau_panda3d_image2.png)

「さいたまスーパーアリーナ」で検索し、メッシュコード「53396570」を得る。

次に、CityGML形式のデータをダウンロードします。


[3D都市モデル（Project PLATEAU）ポータルサイト](http://test.geospatial.jp/ckan/dataset/plateau)


![image1](https://github.com/creativival/plateau_panda3d/blob/main/image/plateau_panda3d_image1.png)

さいたま市のデータ（CityGML）をダウンロードします。

データを解凍します。「bldg」「trans」ファルダーに含まれるビルと道路のデータのうち、メッシュコードと同じ名前のファイルを選びます。

```text
root/
 ├ data/                     PLATEAUのオープンソースデータ
 │     ├ 53396570_bldg_6697_op.gml  # ビルのデータ
 │     ├ 533965_tran_6668_op.gml  # 道路のデータ
 │
```

dataフォルダーに必要なCityGMLファイルをコピーします。

以上で、データの準備は完了です。

次に、ゲームの起動方法説明します。起動ファイル（main.py）を開いてください。

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
        settings=plateau_settings,  # PLATEAUデータ設定
        has_celestial=False,  # 天球を表示
        has_wire_frame=True,  # ワイヤーフレームを表示
        has_solid_model=True,  # 面を表示
        has_player=False, # プレイヤーを表示
        has_mobs=False,  # モブを表示
        character_color=(1, 1, 0, 1),  # キャラクターの色を変更
    )
    app.run()
```

main.py（起動ファイル）の設定を変更します。

plateau_settingsに、先ほどダウンロードしたCityGMLファイルを読み込む設定を行います。  
メッシュコードを「bldg_mesh1」「bldg_mesh2」「bldg_mesh3」に分割して、記載します「bldg_mesh3」は、リスト形式になっており、広い範囲を選択するときは、複数の番号を入れることが可能です。  
座標参照系「bldg_crs_from」「road_crs_from」は、ファイル名の最後に記載してある数字を入力します。（6697、6697_2などは立体、6688は平面データ）  

![平面直角座標系](https://www.mlit.go.jp/plateau/uploads/2022/11/zu03-25.png)

<table><thead><tr><th>系番号</th><th>EPSG<br>コード</th><th>原点の位置(経度)</th><th>原点の位置(緯度)</th><th>適用区域</th></tr></thead>
<tbody>
  <tr><td>1</td><td>6669</td><td>129度30分0秒0000</td><td>33度0分0秒0000</td><td>長崎県すべてと鹿児島県の一部</td></tr>
  <tr><td>2</td><td>6670</td><td>131度 0分0秒0000</td><td>33度0分0秒0000</td><td>福岡県　佐賀県　熊本県　大分県　宮崎県　鹿児島県の一部</td></tr>
  <tr><td>3</td><td>6671</td><td>132度10分0秒0000</td><td>36度0分0秒0000</td><td>山口県　島根県　広島県</td></tr>
  <tr><td colspan="5">...</td></tr>
  <tr><td>9</td><td>6677</td><td>139度50分0秒0000</td><td>36度0分0秒0000</td><td>東京都（島しょ部を除く）福島県　栃木県　茨城県　埼玉県 千葉県　群馬県　神奈川県</td></tr>
  <tr><td colspan="5">...</td></tr>
</tbody></table>

PLATEAU Webサイトより引用（https://www.mlit.go.jp/plateau/learning/tpc03-4/）

平面直角座標系は、誤差を少なくするために全国を9つのエリアに分割されています。  
「crs_to」は、さいたま市が含まれる「9系（6677）」を入力します。  

```text
        has_celestial=False,  # 天球を表示
        has_wire_frame=True,  # ワイヤーフレームを表示
        has_solid_model=True,  # 面を表示
        has_player=False, # プレイヤーを表示
        has_mobs=False,  # モブを表示
```

インスタンス化のさい、引数をブール値で設定すると、オブジェクトを表示/非表示を変更できます。  
FPSが低いときはパソコンの負荷を下げるため、has_celestial、has_solid_modelは、「False」推奨です。

これで、起動ファイルの設定は完了です。ゲームを実行しましょう。

```text
% python main.py
```

ターミナルから起動ファイルを実行します。初回起動時は、データ変換のため時間がかかります。そのまま変換が終了するまで、お待ちください。（SQlite3データベースに全てのデータを登録するため、都心部などビルが多い地域では数時間かかります。）  
2度目の起動からは、データベースを読み込みますので、起動は早くなります。

![PLATEAU Panda3D](https://github.com/creativival/plateau_panda3d/blob/main/image/plateau_panda3d_image3.png)

## 設定例

```text
    # 札幌大通郵便局
    plateau_settings = {
        'bldg_mesh1': '6441',
        'bldg_mesh2': '42',
        'bldg_mesh3_list': ['78'],
        'road_mesh3_list': ['78'],
        # 日本測地系2011 における経緯度座標系と東京湾平均海面を基準とする標高の複合座標参照系
        'bldg_crs_from': '6697',
        # 日本測地系2011 における経緯度座標系
        'road_crs_from': '6668',
        # 平面直角座標系
        'crs_to': '6677',  # 関東圏（9系）
    }
```

![PLATEAU Panda3D](https://github.com/creativival/plateau_panda3d/blob/main/image/plateau_panda3d_image4.png)

```text
    # 渋谷駅
    plateau_settings = {
        'bldg_mesh1': '5339',
        'bldg_mesh2': '35',
        'bldg_mesh3_list': ['85', '86', '95', '96'],  # 4つのメッシュにまたがっているので、すべて指定する
        # 'bldg_mesh3_list': ['85'],
        'road_mesh3_list': [''],
        # 日本測地系2011 における経緯度座標系と東京湾平均海面を基準とする標高の複合座標参照系
        'bldg_crs_from': '6697_2',
        # 日本測地系2011 における経緯度座標系
        'road_crs_from': '6697',
        # 平面直角座標系
        'crs_to': '6677',  # 関東圏（9系）
    }
```

![PLATEAU Panda3D](https://github.com/creativival/plateau_panda3d/blob/main/image/plateau_panda3d_image5.png)

## 天球

巨大なドーム（天球）の内面に画像を貼り付けて、空を表現できます。  
画像サイズは1024x1024。上半分に空の画像、下はrgb(0,1,0)の単色。空の画像は左右の鏡面対象にすると継ぎ目が目立たない。  

```text
        # main.py
        if has_celestial:
            self.sky_texture = self.loader.loadTexture('models/maps/sky_1024x1024.png')
            # self.sky_texture = self.loader.loadTexture('models/maps/cloud_sky_1024x1024.png')
            # self.sky_texture = self.loader.loadTexture('models/maps/star_sky_1024x1024.png')
            CelestialSphere.__init__(self)
```

main.pyのインスタンス変数sky_textureを入れ替えることで、様々な空を表現できます。

![PLATEAU Panda3D](https://github.com/creativival/plateau_panda3d/blob/main/image/plateau_panda3d_image6.png)

快晴

![PLATEAU Panda3D](https://github.com/creativival/plateau_panda3d/blob/main/image/plateau_panda3d_image7.png)

星空

![PLATEAU Panda3D](https://github.com/creativival/plateau_panda3d/blob/main/image/plateau_panda3d_image8.png)

雲空

## 操作方法

基本操作

```text
Escape: ゲームをポーズ
Backspace: ゲームを終了
```

遠景カメラビュー

```text
WASDで平行移動
矢印キーで回転
マウスホイールで遠近
```

プレイヤービュー

```text
F5でカメラの切り替え
WASDで平行移動
マウスで回転
スペースでジャンプ
```

## キャラクター

数字キー（1 - 9）で表情を変えて、エモーションを表現できます。  
色は、インスタンス化の引数character_colorにより設定できます。  
移動時に耳が動くモーションを追加しました。  

![PLATEAU Panda3D](https://github.com/creativival/plateau_panda3d/blob/main/image/plateau_panda3d_image9.png)

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

## マルチプレイヤー（Beta）

マルチプレイが可能です（Betaバージョン）。
設定は constants.pyで行います。  
同じパソコン　IP_ADDRESS = 'localhost'  
同じLAN内　IP_ADDRESS= '192.169.xx.xx'　（あらかじめ、同じ都市データをデータベースに保存しておく）  

![PLATEAU Panda3D](https://github.com/creativival/plateau_panda3d/blob/main/image/plateau_panda3d_image10.png)

```text
F10でサーバーを開く
F11でクライエントとして接続
Hで「Hello!」メッセージを送信
TABでチャットフィルドを開く/閉じる/エンターで送信
プレイヤーの位置、向き、表情は同期される
```

## 開発上の注意

- 開発は基本developブランチでおこなう。大きな変更があるときはfeature/\*ブランチを切る。
- 本番環境にデプロイされるのはmasterブランチ。リリースしたいときはdevelopでの変更をmasterにmergeする。
- 起動ファイルは、main.pyをコピーしたdev_main.pyで各自の設定により行う。dev_main.pyをgitに含めない。

## サウンド

GarageBandで簡単な効果音を作成し、BGMとして鳴らしています。  
音源を提供してくださる方がいらっしゃいましたら、大歓迎です。

## ライセンス

[MIT](https://github.com/creativival/plateau_panda3d/blob/master/LICENSE)





