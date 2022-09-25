from puzzle import State, move, n_move_state

def makeNearGoal():
    cube = State()
    cube.set_left([['W','W','W'],['W','W','W'],['W','W','W']])
    cube.set_top([['B','B','B'],['B','B','B'],['B','B','B']])
    cube.set_back([['O','O','O'],['O','O','O'],['O','O','O']])
    cube.set_bottom([['G','G','G'],['G','G','G'],['G','G','G']])
    cube.set_front([['R','R','R'],['R','R','R'],['R','R','R']])
    cube.set_right([['Y','Y','Y'],['Y','Y','Y'],['Y','Y','Y']])
    # for action in cube.actions:
    #     new_s = move(cube, action)
    #     print(action)
    #     print(new_s)
        # if new_s.isGoalState():
        #     print("executing the " + action + " action resulted in the below goal state " + str(new_s))
    # print(move(cube, 'top'))        
    # print(cube)    
   #print(move(cube, 'top'))
    state = n_move_state(n=10)
    print(state)

        

makeNearGoal()