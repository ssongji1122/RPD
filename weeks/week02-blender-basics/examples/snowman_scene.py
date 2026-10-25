"""Week 02 코드 생성 비교 실습의 기준 스크립트입니다.

수업에서 Claude가 만든 스크립트와 비교할 때 강사가 미리 돌려 보는 정답 예시입니다.
Blender 5.0의 Scripting 작업 공간에서 실행하거나, 터미널에서
`blender --background --python snowman_scene.py -- <출력 PNG 경로>`로 렌더합니다.
"""
import math
import sys

import bpy

RENDER_WIDTH = 960
RENDER_HEIGHT = 540
BODY_RADII = (1.0, 0.7, 0.45)
NOSE_LENGTH = 0.4
HAT_HEIGHT = 0.5
CAMERA_LOCATION = (8.0, -10.0, 5.0)
CAMERA_TARGET = (0.0, 0.0, 2.2)
SUN_ROTATION_DEG = (50.0, 0.0, 35.0)


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def build_snowman():
    z = 0.0
    for radius in BODY_RADII:
        z += radius
        bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(0, 0, z))
        z += radius * 0.8  # 위 공과 살짝 겹치게 쌓습니다
    head_z = z - BODY_RADII[-1] * 0.8
    head_r = BODY_RADII[-1]
    bpy.ops.mesh.primitive_cone_add(
        radius1=0.08, depth=NOSE_LENGTH,
        location=(0, -head_r - NOSE_LENGTH / 2 + 0.05, head_z),
        rotation=(math.radians(90), 0, 0))
    bpy.ops.mesh.primitive_cylinder_add(
        radius=head_r * 0.7, depth=HAT_HEIGHT,
        location=(0, 0, head_z + head_r + HAT_HEIGHT / 2 - 0.05))
    bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))


def add_camera_and_light():
    bpy.ops.object.camera_add(location=CAMERA_LOCATION)
    camera = bpy.context.active_object
    target = bpy.data.objects.new("CameraTarget", None)
    target.location = CAMERA_TARGET
    bpy.context.collection.objects.link(target)
    track = camera.constraints.new(type="TRACK_TO")
    track.target = target
    bpy.context.scene.camera = camera
    bpy.ops.object.light_add(
        type="SUN", rotation=tuple(math.radians(a) for a in SUN_ROTATION_DEG))


def render_to(path):
    scene = bpy.context.scene
    scene.render.resolution_x = RENDER_WIDTH
    scene.render.resolution_y = RENDER_HEIGHT
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    clear_scene()
    build_snowman()
    add_camera_and_light()
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if argv:
        render_to(argv[0])
