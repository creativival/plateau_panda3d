import sys
from panda3d.core import *
from . import draw_line_between_two_points


class Window:
    def __init__(self, window_title):
        # FPS表示
        # Config.prc -> show-frame-rate-meter #t
        self.setFrameRateMeter(True)

        self.props = WindowProperties()
        self.props.setTitle(window_title)
        self.props.setSize(1200, 800)
        self.win.requestProperties(self.props)
        # self.setBackgroundColor(0, 0, 0)

        self.is_open_chat_field = False

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
        if self.db:
            self.db_cursor.close()
            self.db.close()
        sys.exit()