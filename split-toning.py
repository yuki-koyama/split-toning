import bpy

bl_info = {
    "name": "split-toning",
    "author": "Yuki Koyama",
    "version": (0, 0),
    "blender": (2, 79, 0),
    "location": "Node Editor (or Compositor) > Add",
    "description": "Simulating the Split Toning effect in Adobe Lightroom/Photoshop",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Node"
}


def add_split_tone_node_group():
    assert not "SplitTone" in bpy.data.node_groups
    assert not "SplitToneSub" in bpy.data.node_groups

    group = bpy.data.node_groups.new(type="CompositorNodeTree", name="SplitToneSub")

    input_node = group.nodes.new("NodeGroupInput")
    group.inputs.new("NodeSocketColor", "Image")
    group.inputs.new("NodeSocketFloat", "Hue")
    group.inputs.new("NodeSocketFloat", "Saturation")

    solid_node = group.nodes.new(type="CompositorNodeCombHSVA")
    solid_node.inputs["S"].default_value = 1.0
    solid_node.inputs["V"].default_value = 1.0
    solid_node.inputs["A"].default_value = 1.0

    input_sep_node = group.nodes.new(type="CompositorNodeSepHSVA")

    overlay_node = group.nodes.new(type="CompositorNodeMixRGB")
    overlay_node.blend_type = 'OVERLAY'

    overlay_sep_node = group.nodes.new(type="CompositorNodeSepHSVA")

    comb_node = group.nodes.new(type="CompositorNodeCombHSVA")

    output_node = group.nodes.new("NodeGroupOutput")
    group.outputs.new("NodeSocketColor", "Image")

    group.links.new(input_node.outputs["Hue"], solid_node.inputs["H"])
    group.links.new(input_node.outputs["Saturation"], overlay_node.inputs["Fac"])
    group.links.new(input_node.outputs["Image"], overlay_node.inputs[1])
    group.links.new(solid_node.outputs["Image"], overlay_node.inputs[2])
    group.links.new(overlay_node.outputs["Image"], overlay_sep_node.inputs["Image"])
    group.links.new(input_node.outputs["Image"], input_sep_node.inputs["Image"])
    group.links.new(overlay_sep_node.outputs["H"], comb_node.inputs["H"])
    group.links.new(overlay_sep_node.outputs["S"], comb_node.inputs["S"])
    group.links.new(input_sep_node.outputs["V"], comb_node.inputs["V"])
    group.links.new(input_sep_node.outputs["A"], comb_node.inputs["A"])
    group.links.new(comb_node.outputs["Image"], output_node.inputs["Image"])

    # --------------------------------------------------------------------------

    group = bpy.data.node_groups.new(type="CompositorNodeTree", name="SplitTone")

    input_node = group.nodes.new("NodeGroupInput")

    def set_socket_value_range(socket, default_value=0.0, min_value=0.0, max_value=1.0):
        socket.default_value = default_value
        socket.min_value = min_value
        socket.max_value = max_value

    group.inputs.new("NodeSocketColor", "Image")
    group.inputs.new("NodeSocketFloat", "HighlightsHue")
    group.inputs.new("NodeSocketFloat", "HighlightsSaturation")
    group.inputs.new("NodeSocketFloat", "ShadowsHue")
    group.inputs.new("NodeSocketFloat", "ShadowsSaturation")
    group.inputs.new("NodeSocketFloatFactor", "Balance")

    set_socket_value_range(group.inputs["HighlightsHue"])
    set_socket_value_range(group.inputs["HighlightsSaturation"])
    set_socket_value_range(group.inputs["ShadowsHue"])
    set_socket_value_range(group.inputs["ShadowsSaturation"])
    set_socket_value_range(group.inputs["Balance"], default_value=0.5)

    input_sep_node = group.nodes.new(type="CompositorNodeSepHSVA")

    subtract_node = group.nodes.new(type="CompositorNodeMath")
    subtract_node.inputs[0].default_value = 1.0
    subtract_node.operation = 'SUBTRACT'
    subtract_node.use_clamp = True

    multiply_node = group.nodes.new(type="CompositorNodeMath")
    multiply_node.inputs[1].default_value = 2.0
    multiply_node.operation = 'MULTIPLY'
    multiply_node.use_clamp = False

    power_node = group.nodes.new(type="CompositorNodeMath")
    power_node.operation = 'POWER'
    power_node.use_clamp = True

    shadows_node = group.nodes.new(type='CompositorNodeGroup')
    shadows_node.name = "Shadows"
    shadows_node.node_tree = bpy.data.node_groups["SplitToneSub"]

    highlights_node = group.nodes.new(type='CompositorNodeGroup')
    highlights_node.name = "Highlights"
    highlights_node.node_tree = bpy.data.node_groups["SplitToneSub"]

    comb_node = group.nodes.new(type="CompositorNodeMixRGB")
    comb_node.use_clamp = False

    output_node = group.nodes.new("NodeGroupOutput")
    group.outputs.new("NodeSocketColor", "Image")

    group.links.new(input_node.outputs["Image"], input_sep_node.inputs["Image"])
    group.links.new(input_node.outputs["Image"], shadows_node.inputs["Image"])
    group.links.new(input_node.outputs["ShadowsHue"], shadows_node.inputs["Hue"])
    group.links.new(input_node.outputs["ShadowsSaturation"], shadows_node.inputs["Saturation"])
    group.links.new(input_node.outputs["Image"], highlights_node.inputs["Image"])
    group.links.new(input_node.outputs["HighlightsHue"], highlights_node.inputs["Hue"])
    group.links.new(input_node.outputs["HighlightsSaturation"], highlights_node.inputs["Saturation"])
    group.links.new(input_node.outputs["Balance"], subtract_node.inputs[1])
    group.links.new(subtract_node.outputs["Value"], multiply_node.inputs[0])
    group.links.new(input_sep_node.outputs["V"], power_node.inputs[0])
    group.links.new(multiply_node.outputs["Value"], power_node.inputs[1])
    group.links.new(power_node.outputs["Value"], comb_node.inputs["Fac"])
    group.links.new(shadows_node.outputs["Image"], comb_node.inputs[1])
    group.links.new(highlights_node.outputs["Image"], comb_node.inputs[2])
    group.links.new(comb_node.outputs["Image"], output_node.inputs["Image"])

    return group


def create_split_tone_node(node_tree):
    node = node_tree.nodes.new(type='CompositorNodeGroup')
    node.name = "SplitTone"
    node.node_tree = bpy.data.node_groups["SplitTone"]

    return node


class AddSplitToningNodeOperator(bpy.types.Operator):
    bl_idname = "node.add_split_toning_node_operator"
    bl_label = "Split-Toning"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        if not bpy.context.scene.use_nodes:
            self.report({'ERROR'}, "Failed to add a split-toning node because the scene does not use nodes currently.")
            return {'CANCELLED'}

        if not "SplitTone" in bpy.data.node_groups:
            add_split_tone_node_group()

        create_split_tone_node(bpy.context.scene.node_tree)

        self.report({'INFO'}, "A split-toning node is added to the node tree.")
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.separator()
    self.layout.operator(AddSplitToningNodeOperator.bl_idname)


def register():
    bpy.utils.register_module(__name__)
    bpy.types.NODE_MT_add.append(menu_func)

    print("split-toning: registered.")


def unregister():
    bpy.types.NODE_MT_add.remove(menu_func)
    bpy.utils.unregister_module(__name__)

    print("split-toning: unregistered.")


if __name__ == "__main__":
    register()
