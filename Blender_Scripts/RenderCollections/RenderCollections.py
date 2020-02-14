import os
import bpy

OPTIONS = ["A", "B", "C", "D", "E", "F", "G", "H"]


def render_me():
    """    Just renders the sequence    """
    bpy.ops.render.render(animation=True, use_viewport=True)


def switch_2_defaults():
    """
    Turns visibility and renderability OFF and keeps the first one ON.
    """
    facade_variant = f"Opcion{OPTIONS[0]}"
    facade_variant_back = f"Opcion{OPTIONS[0]}_Back"

    for parent_collection in bpy.data.collections:
        if facade_variant_back in parent_collection.children.keys():
            options_2_render = [op for op in parent_collection.children.keys() if "opcion" in op.lower()]
            for col in options_2_render:
                bpy.data.collections[col].hide_viewport = True
                bpy.data.collections[col].hide_render = True

    bpy.data.collections[facade_variant].hide_render = False
    bpy.data.collections[facade_variant].hide_viewport = False
    bpy.data.collections[facade_variant_back].hide_render = False
    bpy.data.collections[facade_variant_back].hide_viewport = False


def options_switch(option, visibility):
    """
    Turns visibility and renderability of the option collection ON or OFF before rendering.
    :param option:      String of the option to render
    :param visibility:  Boolean value for the visibility and renderability for the option.
    :param frame_end:   Hard-coded based on my animation needs. From 5 frame
                        animation I only need the first 3 if Option*_Back
                        collection does not exist
    """
    facade_variant = f"Opcion{option}"
    facade_variant_back = f"Opcion{option}_Back"
    bpy.data.collections[facade_variant].hide_viewport = visibility
    bpy.data.collections[facade_variant].hide_render = visibility
    if bpy.data.collections.get(facade_variant_back):
        print(facade_variant_back, "ON")
        bpy.data.collections[facade_variant_back].hide_render = visibility
        bpy.data.collections[facade_variant_back].hide_viewport = visibility
        bpy.context.scene.frame_end = 5
    else:
        facade_variant = f"Opcion{OPTIONS[0]}"
        facade_variant_back = f"Opcion{OPTIONS[0]}_Back"
        print(facade_variant_back, "OFF")
        bpy.data.collections[facade_variant_back].hide_render = visibility
        bpy.data.collections[facade_variant_back].hide_viewport = visibility
        bpy.context.scene.frame_end = 3


def render_options(options):
    """
    Turns ALL collections OFF and sets defaults ON.
    For every option turns ON the collections and sets the ouputs accordingly.
    Renders the option.
    Turns ALL collections OFF and sets defaults ON again

    :param options: List of options to render defined globally.

    """
    switch_2_defaults()
    for option in options:
        options_switch(option, False)
        project_path = os.path.abspath(r"C:\Users\<YourUserName>\<My_Project>")
        filepath = os.path.join(project_path, "Renders", "RAW_Renders", f"Scene_V01{option}-####.exr")
        bpy.context.scene.render.filepath = filepath
        base_path = os.path.join(project_path, "Renders", "Comp_Renders")
        file_subpath = f"Scene_V01{option}-####.png"
        bpy.context.scene.node_tree.nodes['File Output'].base_path = base_path
        bpy.context.scene.node_tree.nodes['File Output'].file_slots[0].path = file_subpath

        render_me()

        options_switch(option, True)
    switch_2_defaults()


render_options(OPTIONS)
