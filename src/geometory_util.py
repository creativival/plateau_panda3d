from math import *
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import OnscreenText


def draw_line_between_two_points(position1, position2, line_color, parent, thickness=1, node_name=''):
    line_segs = LineSegs()
    line_segs.setColor(*line_color)
    line_segs.moveTo(position1)
    line_segs.drawTo(position2)
    line_segs.setThickness(thickness)
    node = line_segs.create(True)
    np = NodePath(node)
    np.setTransparency(TransparencyAttrib.MAlpha)
    np.reparentTo(parent)
    if node_name:
        np.setName(node_name)


def draw_triangles(vertices, colors, parent, position=None, direction=None, node_name=''):
    geom_format = GeomVertexFormat.getV3c4()
    geom_vertex_data = GeomVertexData("box", geom_format, Geom.UHStatic)
    vertex_writer = GeomVertexWriter(geom_vertex_data, "vertex")
    color_writer = GeomVertexWriter(geom_vertex_data, "color")

    for pos, color in zip(vertices, colors):
        vertex_writer.addData3f(pos)
        color_writer.addData4f(color)

    geom_triangles = GeomTriangles(Geom.UHStatic)
    for i in range(len(vertices) - 2):
        v1 = 0
        v2 = i + 1
        v3 = i + 2
        geom_triangles.addVertices(v1, v2, v3)
        geom_triangles.closePrimitive()

    geom = Geom(geom_vertex_data)
    geom.addPrimitive(geom_triangles)

    geom_node = GeomNode('geom_node')
    # 右回りの面しか描画されない
    if direction == 'both':
        geom_node.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullNone))  # 両面を表示
    elif direction == 'reverse':
        geom_node.setAttrib(CullFaceAttrib.makeReverse())  # 両面を表示
    geom_node.addGeom(geom)
    node = parent.attachNewNode(geom_node)
    node.setTransparency(TransparencyAttrib.MAlpha)
    if node_name:
        node.setName(node_name)
    if position:
        node.setPos(position)


if __name__ == '__main__':
    base = ShowBase()
    font = base.loader.loadFont("cmr12.egg")

    base.props = WindowProperties()
    base.props.setTitle('Gem')
    base.props.setSize(1200, 800)
    base.win.requestProperties(base.props)
    base.setBackgroundColor(0, 0, 0)

    vertices = [Vec3(1, 0, 1), Vec3(-1, 0, 1), Vec3(-1, 0, -1), Vec3(1, 0, -1),  Vec3(1.2, 0, 0)]
    colors = [Vec4(1, 0, 0, 1), Vec4(0, 1, 0, 1), Vec4(0, 0, 1, 1), Vec4(1, 0, 1, 1), Vec4(1, 1, 0, 1)]

    # format = GeomVertexFormat.getV3c4()
    # geomData = GeomVertexData("box", format, Geom.UHStatic)
    # vertexWriter = GeomVertexWriter(geomData, "vertex")
    # colorWriter = GeomVertexWriter(geomData, "color")
    #
    # for pos, color in zip(vertices, colors):
    #     print(pos, color)
    #     vertexWriter.addData3f(pos)
    #     colorWriter.addData4f(color)
    #
    # triangles = GeomTriangles(Geom.UHStatic)
    # triangles.addVertices(0, 1, 2)
    # triangles.closePrimitive()
    # triangles.addVertices(2, 3, 0)
    # triangles.closePrimitive()
    #
    # geom = Geom(geomData)
    # geom.addPrimitive(triangles)
    # gem_node = GeomNode("box")
    # gem_node.addGeom(geom)

    gem_node = draw_triangles(vertices, colors)
    box = base.render.attachNewNode(gem_node)

    OnscreenText(text="0",
                 fg=Vec4(1, 1, 1, 1),
                 bg=Vec4(0, 0, 0, 1),
                 pos=Vec2(0.85, 0.75),
                 scale=0.2,
                 font=font)

    OnscreenText(text="1",
                 fg=Vec4(1, 1, 1, 1),
                 bg=Vec4(0, 0, 0, 1),
                 pos=Vec2(-0.85, 0.75),
                 scale=0.2,
                 font=font)

    OnscreenText(text="2",
                 fg=Vec4(1, 1, 1, 1),
                 bg=Vec4(0, 0, 0, 1),
                 pos=Vec2(-0.85, -0.75),
                 scale=0.2,
                 font=font)

    OnscreenText(text="3",
                 fg=Vec4(1, 1, 1, 1),
                 bg=Vec4(0, 0, 0, 1),
                 pos=Vec2(0.85, -0.75),
                 scale=0.2,
                 font=font)

    OnscreenText(text="4",
                 fg=Vec4(1, 1, 1, 1),
                 bg=Vec4(0, 0, 0, 1),
                 pos=Vec2(1.2, 0),
                 scale=0.2,
                 font=font)

    base.cam.setPos(0, -5, 0)
    base.run()
