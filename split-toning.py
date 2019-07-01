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
    bl_label = "Add Split-Toning Node Operator"


def register():
    print("split-toning: registered.")


def unregister():
    print("split-toning: unregistered.")


if __name__ == "__main__":
    register()
