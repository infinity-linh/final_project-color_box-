from ursina import *


class Game(Ursina):
    def __init__(self):
        super().__init__()
        window.fullscreen = False
        Entity(model='quad', scale=50, texture='white_cube', texture_scale=(60, 60), rotation_x=90, y=-5,
               color=color.light_gray)  # plane
        Entity(model='sphere', scale=100,
               texture='textures/sky2', double_sided=True)  # sky
        EditorCamera()
        camera.world_position = (0, 0, -15)
        self.model, self.texture = 'models/custom_cube', 'textures/rubik_texture'
        self.load_game()

    def load_game(self):
        self.create_cube_positions()
        # print(self.SIDE_POSITIONS)
        self.CUBES = [Entity(model=self.model, texture=self.texture,
                             position=pos) for pos in self.SIDE_POSITIONS]
        self.PARENT = Entity()
        self.rotation_axes = {'LEFT': 'x', 'RIGHT': 'x',
                              'TOP': 'y', 'BOTTOM': 'y', 'FACE': 'z', 'BACK': 'z'}
        self.cubes_side_positons = {'LEFT': self.LEFT, 'BOTTOM': self.BOTTOM, 'RIGHT': self.RIGHT, 'FACE': self.FACE,
                                    'BACK': self.BACK, 'TOP': self.TOP}
        self.animation_time = 0.5
        self.action_trigger = True
        # self.action_mode = True
        self.message = Text(origin=(0, 19), color=color.black)
    #     self.toggle_game_mode()
    #     self.create_sensors()
        # initial state of the cube, rotations - number of side turns
        self.random_state(rotations=3)

    def random_state(self, rotations=10):
        [self.rotate_side_without_animation(random.choice(
            list(self.rotation_axes))) for i in range(rotations)]

    def rotate_side_without_animation(self, side_name):
        # print("1", side_name)
        cube_positions = self.cubes_side_positons[side_name]
        rotation_axis = self.rotation_axes[side_name]
        # print("2", cube_positions)
        print("3", rotation_axis)
        self.reparent_to_scene()
        for cube in self.CUBES:
            if cube.position in cube_positions:
                cube.parent = self.PARENT
                exec(f'self.PARENT.rotation_{rotation_axis} = 90')

    def reparent_to_scene(self):
        # print(self.CUBES)
        for cube in self.CUBES:
            if cube.parent == self.PARENT:
                world_pos, world_rot = round(
                    cube.world_position, 1), cube.world_rotation
                cube.parent = scene
                cube.position, cube.rotation = world_pos, world_rot
        self.PARENT.rotation = 0

    def status_rubik(self):
        pass

    def create_cube_positions(self):
        self.LEFT = {Vec3(-1, y, z) for y in range(-1, 2)
                     for z in range(-1, 2)}
        # print("Left ", self.LEFT)
        self.BOTTOM = {Vec3(x, -1, z) for x in range(-1, 2)
                       for z in range(-1, 2)}
        # print("Bottom ", self.BOTTOM)

        self.FACE = {Vec3(x, y, -1) for x in range(-1, 2)
                     for y in range(-1, 2)}
        # print("Face ", self.FACE)

        self.BACK = {Vec3(x, y, 1) for x in range(-1, 2) for y in range(-1, 2)}
        # print("Back ", self.BACK)

        self.RIGHT = {Vec3(1, y, z) for y in range(-1, 2)
                      for z in range(-1, 2)}
        # print("Right ", self.RIGHT)

        self.TOP = {Vec3(x, 1, z) for x in range(-1, 2) for z in range(-1, 2)}
        # print("Top ", self.TOP)
        # print("Len :", len(self.LEFT | self.BOTTOM | self.BACK))

        self.SIDE_POSITIONS = self.LEFT | self.BOTTOM | self.FACE | self.BACK | self.RIGHT | self.TOP


if __name__ == '__main__':
    game = Game()
    game.run()
