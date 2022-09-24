# from puzzle import 
from rubik_2d import State, move, num_pieces_correct_side, num_solved_sides

def makeNearGoal():
    cube = State()
    cube.set_left([['W','W','W'],['W','W','W'],['W','W','W']])
    cube.set_top([['B','B','B'],['B','B','B'],['B','B','B']])
    cube.set_back([['O','O','O'],['O','O','O'],['O','O','O']])
    cube.set_bottom([['G','G','G'],['G','G','G'],['G','G','G']])
    cube.set_front([['R','R','R'],['R','R','R'],['R','R','R']])
    cube.set_right([['Y','Y','Y'],['Y','Y','Y'],['Y','Y','Y']])
    # for action in cube.actions:
    #     print(action)
    #     new_s = move(cube, action)
    #     print(new_s)
    #     if new_s.isGoalState():
    #         print("executing the " + action + " action resulted in the below goal state " + str(new_s))
    # cube.turn_back()
    # cube.rotate_cube()
    # print()        
    # print(cube)
    # print('test:', )
    states = move(cube,"right")
    states = move(states,"front")
    states = move(states,"back")
    states = move(states,"left")
    states = move(states,"top")
    states = move(states,"bottom")
    states = move(states,"left")

    print(states)
    # num_solved_sides(states)


        

        

makeNearGoal()