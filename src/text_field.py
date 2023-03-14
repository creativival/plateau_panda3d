from math import *
from panda3d.core import *
from . import draw_line_between_two_points
from direct.gui.DirectGui import *


class TextField:
    def __init__(self):
        # ConfigVariableBool("ime-aware").setValue(True)
        self.is_open_text_field = False
        input_texture = self.loader.loadTexture('texture/button_press.png')
        self.messages = []
        self.timers = []

        # self.bottom_left_text = self.draw_2d_text('bottom_left_text', parent=self.a2dBottomLeft, pos=(0.05, 0.1))
        self.text_field = DirectEntry(text='', scale=.15, command=self.send_chat, initialText='', numLines=1,
                                      focus=1, frameTexture=input_texture, parent=self.a2dBottomLeft, width=25,
                                      text_fg=(1, 0, 0, 1), pos=(0.1, 0, 0.1), text_scale=0.75, entryFont=self.font)
        self.text_field.hide()

        self.accept('tab', self.toggle_text_field)

    def toggle_text_field(self):
        if self.text_field.isHidden():
            self.text_field.show()
            self.is_open_text_field = True
            self.text_field.setFocus()
        else:
            self.text_field.hide()
            self.is_open_text_field = False
