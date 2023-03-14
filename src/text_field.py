from math import *
from panda3d.core import *
from . import draw_line_between_two_points
from direct.gui.DirectGui import *


class TextField:
    def __init__(self):
        # ConfigVariableBool("ime-aware").setValue(True)
        self.is_open_text_field = False
        input_texture = self.loader.loadTexture('texture/button_press.png')

        # self.bottom_left_text = self.draw_2d_text('bottom_left_text', parent=self.a2dBottomLeft, pos=(0.05, 0.1))
        self.text_field = DirectEntry(text='', scale=.15, command=self.send_text_from_field, initialText='', numLines=1,
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

    def send_text_from_field(self, text):
        if text:
            if text[:5] == 'build':
                print('build')
                build_command = text.split()
                if len(build_command) == 8:
                    _, shape, x, y, z, px, py, pz = build_command
                    x, y, z, px, py, pz = map(float, (x, y, z, px, py, pz))
                    r, g, b = 255, 255, 255
                elif len(build_command) == 11:
                    _, shape, x, y, z, px, py, pz, r, g, b = build_command
                    x, y, z, px, py, pz, r, g, b = map(float, (x, y, z, px, py, pz, r, g, b))
                else:
                    shape = None
                    print('Incorrect format')

                if shape == 'cube':
                    cube = self.loader.loadModel('models/misc/rgbCube')
                    cube.setTransparency(TransparencyAttrib.MAlpha)
                    cube.setScale(x, y, z)
                    cube.setPos(self.area_center + Point3(px, py, pz + z / 2))
                    cube.setColor(*LRGBColor(r, g, b) / 255, 0.5)
                    cube.reparentTo(self.map_node)
                else:
                    print('Incorrect format')
            else:
                self.send_message(text)
            self.text_field.enterText('')
            self.text_field.hide()
            self.is_open_text_field = False
