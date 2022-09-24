import random
from rubik_2d import State, move, num_solved_sides, num_pieces_correct_side, n_move_state

ALPHA = 0.6

class Core:

    def __init__(self, QValues=None, start=None):
        self.visited = []
        self.visit_count = {}
        self.revisits = 0

        self.QV = QValues if QValues is not None else {}
        # print(self.QV)
        self.R = {}
        self.start_state = start 
        print("Start: ",self.start_state)
        self.curr_state = self.start_state
        self.prev_state = None
        self.second_last_action = None
        self.actions = self.start_state.actions
        self.save_action = []
        self.one_away = []
        self.two_away = []
        self.three_away = []
        self.four_away = []
        self.five_away = []
        self.six_away = []
        self.last_action = None
        self.move = {"front": 0, "back": 0, "left": 0, "right": 0, "top": 0, "bottom": 0}

    def register_patterns(self):
        s = State()
        for action in self.actions:
            s_ = move(s, action)
            self.one_away.append(s_)
            for action_ in self.actions:
                self.QV[s_.__hash__(), action_] = -10 if action_ != action else 10
        for s in self.one_away:
            # print(s)
            for action in self.actions:
                s_ = move(s, action)
                self.two_away.append(s_)
                for action_ in self.actions:
                    self.QV[(s_.__hash__(), action)] = -6 if action_ !=action else 6
        # print(self.QV)
        for s in self.two_away:
            for action in self.actions:
                s_ = move(s, action)
                self.three_away.append(s_)
                for action_ in self.actions:
                    self.QV[(s_.__hash__(), action_)] = -5 if action_ != action else 5
        for s in self.three_away:
            for action in self.actions:
                s_ = move(s, action)
                self.four_away.append(s_)
                for action_ in self.actions:
                    self.QV[(s_.__hash__(), action_)] = -4 if action_ != action else 4
        for s in self.four_away:
            for action in self.actions:
                s_ = move(s, action)
                self.five_away.append(s_)
                for action_ in self.actions:
                    self.QV[(s_.__hash__(), action_)] = -3 if action_ != action else 3
        for s in self.five_away:
            for action in self.actions:
                s_ = move(s, action)
                self.six_away.append(s_)
                for action_ in self.actions:
                    self.QV[(s_.__hash__(), action_)] = -1 if action_ != action else 1
    
    
    def QLearn(self, discount=0.99, episodes=10, epsilon=0.9):
        self.curr_state = self.curr_state
        output = []
        for i in range(episodes):
            # print(i)
            print("=====EPISODE "+str(i)+"=====")
            saved_reward = self.curr_state.__hash__() in self.R.keys()
            # print(saved_reward)
            if not saved_reward:
                self.R[self.curr_state.__hash__()] = []
            if not self.curr_state.__hash__ in self.visit_count:
                self.visit_count[self.curr_state.__hash__()] = 1
                # print(self.visit_count)
            else :
                self.visit_count[self.curr_state.__hash__()] += 1
            vc = self.visit_count[self.curr_state.__hash__()]
            # print(vc)
            for action in self.actions:
                if not (self.curr_state.__hash__(), action) in self.QV.keys():
                    self.QV[(self.curr_state.__hash__(), action)] = 0
                else:
                    self.revisits += 1
                    break
                if not saved_reward:
                    self.R[self.curr_state.__hash__()].append(self.reward(self.curr_state, action))
            # print("####################",self.R)
            if 100 in self.R[self.curr_state.__hash__()]:
                print("Mục tiêu đã đạt được, kết thúc!")
                return
            follow_policy = random.uniform(0, 1.0)
            print("random value is " + str(follow_policy))
            if follow_policy > epsilon:
                print("Following policy")
                for action in self.actions:
                    print("q value for action " + action +" from curr state is " + str(self.QV[(self.curr_state.__hash__(), action)]))
                best_action = None
                best_QV = -100000000
                # print(self.QV)
                for action in self.actions:
                    if self.QV[(self.curr_state.__hash__(), action)] > best_QV and action != self.second_last_action:
                        best_action = action
                        best_QV = self.QV[(self.curr_state.__hash__(), action)]
                if best_QV == 0:
                    best_action = random.choice(self.actions)
                    while best_action == self.last_action:
                        best_action = random.choice(self.actions)
                        # print(best_action)
                output.append(best_action)
                print("actions chosen = " + best_action)
                self.move[best_action] = self.move[best_action] + 1
                # print(self.move)

                for action in self.actions:
                        curr_QV = self.QV[(self.curr_state.__hash__(), action)]
                        reward = self.reward(self.curr_state, action)
                        max_reward = self.max_reward(self.curr_state, action)
                        self.QV[(self.curr_state.__hash__(), action)] = curr_QV + ALPHA*(reward +\
                                                            (discount**vc)*max_reward - curr_QV)
                # print(self.QV)
                print("new q value for " + best_action + " action is " + str(self.QV[(self.curr_state.__hash__(), best_action)]))
                # print(follow_policy)
                self.curr_state.move(best_action)
                print(self.curr_state)
                self.curr_state = self.curr_state.copy()
                if self.curr_state.isGoalState():
                    print("Đã đạt được trạng thái mục tiêu ở " + str(i))
                    return
                self.second_last_action = self.last_action
                self.last_action = best_action
            else:
            # pick random move
                action = random.choice(self.actions)
                self.move[action] = self.move[action] + 1
                while action == self.last_action or action == self.second_last_action:
                    action = random.choice(self.actions)
                reward = 0
                for action in self.actions:
                    curr_QV = self.QV[(self.curr_state.__hash__(), action)]
                    reward = self.reward(self.curr_state, action)
                    max_reward = self.max_reward(self.curr_state, action)
                    self.QV[(self.curr_state.__hash__(), action)] = curr_QV + ALPHA*(reward +\
                                                         (discount**vc)*max_reward - curr_QV)
                self.curr_state.move(action)
                # print(self.curr_state)
                self.curr_state = self.curr_state.copy()
                self.second_last_action = self.last_action  
                self.last_action = action
                if self.curr_state.isGoalState():
                    print("Đã đạt được trạng thái mục tiêu ở " + str(i))
                    #time.sleep(2)
                    return
    def Play(self, state_random, save_action):
        self.second_last_action = None
        self.last_action = None
        self.curr_state = state_random
        print(state_random)
        # for i in range(20):
        best_action = None
        best_QV = -100000000
        if not (self.curr_state.__hash__(), self.actions[0]) in self.QV.keys():
            best_action = random.choice(self.actions)
            while best_action == self.second_last_action or best_action == self.last_action:
                best_action = random.choice(self.actions)
            for action in self.actions:
                self.QV[(self.curr_state.__hash__(), action)] = 0
            best_QV = 0
        else:
            for action in self.actions:
                if self.QV[(self.curr_state.__hash__(), action)] > best_QV \
                and (action != self.last_action and action != self.second_last_action):
                    best_action = action
                    best_QV = self.QV[(self.curr_state.__hash__(), action)]
        save_action.append(best_action)
        print("actions chosen = " + best_action)
        print("last action = " + (self.last_action if self.last_action is not None  else "None"))
        print("q value is " + str(self.QV[(self.curr_state.__hash__(), best_action)]))
        #time.sleep(1)
        self.curr_state.move(best_action)
        self.second_last_action = self.last_action
        self.last_action = best_action
        print(save_action)
        if self.curr_state.isGoalState():
            print("AGENT REACHED A GOAL STATE!!!")
            #time.sleep(5)
            return
        # else :
        #     self.Play()
        else:
            print("Trạng thái chưa đạt quay tiếp! ")
            self.Play(self.curr_state, save_action)

    def reward(self, state, action):
        next_state = move(state, action)
        if next_state.isGoalState():
            # print(state)
            # print(next_state)
            print("Reward is goal")
            return 100
        reward = -0.1
        solved_sides = 2 * (num_solved_sides(next_state) < num_solved_sides(state))
        solved_pieces = 0.5 * (num_pieces_correct_side(next_state) < num_pieces_correct_side(state))
        if (next_state.__hash__(), action) in self.QV.keys():
            reward = -0.2
        reward -= solved_sides
        # print(reward)
        reward -= solved_pieces
        # print(reward)
        return reward

    def max_reward(self, state, action):
        new_state = move(state, action)
        if not new_state in self.R.keys():
            self.R[new_state] = []
            for action in self.actions:
                self.R[new_state].append(self.reward(new_state, action))
        return max(self.R[new_state])

def study(agent):
    # print(agent)
    print("REGISTERING PATTERN DATABASE, THIS WILL TAKE A LITTLE WHILE")
    agent.register_patterns()
    Epsilons = [i/ 50 for i in range(50)]
    Epsilons.reverse()
    for i in range(2):
        for j, e in enumerate(Epsilons):
            print("======= ROUND " + str(j) + "=========")
            agent.QLearn(epsilon=e)
    print("there are " + str(len(agent.QV)) + " keys in Q Table")
    return

    
# cubes, _ = n_move_state(n=6)
# agent = Core(start=cubes)
# study(agent)
# while True:
#     save_action = []
#     put = input("nhập số bất kì: ")
#     state_random, act = n_move_state(n=8)
#     print(act)
#     event = agent.Play(state_random, save_action)
#     # # agent.print_()
#     print(save_action)