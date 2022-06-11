from copy import deepcopy

class State:
    def __init__(self, arrangement, goal, total_num):
        self.arrangement = arrangement
        self.goal = goal
        self.n_block = total_num

    def delta(self):
        # calculate the number of blocks that are in the correct position 
        n_correct_position = 0
        for current_stack in self.arrangement:
            for goal_stack in self.goal:
                i = 0
                flag = 0
                current_stack_len = len(current_stack)
                goal_stack_len = len(goal_stack)
                min_len = min(current_stack_len, goal_stack_len)
                while i < min_len and min_len > 0 and flag == 0:
                    # check from the bottom to the top of the stack
                    if current_stack[i] == goal_stack[i]:
                        n_correct_position += 1
                    # move to another stack when the current block position doesn't match the goal state
                    else: flag = 1
                    i += 1

        return self.n_block - n_correct_position

class BlockWorldAgent:
    def __init__(self):
        pass

    def solve(self, initial_arrangement, goal_arrangement):
        self.goal = goal_arrangement
        self.solution = []

        # calculate the total number of blocks
        n_blocks = 0
        for stack in initial_arrangement:
            n_blocks += len(stack)
        self.n_blocks = n_blocks

        # set initial state
        self.current_state = State(initial_arrangement, self.goal, self.n_blocks)
        
        # check if goal is reached
        while self.current_state.delta() != 0:
            self.current_state, move = self.generate_new_state()
            self.solution.append(move)

        # return the moves taken to reach the goal state
        return self.solution

    def generate_new_state(self): 
        current_arrangement = self.current_state.arrangement
        # get the number of stacks in the current arrangement
        n_stacks = len(current_arrangement)

        for idx_1 in range(n_stacks):
            # skip if block is already on the table
            if len(current_arrangement[idx_1]) > 1: 
                possible_arrangement, possible_move = self.move_to_block_table(idx_1)  
                new_state = State(possible_arrangement, self.goal, self.n_blocks)
                # check if new state is optimal
                if new_state.delta() <= self.current_state.delta():
                    return new_state, possible_move
            # loop through all stacks, and move the top block onto other stacks
            for idx_2 in range(n_stacks):
                stack_1 = current_arrangement[idx_1]
                stack_2 = current_arrangement[idx_2]
                if idx_1 != idx_2 and len(stack_1) > 0 and len(stack_2) > 0:
                    possible_arrangement, possible_move = self.move_block_to_another_stack(idx_1, idx_2)
                    new_state = State(possible_arrangement, self.goal, self.n_blocks)
                    # check if new state is optimal
                    if new_state.delta() < self.current_state.delta():
                        return new_state, possible_move

    def move_block_to_another_stack(self, idx_1, idx_2):
        new_arrangement = deepcopy(self.current_state.arrangement)
        top_block = new_arrangement[idx_1].pop()
        # move the top block to another stack
        move = (top_block, new_arrangement[idx_2][-1])
        new_arrangement[idx_2].append(top_block)
        if len(new_arrangement[idx_1]) == 0:
            new_arrangement.remove(new_arrangement[idx_1])
        return new_arrangement, move
    
    def move_to_block_table(self, idx):
        new_arrangement = deepcopy(self.current_state.arrangement)
        top_block = new_arrangement[idx].pop()
        new_arrangement.append([top_block])
        move = (top_block, 'Table')
        return new_arrangement, move

    
   
