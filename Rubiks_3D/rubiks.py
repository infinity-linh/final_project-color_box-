from ursina import *
from core import Core, study
from rubik_2d import *
import time
def position_box():
    side_position = {}
    LEFT = {Vec3(-1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
    BOTTOM = {Vec3(x, -1, z) for x in range(-1, 2) for z in range(-1, 2)}
    FACE = {Vec3(x, y, -1) for x in range(-1, 2) for y in range(-1, 2)}
    BACK = {Vec3(x, y, 1) for x in range(-1, 2) for y in range(-1, 2)}
    RIGHT = {Vec3(1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
    TOP = {Vec3(x, 1, z) for x in range(-1, 2) for z in range(-1, 2)}
    side_position['LEFT'] = LEFT
    side_position['BOTTOM'] = BOTTOM
    side_position['FACE'] = FACE
    side_position['BACK'] = BACK
    side_position['RIGHT'] = RIGHT
    side_position['TOP'] = TOP
    SIDE_POSITIONS = LEFT | BOTTOM | FACE | BACK | RIGHT | TOP
    return side_position, SIDE_POSITIONS

def reparent_to_scene():
        for cube in cubes:
            if cube.parent == cube_root:
                world_pos, world_rot = round(cube.world_position, 1), cube.world_rotation
                cube.parent = scene
                cube.position, cube.rotation = world_pos, world_rot
                # print(cube.position, cube.rotation)
                print(world_pos,world_rot)
        cube_root.rotation = 0


def rotate_side(side_name):
    cube_position = side_position[side_name]
    rotation_axis = rotation_axes[side_name]
    reparent_to_scene()
    for cube in cubes:
        if cube.position in cube_position:
            cube.parent = cube_root
            eval(f'cube_root.animate_rotation_{rotation_axis}(180, duration=0.5)')
    # print(cube_position)
    # invoke(update, delay=animation_time + 0.11)

def action(key):
    if key == "left":
        rotate_side("LEFT")
    elif key == "right":
        rotate_side("RIGHT")
    elif key == "top":
        rotate_side("TOP")
    elif key == "bottom":
        rotate_side("BOTTOM")
    elif key == "front":
        rotate_side("FACE")
    elif key == "back":
        rotate_side("BACK")

# def input(key):
#     if key == "space":
#         state_random, act = n_move_state(n=8)
#         for ac in range(len(act)):
#             action(act[ac])
#         print("Đã xáo xong!")
#     elif key == "x":
#         agent.Play(state_random, save_action)
#         for a in save_action:
#             action(a)

# def animation_cube(act):
#     action(act)
    # print("Hello world!")

# def print_():
#     print("Next")

# def update():
    # if held_keys["space"]:
    #     state_random, act = n_move_state(n=8)
    #     for ac in act:

# def input(key):
        # invoke(Func(animation_cube, ac), delay=0.7)
        # key = "space"
        # if k == len(act) - 1:
        #     print("Đã xáo xong")
    # elif key == "x":
    #     key = "x"
    #     print(key)
    # invoke(print_, delay=1)


app = Ursina()

Entity(model='quad', scale=60, texture='white_cube', texture_scale=(60, 60), rotation_x=90, y=-5,
               color=color.light_gray)  # plane
Entity(model='sphere', scale=100, texture='textures/sky2', double_sided=True)  # sky
EditorCamera()
camera.world_position = (0, 0, -15)
model, texture = 'models/custom_cube', 'textures/rubik_texture'
side_position, SIDE_POSITIONS = position_box()
cubes = [Entity(model=model, texture=texture, position=pos) for pos in SIDE_POSITIONS]
cube_root = Entity()
rotation_axes = {'LEFT': 'x', 'RIGHT': 'x', 'TOP': 'y', 'BOTTOM': 'y', 'FACE': 'z', 'BACK': 'z'}
# cubes_side_positons = side_position
animation_time = 0.5
# cub, actions = n_move_state(n=10)
cub, _ = n_move_state(n=6)
agent = Core(start=cub)
study(agent)
save_action = []

cub, actions = n_move_state(n=10)
for act in actions:
    action(act)
    app.run()
agent.Play(cub,save_action)
for act in save_action:
    action(act)
    app.run()
# app.disable()

