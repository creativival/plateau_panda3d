from math import *
from panda3d.core import *
from . import draw_line_between_two_points


class Collision:
    def __init__(self):
        # Initialize the collision traverser.
        self.collision_traverser = CollisionTraverser()

        # Initialize the handler.
        self.collision_handler_queue = CollisionHandlerQueue()
        # self.collHandEvent.addInPattern('into-%in')
        # self.collHandEvent.addOutPattern('outof-%in')

        picker_node = CollisionNode('mouseRay')
        picker_node_path = self.camera.attachNewNode(picker_node)
        picker_node.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.picker_ray = CollisionRay()
        picker_node.addSolid(self.picker_ray)
        self.collision_traverser.addCollider(picker_node_path, self.collision_handler_queue)

        self.picked_object_tag = None

        self.accept('f9', self.toggle_show_or_hide_building)

        self.taskMgr.doMethodLater(0.5, self.pick_object_by_mouse, 'pick_object_by_mouse')
        self.taskMgr.add(self.check_picked_object, 'check_picked_object')

    def toggle_show_or_hide_building(self):
        if self.picked_object_tag:
            building_node = self.map_node.find(self.picked_object_tag)
            if building_node:
                is_hidden = building_node.getPythonTag('is_hidden')
                if is_hidden:
                    building_node.show()
                    building_node.setPythonTag('is_hidden', False)
                else:
                    building_node.hide()
                    building_node.setPythonTag('is_hidden', True)

    def pick_object_by_mouse(self, task):
        self.picked_object_tag = None

        if self.mouseWatcherNode.hasMouse():
            mouse_x, mouse_y = self.mouseWatcherNode.getMouse()
            self.picker_ray.setFromLens(self.camNode, mouse_x, mouse_y)
            self.collision_traverser.traverse(self.render)
            # Assume for simplicity's sake that myHandler is a CollisionHandlerQueue.
            if self.collision_handler_queue.getNumEntries() > 0:
                # print('get entry')
                # This is so we get the closest object.
                self.collision_handler_queue.sortEntries()
                picked_obj = self.collision_handler_queue.getEntry(0).getIntoNodePath()
                picked_obj = picked_obj.findNetTag('building_id')
                if not picked_obj.isEmpty():
                    # print('not empty')
                    # print(picked_obj)
                    # print(picked_obj.getTag('myObjectTag'))
                    self.picked_object_tag = picked_obj.getTag('building_id')

        return task.again

    def check_picked_object(self, task):
        for building_node in self.all_buildings:
            if building_node.getTag('building_id') == self.picked_object_tag:
                # print(building_node.getColorScale())
                if building_node.getPythonTag('is_hidden'):
                    if building_node.isHidden():
                        building_node.show()
                    if not building_node.hasColorScale() or \
                            building_node.getColorScale() != LVecBase4f(0, 0, 1, 1):
                        building_node.setColorScale(0, 0, 1, 1)
                else:
                    if not building_node.hasColorScale() or \
                            building_node.getColorScale() != LVecBase4f(1, 0, 0, 1):
                        building_node.setColorScale(1, 0, 0, 1)
            else:
                if building_node.getPythonTag('is_hidden') and \
                        not building_node.isHidden():
                    building_node.hide()
                if building_node.hasColorScale():
                    building_node.clearColorScale()

        return task.cont
