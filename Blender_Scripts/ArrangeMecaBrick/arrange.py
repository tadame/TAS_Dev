import bpy


LEGO_GROUP = "Lego_GRP"
PIECE_NAME = "Piece"
CLEAN_MATERIALS = True


def get_materials():
    """Get Materials in scene & objects.
    """
    gather = {}
    for mat in bpy.data.materials:
        elements = []
        for obj in bpy.data.objects:
            if obj.material_slots:
                if mat.name == obj.material_slots[0].material.name:
                    elements.append(obj)
        gather.update({mat: elements})
    return gather


def create_default_material():
    """Create default grey material
    """
    default_grey = bpy.data.materials.data.materials.new("Default_Grey")
    default_grey.use_nodes = True
    default_grey.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.5, 0.5, 0.5, 1)
    return default_grey


def clean_materials(purge, piece, shd):
    if purge:
        piece.data.materials.clear()
        piece.data.materials.append(shd)


def create_collections():
    """Create collections and add items
    """
    gather = get_materials()
    default_grey = create_default_material()
    default_collection = bpy.data.collections.items()[0][1]
    lego_collection = bpy.data.collections.new(LEGO_GROUP)
    bpy.context.scene.collection.children.link(lego_collection)
    for mat in gather.keys():
        collection = bpy.data.collections.new(f"{mat.name}_GRP")
        bpy.context.scene.collection.children.link(collection)
        lego_collection.children.link(collection)
        for item in gather.get(mat):
            default_collection.objects.unlink(item)
            collection.objects.link(item)
            item.name = f"{PIECE_NAME}_{mat.name}"
            clean_materials(CLEAN_MATERIALS, item, default_grey)


if __name__ == "__main__":
    create_collections()
