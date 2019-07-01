import bpy

bl_info = {
    "name": "split-toning",
    "author": "Yuki Koyama",
    "version": (0, 0),
    "blender": (2, 79, 0),
    "location": "",
    "description": "Simulating the Split Toning effect in Adobe Lightroom/Photoshop",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Node"
}


class AddSplitToningNodeOperator(bpy.types.Operator):
    bl_idname = "node.add_split_toning_node_operator"
    bl_label = "Split-Toning"

    def execute(self, context):
        self.report({'WARNING'}, "TODO: This function is under construction...")
        return {'FINISHED'}


def menu_fn(self, context):
    self.layout.separator()
    self.layout.operator(AddSplitToningNodeOperator.bl_idname)


def register():
    bpy.utils.register_module(__name__)
    bpy.types.NODE_MT_add.append(menu_fn)
    print("split-toning: registered.")


def unregister():
    bpy.types.NODE_MT_add.remove(menu_fn)
    bpy.utils.unregister_module(__name__)
    print("split-toning: unregistered.")


if __name__ == "__main__":
    register()
