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
                self.build_shape(text)
            else:
                self.send_message(text)
            self.text_field.enterText('')
            self.text_field.hide()
            self.is_open_text_field = False

    def build_shape(self, text):
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

        if shape in ['cube', 'sphere', 'cylinder', 'corn']:
            if shape == 'cube':
                model_path = 'models/misc/rgbCube'
                sx, sy, sz = x, y, z
                dz = z / 2
            else:
                model_path = f'models/{shape}_uv64'
                sx, sy, sz = x / 2, y / 2, z / 2
                dz = z / 2
            bottom_center_position = self.area_center + Point3(px, py, pz)
            building_node = self.map_node.attachNewNode(PandaNode(text))
            building_node.setPos(bottom_center_position)
            building_node.setTag('height', str(z))
            building_node.setTag('building_id', text)
            building_node.setPythonTag('is_hidden', False)
            model = self.loader.loadModel(model_path)
            model.setTextureOff(1)
            model.setTransparency(TransparencyAttrib.MAlpha)
            model.setScale(sx, sy, sz)
            model.setZ(dz)
            model.setColor(*LRGBColor(r, g, b) / 255, 0.5)
            model.reparentTo(building_node)
            # Create a collision node for this object.
            collision_node = CollisionNode(text)
            # Attach a collision sphere solid to the collision node.
            # collision_node.addSolid(CollisionSphere(0, 0, 0, float(height)))
            collision_node.addSolid(CollisionBox(Point3(0, 0, z / 2), x / 2, y / 2, z / 2))
            # Attach the collision node to the object's model.
            # collision_base_node = cube.attachNewNode(PandaNode(f'collision_{text}'))
            # collision_base_node.setH(degrees(min_angle) + 45)
            building_collision = building_node.attachNewNode(collision_node)
            # Set the object's collision node to render as visible.
            # building_collision.show()

            self.all_buildings.append(building_node)
        else:
            print('Incorrect format')
