import bpy
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "starter_files"


def reset_to_factory():
    bpy.ops.wm.read_factory_settings(use_empty=False)


def save_mainfile(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(path))


def clear_mesh_objects():
    bpy.ops.object.select_all(action="DESELECT")
    for obj in list(bpy.data.objects):
        if obj.type == "MESH":
            obj.select_set(True)
    bpy.ops.object.delete()


def create_navigation_practice():
    reset_to_factory()

    cube = bpy.data.objects["Cube"]
    cube.name = "Center_Cube"

    bpy.ops.mesh.primitive_uv_sphere_add(location=(2.8, 0.0, 0.0))
    sphere = bpy.context.active_object
    sphere.name = "Right_Sphere"

    bpy.ops.mesh.primitive_cylinder_add(location=(-2.8, 0.0, 0.0))
    cylinder = bpy.context.active_object
    cylinder.name = "Left_Cylinder"

    bpy.ops.object.select_all(action="DESELECT")
    for obj in (cube, sphere, cylinder):
        obj.select_set(True)

    save_mainfile(OUTPUT_DIR / "week02_navigation_practice.blend")


def create_factory_start():
    reset_to_factory()
    save_mainfile(OUTPUT_DIR / "week02_factory_start.blend")


def create_transform_practice():
    reset_to_factory()
    clear_mesh_objects()

    bpy.ops.mesh.primitive_cube_add(location=(0.0, 0.0, 0.0))
    cube = bpy.context.active_object
    cube.name = "Transform_Cube"

    bpy.ops.mesh.primitive_uv_sphere_add(location=(2.6, 0.0, 0.0))
    sphere = bpy.context.active_object
    sphere.name = "Transform_Sphere"

    bpy.ops.mesh.primitive_cylinder_add(location=(-2.6, 0.0, 0.0))
    cylinder = bpy.context.active_object
    cylinder.name = "Transform_Cylinder"

    bpy.ops.mesh.primitive_cone_add(location=(0.0, 2.6, 0.0))
    cone = bpy.context.active_object
    cone.name = "Transform_Cone"

    save_mainfile(OUTPUT_DIR / "week02_transform_practice.blend")


def create_pencil_holder_start():
    reset_to_factory()
    clear_mesh_objects()

    bpy.ops.mesh.primitive_cube_add(location=(0.0, 0.0, 0.0))
    cube = bpy.context.active_object
    cube.name = "PencilHolder_Base"

    save_mainfile(OUTPUT_DIR / "week02_pencil_holder_start.blend")


def create_feature_drill_start():
    reset_to_factory()
    clear_mesh_objects()

    bpy.ops.mesh.primitive_cube_add(location=(0.0, 0.0, 0.0))
    block = bpy.context.active_object
    block.name = "Feature_Drill_Block"
    block.scale = (1.35, 1.35, 0.8)
    bpy.context.view_layer.objects.active = block
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    save_mainfile(OUTPUT_DIR / "week02_feature_drill_start.blend")


create_factory_start()
create_navigation_practice()
create_transform_practice()
create_pencil_holder_start()
create_feature_drill_start()

print(f"Created starter files in {OUTPUT_DIR}")
