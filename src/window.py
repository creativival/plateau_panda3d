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
        self.is_paused_player = False

        self.top_left_text = self.draw_2d_text('', parent=self.a2dTopLeft)
        self.top_center_text = self.draw_2d_text('', parent=self.a2dTopCenter, pos=(0, -0.1),
                                                align=TextNode.ACenter)
        self.top_right_text = self.draw_2d_text('', parent=self.a2dTopRight, pos=(-0.05, -0.1),
                                                align=TextNode.ARight)

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
        self.accept('backspace', self.backspace_key)

    def escape_key(self):
        if self.is_paused_player:
            self.is_paused_player = False
            self.top_center_text.setText('')
        else:
            self.is_paused_player = True
            self.top_center_text.setText('Pause')

    def backspace_key(self):
        # 終了
        if self.db:
            self.db_cursor.close()
            self.db.close()
        sys.exit()
