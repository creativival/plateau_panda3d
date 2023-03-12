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

        # # Load a model.
        # smiley = self.loader.loadModel('smiley')
        # # Reparent the model to the camera so we can move it.
        # smiley.reparentTo(self.camera)
        # # Set the initial position of the model in the scene.
        # smiley.setPos(0, 25.5, 0.5)
        # smiley.setTransparency(TransparencyAttrib.MAlpha)
        # 
        # # Create a collision node for this object.
        # cNode = CollisionNode('smiley')
        # # Attach a collision sphere solid to the collision node.
        # cNode.addSolid(CollisionSphere(0, 0, 0, 1.1))
        # # Attach the collision node to the object's model.
        # smileyC = smiley.attachNewNode(cNode)
        # # Set the object's collision node to render as visible.
        # smileyC.show()
        # 
        # # Load another model.
        # frowney = self.loader.loadModel('frowney')
        # # Reparent the model to render.
        # frowney.reparentTo(self.render)
        # # Set the position of the model in the scene.
        # frowney.setPos(5, 25, 0)
        # frowney.setTransparency(TransparencyAttrib.MAlpha)
        # 
        # # Create a collision node for this object.
        # cNode = CollisionNode('frowney')
        # # Attach a collision sphere solid to the collision node.
        # cNode.addSolid(CollisionSphere(0, 0, 0, 1.1))
        # # Attach the collision node to the object's model.
        # frowneyC = frowney.attachNewNode(cNode)
        # # Set the object's collision node to render as visible.
        # frowneyC.show()
        # 
        # smiley.setTag('myObjectTag', '1')
        # frowney.setTag('myObjectTag', '2')

        # self.all_objects = [smiley, frowney]
        self.picked_object_tag = None

        self.taskMgr.doMethodLater(0.5, self.pick_object_by_mouse, 'pick_object_by_mouse')
        self.taskMgr.add(self.check_picked_object, 'check_picked_object')

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
        for obj in self.all_buildings:
            if obj.getTag('building_id') == self.picked_object_tag:
                obj.setColorScale(1, 0, 0, 1)
            else:
                if obj.hasColorScale():
                    obj.clearColorScale()

        return task.cont
