import sys
from panda3d.core import *
from . import draw_line_between_two_points


class Window:
    def __init__(self, title, window_title):
        # FPS表示
        # Config.prc -> show-frame-rate-meter #t
        self.setFrameRateMeter(True)

        self.props = WindowProperties()
        self.props.setTitle(window_title)
        self.props.setSize(1200, 800)
        self.win.requestProperties(self.props)
        # self.setBackgroundColor(0, 0, 0)

        # 建物、道路を配置
        self.map_node = self.render.attachNewNode(PandaNode('map_node'))

        for attributes in self.building_attributes_list:
            height = attributes['height']
            if height:
                bldg_id = attributes['building_id']
                base_position = Point3(*attributes['center_position'])

                building_node = self.map_node.attachNewNode(PandaNode(f'building{bldg_id}'))
                building_node.setPos(base_position)
                building_node.setTag('height', str(height))

        self.draw_2d_text(title)

        # plight = PointLight('plight')
        # plight.setColor((0.2, 0.2, 0.2, 1))
        # plnp = self.render.attachNewNode(plight)
        # plnp.setPos(self.area_center)
        # self.render.setLight(plnp)
        #
        # alight = AmbientLight('alight')
        # alight.setColor((0.2, 0.2, 0.2, 1))
        # alnp = self.render.attachNewNode(alight)
        # self.render.setLight(alnp)

        self.accept('escape', self.escape_key)

    def escape_key(self):
        # 終了
        sys.exit()