from queue import Queue
import random
class Logic:
    def __init__(self, mat):
        self.possible_next_state = Queue(maxsize=480)
        count = 0
        while count < 2:
            row_ind = random.randint(0, 3)
            column_ind = random.randint(0, 3)
            if mat[row_ind][column_ind] == 0:
                mat[row_ind][column_ind] = 2
                count += 1

    @staticmethod
    def checking_2048(mat) -> bool:
        for row in range(4):
            for col in range(4):
                if mat[row][col] == 2048:
                    return True
        return False
    @staticmethod
    def getting_zero_indice_lists(mat) -> list:
        index_zeros = []
        for row in range(4):
            for col in range(4):
                if mat[row][col] == 0:
                    index_zeros.append((row, col))
        return index_zeros
    @staticmethod
    def adding_new_2(mat):
        new_number_added = False
        for row_index in range(4):
            for column_ind in range(4):
                if mat[row_index][column_ind] == 0:
                    mat[row_index][column_ind] = 2
                    new_number_added = True
                    break
            if new_number_added:
                break
        return mat

    @staticmethod
    def adding_new_4(mat):
        new_number_added = False
        for row_index in range(4):
            for column_ind in range(4):
                if mat[row_index][column_ind] == 0:
                    mat[row_index][column_ind] = 4
                    new_number_added = True
                    break
            if new_number_added:
                break
        return mat

    @staticmethod
    def compression(mat):
        changed = False 
        new_matrix = []
        for row in range(4):
            new_matrix.append([0] * 4)
        for row in range(4):
            pos = 0
            for col in range(4):
                if mat[row][col] != 0:
                    new_matrix[row][pos] = mat[row][col]
                    if col != pos:
                        changed = True
                    pos += 1
        return new_matrix, changed

    
    @staticmethod
    def merging(mat, total_cost):
        changed = False 
        cost = total_cost
        for i in range(4):
            for j in range(3):
                if mat[i][j] == mat[i][j + 1] and mat[i][j] != 0:
                    cost += mat[i][j] * 2
                    mat[i][j] = mat[i][j] * 2
                    mat[i][j + 1] = 0
                    changed = True
        return mat, changed, cost

    
    @staticmethod
    def reversing(mat):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(mat[i][3 - j])
        return new_matrix

   
    @staticmethod
    def transposing(mat):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(mat[j][i])
        return new_matrix

    
    def swipe_left(self, grid, total_cost):  
        new_grid, changed1 = self.compression(grid)
        new_grid, changed2, cost = self.merging(new_grid, total_cost)
        changed = changed1 or changed2
        new_grid, temp = self.compression(new_grid)
        return new_grid, changed, cost

   
    def swipe_right(self, grid, total_cost):  
        new_grid = self.reversing(grid)
        new_grid, changed, cost = self.swipe_left(new_grid, total_cost)
        new_grid = self.reversing(new_grid)
        return new_grid, changed, cost

   
    def swipe_up(self, grid, total_cost): 
        new_grid = self.transposing(grid)
        new_grid, changed, cost = self.swipe_left(new_grid, total_cost)
        new_grid = self.transposing(new_grid)
        return new_grid, changed, cost

   
    def swipe_down(self, grid, total_cost): 
        new_grid = self.transposing(grid)
        new_grid, changed, cost = self.swipe_right(new_grid, total_cost)
        new_grid = self.transposing(new_grid)
        return new_grid, changed, cost

    def getting_next_states(self, current_states):
        while not current_states.empty():
            node = current_states.get()
            node_mat = list(map(list, node['matrix']))
            tot_cost = node['total_cost']   
            path = node['path']
            previous_score = node['current_score']
            zero_indices = self.getting_zero_indice_lists(node_mat)
            if len(zero_indices) == 0:  
                swipe_up_mat, swipe_up_flag, curr_swipe_up_cost = self.swipe_up(node_mat, 0)
                swipe_down_mat, swipe_down_flag, curr_swipe_down_cost = self.swipe_down(node_mat, 0)
                swipe_left_mat, swipe_left_flag, curr_swipe_left_cost = self.swipe_left(node_mat, 0)
                swipe_right_mat, swipe_right_flag, curr_swipe_right_cost = self.swipe_right(node_mat, 0)
                if swipe_up_mat != node_mat:
                    self.possible_next_state.put({'matrix': tuple(map(tuple, swipe_up_mat)), 'current_score': curr_swipe_up_cost, 'previous_score': previous_score, 'parent_matrix': tuple(map(tuple, node_mat)), 'path': path + ",U", 'total_cost': tot_cost + curr_swipe_up_cost})
                if swipe_down_mat != node_mat:
                    self.possible_next_state.put({'matrix': tuple(map(tuple, swipe_down_mat)), 'current_score': curr_swipe_down_cost, 'previous_score': previous_score, 'parent_matrix': tuple(map(tuple, node_mat)), 'path': path + ",D", 'total_cost': tot_cost + curr_swipe_down_cost})
                if swipe_left_mat != node_mat:
                    self.possible_next_state.put({'matrix': tuple(map(tuple, swipe_left_mat)), 'current_score': curr_swipe_left_cost, 'previous_score': previous_score, 'parent_matrix': tuple(map(tuple, node_mat)), 'path': path + ",L", 'total_cost': tot_cost + curr_swipe_left_cost})
                if swipe_right_mat != node_mat:
                    self.possible_next_state.put({'matrix': tuple(map(tuple, swipe_right_mat)), 'current_score': curr_swipe_right_cost, 'previous_score': previous_score, 'parent_matrix': tuple(map(tuple, node_mat)), 'path': path + ",R", 'total_cost': tot_cost + curr_swipe_right_cost})
            else:
                for each_zero in zero_indices:
                    node_mat = list(map(list, node['matrix']))
                    node_mat[each_zero[0]][each_zero[1]] = 2
                    swipe_up_mat, swipe_up_flag, curr_swipe_up_cost = self.swipe_up(node_mat, 0)
                    swipe_down_mat, swipe_down_flag, curr_swipe_down_cost = self.swipe_down(node_mat, 0)
                    swipe_left_mat, swipe_left_flag, curr_swipe_left_cost = self.swipe_left(node_mat, 0)
                    swipe_right_mat, swipe_right_flag, curr_swipe_right_cost = self.swipe_right(node_mat, 0)
                    if swipe_up_mat != node_mat:
                        self.possible_next_state.put({'matrix': tuple(map(tuple, swipe_up_mat)), 'current_score': curr_swipe_up_cost, 'previous_score': previous_score, 'parent_matrix': tuple(map(tuple, node_mat)), 'path': path + ",U", 'total_cost': tot_cost + curr_swipe_up_cost})
                    if swipe_down_mat != node_mat:
                        self.possible_next_state.put({'matrix': tuple(map(tuple, swipe_down_mat)), 'current_score': curr_swipe_down_cost, 'previous_score': previous_score, 'parent_matrix': tuple(map(tuple, node_mat)), 'path': path + ",D", 'total_cost': tot_cost + curr_swipe_down_cost})
                    if swipe_left_mat != node_mat:
                        self.possible_next_state.put({'matrix': tuple(map(tuple, swipe_left_mat)), 'current_score': curr_swipe_left_cost, 'previous_score': previous_score, 'parent_matrix': tuple(map(tuple, node_mat)), 'path': path + ",L", 'total_cost': tot_cost + curr_swipe_left_cost})
                    if swipe_right_mat != node_mat:
                        self.possible_next_state.put({'matrix': tuple(map(tuple, swipe_right_mat)), 'current_score': curr_swipe_right_cost, 'previous_score': previous_score, 'parent_matrix': tuple(map(tuple, node_mat)), 'path': path + ",R", 'total_cost': tot_cost + curr_swipe_right_cost})
                    node_mat = list(map(list, node['matrix']))
                    node_mat[each_zero[0]][each_zero[1]] = 4
                    up_mat, up_flag, curr_swipe_up_cost = self.swipe_up(node_mat, 0)
                    down_mat, down_flag, curr_swipe_down_cost = self.swipe_down(node_mat, 0)
                    left_mat, left_flag, curr_swipe_left_cost = self.swipe_left(node_mat, 0)
                    right_mat, right_flag, curr_swipe_right_cost = self.swipe_right(node_mat, 0)
                    if up_mat != node_mat:
                        self.possible_next_state.put({'matrix': tuple(map(tuple, up_mat)), 'current_score': curr_swipe_up_cost, 'previous_score': previous_score, 'parent_matrix': tuple(map(tuple, node_mat)), 'path': path + ",U", 'total_cost': tot_cost + curr_swipe_up_cost})
                    if down_mat != node_mat:
                        self.possible_next_state.put({'matrix': tuple(map(tuple, down_mat)), 'current_score': curr_swipe_down_cost, 'previous_score': previous_score, 'parent_matrix': tuple(map(tuple, node_mat)), 'path': path + ",D", 'total_cost': tot_cost + curr_swipe_down_cost})
                    if left_mat != node_mat:
                        self.possible_next_state.put({'matrix': tuple(map(tuple, left_mat)), 'current_score': curr_swipe_left_cost, 'previous_score': previous_score, 'parent_matrix': tuple(map(tuple, node_mat)), 'path': path + ",L", 'total_cost': tot_cost + curr_swipe_left_cost})
                    if right_mat != node_mat:
                        self.possible_next_state.put({'matrix': tuple(map(tuple, right_mat)), 'current_score': curr_swipe_right_cost, 'previous_score': previous_score, 'parent_matrix': tuple(map(tuple, node_mat)), 'path': path + ",R", 'total_cost': tot_cost + curr_swipe_right_cost})


def min_max_algorithm(maximiservalue):
    mat = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]] 
    logic = Logic(mat) 
    result = ""
    total_cost = 0
    finds_2048 = False
    current_possible_move = Queue(maxsize=4)
    swipe_up_mat, up_flag, curr_swipe_up_cost = logic.swipe_up(mat, 0)
    swipe_down_mat, down_flag, curr_swipe_down_cost = logic.swipe_down(mat, 0)
    swipe_left_mat, left_flag, curr_swipe_left_cost = logic.swipe_left(mat, 0)
    swipe_right_mat, right_flag, curr_swipe_right_cost = logic.swipe_right(mat, 0)

    current_possible_move.put({'matrix': tuple(map(tuple, swipe_up_mat)), 'current_score': curr_swipe_up_cost, 'previous_score': 0, 'parent_matrix': tuple(map(tuple, mat)), 'path': result + ",U", 'total_cost': total_cost + curr_swipe_up_cost})
    current_possible_move.put({'matrix': tuple(map(tuple, swipe_down_mat)), 'current_score': curr_swipe_down_cost, 'previous_score': 0, 'parent_matrix': tuple(map(tuple, mat)), 'path': result + ",D", 'total_cost': total_cost + curr_swipe_down_cost})
    current_possible_move.put({'matrix': tuple(map(tuple, swipe_left_mat)), 'current_score': curr_swipe_left_cost, 'previous_score': 0, 'parent_matrix': tuple(map(tuple, mat)), 'path': result + ",L", 'total_cost': total_cost + curr_swipe_left_cost})
    current_possible_move.put({'matrix': tuple(map(tuple, swipe_right_mat)), 'current_score': curr_swipe_right_cost, 'previous_score': 0, 'parent_matrix': tuple(map(tuple, mat)), 'path': result + ",R", 'total_cost': total_cost + curr_swipe_right_cost})

    while (not current_possible_move.empty()) & (not finds_2048):
        logic.possible_next_state.queue.clear()
        logic.getting_next_states(current_possible_move)
        current_possible_move.queue.clear()
        moves = list(logic.possible_next_state.queue)
        if len(moves) == 0:
            print("GAME OVER! NO POSSIBLE MOVE")
            print("The final score: ", next_state['total_cost'])
            print("The sequence of moves: ", next_state['path'][1:])
            print("The final arrangement of numbers:")
            for row in next_state['matrix']:
                print(row)
            print()
            break
       
        maximum_or_minimum_localfound = False
        while (not maximum_or_minimum_localfound) & (len(moves) != 0):
            if maximiservalue:
               
                next_state = max(moves, key=lambda x: x['current_score'] + x['previous_score'])
                maximiservalue = False
            else:
               
                next_state = min(moves, key=lambda x: x['current_score'] + x['previous_score'])
                maximiservalue = True
            cost = next_state['current_score'] + next_state['previous_score']
            new_possible_moves = list(filter(lambda x: x['current_score'] + x['previous_score'] == cost, moves))
            next_state = new_possible_moves[random.randint(0, len(new_possible_moves)-1)]
            maximum_or_minimum_localfound = True
            current_possible_move.put(next_state)
        finds_2048 = logic.checking_2048(next_state['matrix'])
        moves.clear()
      

    if finds_2048:
        print("2048 is found")
        print("The final score is: ", next_state['total_cost'])
        print("The sequence of moves are: ", next_state['path'][1:])
        print("The final arrangement of numbers is:")
        for row in next_state['matrix']:
            print(row)
        print()


if __name__ == '__main__':
    print("We will consider depth as 2")
    min_max_algorithm(True)

