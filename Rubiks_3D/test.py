from core import Core, study
from rubik_2d import *

cubes, _ = n_move_state(n = 6)
agent = Core(start=cubes)
study(agent)
state_random, act = n_move_state(n=8)
agent.Play(state_random)