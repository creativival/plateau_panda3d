import platform
from direct.gui.DirectGui import OnscreenText
from panda3d.core import *


class DrawText:
    def __init__(self):
        # font
        pf = platform.system()
        if pf == 'Windows':
            # Windows
            self.font = self.loader.loadFont('/c/Windows/Fonts/msgothic.ttc')
        elif pf == 'Darwin':
            # Mac
            self.font = self.loader.loadFont('/System/Library/Fonts/Hiragino Sans GB.ttc')
        elif pf == 'Linux':
            # Ubuntu18.04
            self.font = self.loader.loadFont('/usr/share/fonts/opentype/note/NotoSansCJK-Bold.ttc')
        self.text_parent = self.a2dTopLeft

    def draw_2d_text(self, text, parent=None, scale=0.07, pos=(0.05, -0.1), align=TextNode.ALeft,
                     fg=(1, 1, 0, 1), bg=(0, 0, 0, 0.1), mayChange=True, wordwrap=40):
        if parent is None:
            parent = self.text_parent
        return OnscreenText(text=text,
                     parent=parent,
                     font=self.font,
                     scale=scale,
                     pos=pos,
                     align=align,
                     fg=fg,
                     bg=bg,
                     mayChange=mayChange,
                     wordwrap=wordwrap
                     )

    def draw_3d_text(self, text, position, parent=None, heading=0, pitch=0, fg=(1, 1, 1, 1), bg=(1, 1, 1, 0), frame=(1, 1, 1, 1),
                     scale=5, node_name=''):
        if parent is None:
            parent = self.render
        text_node = parent.attachNewNode(PandaNode(node_name))
        text_node.setPos(position)
        text_node.setHpr(heading, pitch, 0)
        text_node.setPythonTag('position', position)
        # print(text, phi, theta, heading, pitch)
        return OnscreenText(text=text,
                     parent=text_node,
                     font=self.font,
                     fg=fg,
                     frame=frame,
                     bg=bg,
                     pos=Vec2(0, 0.5) * scale,
                     scale=scale)
