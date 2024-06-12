from queue import Queue
import random


class Logic:

    def __init__(self, mat):
        # current_score = 0
        self.possible_next_states = Queue(maxsize=480)
        count = 0
        while count < 2:
            row_ind = random.randint(0, 3)
            col_ind = random.randint(0, 3)
            if mat[row_ind][col_ind] == 0:
                mat[row_ind][col_ind] = 2
                count += 1

    @staticmethod
    def check_2048(mat) -> bool:
        for row in range(4):
            for col in range(4):
                if mat[row][col] == 2048:
                    return True
        return False

    @staticmethod
    def get_zero_indices_list(mat) -> list:
        index_zeros = []
        for row in range(4):
            for col in range(4):
                if mat[row][col] == 0:
                    index_zeros.append((row, col))
        return index_zeros

    # function to add a new 2 in grid using vertical scan
    @staticmethod
    def add_new_2(mat):
        new_num_added = False
        for row_index in range(4):
            for col_index in range(4):
                if mat[row_index][col_index] == 0:
                    mat[row_index][col_index] = 2
                    new_num_added = True
                    break
            if new_num_added:
                break
        return mat

    # function to add a new 4 in grid using vertical scan
    @staticmethod
    def add_new_4(mat):
        new_num_added = False
        for row_index in range(4):
            for col_index in range(4):
                if mat[row_index][col_index] == 0:
                    mat[row_index][col_index] = 4
                    new_num_added = True
                    break
            if new_num_added:
                break
        return mat

    # function used to move cells data to left extremes.
    @staticmethod
    def compress(mat):
        changed = False  # defines diff b/w mat and new_mat
        new_mat = []
        # init with 0's
        for row in range(4):
            new_mat.append([0] * 4)

        # shift entries of each cell to it's extreme left
        for row in range(4):
            pos = 0
            for col in range(4):
                if mat[row][col] != 0:
                    new_mat[row][pos] = mat[row][col]
                    if col != pos:
                        changed = True
                    pos += 1
        return new_mat, changed

    # function to merge the consecutive cells with same number
    @staticmethod
    def merge(mat, total_cost):
        changed = False  # defines whether any merges done or not
        cost = total_cost

        for i in range(4):
            for j in range(3):
                # 2 consecutive cells with same non-zero value
                if mat[i][j] == mat[i][j + 1] and mat[i][j] != 0:
                    # double current cell value and empty the next cell
                    cost += mat[i][j] * 2
                    mat[i][j] = mat[i][j] * 2
                    mat[i][j + 1] = 0
                    changed = True

        return mat, changed, cost

    # function to reverse the matrix
    @staticmethod
    def reverse(mat):
        new_mat = []
        for i in range(4):
            new_mat.append([])
            for j in range(4):
                new_mat[i].append(mat[i][3 - j])
        return new_mat

    # function to get transpose of matrix
    @staticmethod
    def transpose(mat):
        new_mat = []
        for i in range(4):
            new_mat.append([])
            for j in range(4):
                new_mat[i].append(mat[j][i])
        return new_mat

    # function to update the matrix for move / swipe left
    def swipe_left(self, grid, total_cost):  # left = compress + merge + compress
        new_grid, changed1 = self.compress(grid)
        new_grid, changed2, cost = self.merge(new_grid, total_cost)
        changed = changed1 or changed2
        new_grid, temp = self.compress(new_grid)
        return new_grid, changed, cost

    # function to update the matrix for move / swipe right
    def swipe_right(self, grid, total_cost):  # right = reverse + left + reverse
        new_grid = self.reverse(grid)
        new_grid, changed, cost = self.swipe_left(new_grid, total_cost)
        new_grid = self.reverse(new_grid)
        return new_grid, changed, cost

    # function to update the matrix for move / swipe up
    def swipe_up(self, grid, total_cost):  # up = transpose + left + transpose
        new_grid = self.transpose(grid)
        new_grid, changed, cost = self.swipe_left(new_grid, total_cost)
        new_grid = self.transpose(new_grid)
        return new_grid, changed, cost

    # function to update the matrix for move / swipe down
    def swipe_down(self, grid, total_cost):  # down = transpose + right + transpose
        new_grid = self.transpose(grid)
        new_grid, changed, cost = self.swipe_right(new_grid, total_cost)
        new_grid = self.transpose(new_grid)
        return new_grid, changed, cost

    def get_next_states(self, current_states):
        while not current_states.empty():
            node = current_states.get()
            # node_mat = list(map(list, node['matrix']))
            tot_cost = node['total_cost']   # cost required to reach that node from root.
            path = node['path']
            previous_score = node['current_score']
            zero_indices = self.get_zero_indices_list(mat)
            if len(zero_indices) == 0:
                swipe_up_mat, swipe_up_flag, curr_swipe_up_cost = logic.swipe_up(node_mat, 0)
                swipe_down_mat, swipe_down_flag, curr_swipe_down_cost = logic.swipe_down(node_mat, 0)
                swipe_left_mat, swipe_left_flag, curr_swipe_left_cost = logic.swipe_left(node_mat, 0)
                swipe_right_mat, swipe_right_flag, curr_swipe_right_cost = logic.swipe_right(node_mat, 0)
                if swipe_up_mat != node_mat:
                    self.possible_next_states.put({'matrix': tuple(map(tuple, swipe_up_mat)), 'current_score': curr_swipe_up_cost, 'previous_score': previous_score, 'parent_matrix': tuple(map(tuple, node_mat)), 'path': path + ",U", 'total_cost': tot_cost + curr_swipe_up_cost})
                if swipe_down_mat != node_mat:
                    self.possible_next_states.put({'matrix': tuple(map(tuple, swipe_down_mat)), 'current_score': curr_swipe_down_cost, 'previous_score': previous_score, 'parent_matrix': tuple(map(tuple, node_mat)), 'path': path + ",D", 'total_cost': tot_cost + curr_swipe_down_cost})
                if swipe_left_mat != node_mat:
                    self.possible_next_states.put({'matrix': tuple(map(tuple, swipe_left_mat)), 'current_score': curr_swipe_left_cost, 'previous_score': previous_score, 'parent_matrix': tuple(map(tuple, node_mat)), 'path': path + ",L", 'total_cost': tot_cost + curr_swipe_left_cost})
                if swipe_right_mat != node_mat:
                    self.possible_next_states.put({'matrix': tuple(map(tuple, swipe_right_mat)), 'current_score': curr_swipe_right_cost, 'previous_score': previous_score, 'parent_matrix': tuple(map(tuple, node_mat)), 'path': path + ",R", 'total_cost': tot_cost + curr_swipe_right_cost})
            else:
                for each_zero in zero_indices:
                    node_mat = list(map(list, node['matrix']))
                    node_mat[each_zero[0]][each_zero[1]] = 2
                    swipe_up_mat, swipe_up_flag, curr_swipe_up_cost = logic.swipe_up(node_mat, 0)
                    swipe_down_mat, swipe_down_flag, curr_swipe_down_cost = logic.swipe_down(node_mat, 0)
                    swipe_left_mat, swipe_left_flag, curr_swipe_left_cost = logic.swipe_left(node_mat, 0)
                    swipe_right_mat, swipe_right_flag, curr_swipe_right_cost = logic.swipe_right(node_mat, 0)
                    if swipe_up_mat != node_mat:
                        self.possible_next_states.put({'matrix': tuple(map(tuple, swipe_up_mat)), 'current_score': curr_swipe_up_cost, 'previous_score': previous_score, 'parent_matrix': tuple(map(tuple, node_mat)), 'path': path + ",U", 'total_cost': tot_cost + curr_swipe_up_cost})
                    if swipe_down_mat != node_mat:
                        self.possible_next_states.put({'matrix': tuple(map(tuple, swipe_down_mat)), 'current_score': curr_swipe_down_cost, 'previous_score': previous_score, 'parent_matrix': tuple(map(tuple, node_mat)), 'path': path + ",D", 'total_cost': tot_cost + curr_swipe_down_cost})
                    if swipe_left_mat != node_mat:
                        self.possible_next_states.put({'matrix': tuple(map(tuple, swipe_left_mat)), 'current_score': curr_swipe_left_cost, 'previous_score': previous_score, 'parent_matrix': tuple(map(tuple, node_mat)), 'path': path + ",L", 'total_cost': tot_cost + curr_swipe_left_cost})
                    if swipe_right_mat != node_mat:
                        self.possible_next_states.put({'matrix': tuple(map(tuple, swipe_right_mat)), 'current_score': curr_swipe_right_cost, 'previous_score': previous_score, 'parent_matrix': tuple(map(tuple, node_mat)), 'path': path + ",R", 'total_cost': tot_cost + curr_swipe_right_cost})
                    node_mat = list(map(list, node['matrix']))
                    node_mat[each_zero[0]][each_zero[1]] = 4
                    up_mat, up_flag, curr_swipe_up_cost = logic.swipe_up(node_mat, 0)
                    down_mat, down_flag, curr_swipe_down_cost = logic.swipe_down(node_mat, 0)
                    left_mat, left_flag, curr_swipe_left_cost = logic.swipe_left(node_mat, 0)
                    right_mat, right_flag, curr_swipe_right_cost = logic.swipe_right(node_mat, 0)
                    if up_mat != node_mat:
                        self.possible_next_states.put({'matrix': tuple(map(tuple, up_mat)), 'current_score': curr_swipe_up_cost, 'previous_score': previous_score, 'parent_matrix': tuple(map(tuple, node_mat)), 'path': path + ",U", 'total_cost': tot_cost + curr_swipe_up_cost})
                    if down_mat != node_mat:
                        self.possible_next_states.put({'matrix': tuple(map(tuple, down_mat)), 'current_score': curr_swipe_down_cost, 'previous_score': previous_score, 'parent_matrix': tuple(map(tuple, node_mat)), 'path': path + ",D", 'total_cost': tot_cost + curr_swipe_down_cost})
                    if left_mat != node_mat:
                        self.possible_next_states.put({'matrix': tuple(map(tuple, left_mat)), 'current_score': curr_swipe_left_cost, 'previous_score': previous_score, 'parent_matrix': tuple(map(tuple, node_mat)), 'path': path + ",L", 'total_cost': tot_cost + curr_swipe_left_cost})
                    if right_mat != node_mat:
                        self.possible_next_states.put({'matrix': tuple(map(tuple, right_mat)), 'current_score': curr_swipe_right_cost, 'previous_score': previous_score, 'parent_matrix': tuple(map(tuple, node_mat)), 'path': path + ",R", 'total_cost': tot_cost + curr_swipe_right_cost})


if __name__ == '__main__':
    mat = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]  # mat loaded with 0's
    logic = Logic(mat)  # Matrix initialise with random two 2's
    result = ""
    plays = 100
    total_cost = 0
    found_2048 = False
    current_possible_moves = Queue(maxsize=4)
    swipe_up_mat, up_flag, curr_swipe_up_cost = logic.swipe_up(mat, 0)
    swipe_down_mat, down_flag, curr_swipe_down_cost = logic.swipe_down(mat, 0)
    swipe_left_mat, left_flag, curr_swipe_left_cost = logic.swipe_left(mat, 0)
    swipe_right_mat, right_flag, curr_swipe_right_cost = logic.swipe_right(mat, 0)

    current_possible_moves.put({'matrix': tuple(map(tuple, swipe_up_mat)), 'current_score': curr_swipe_up_cost, 'previous_score': 0, 'parent_matrix': tuple(map(tuple, mat)), 'path': result + ",U", 'total_cost': total_cost + curr_swipe_up_cost})
    current_possible_moves.put({'matrix': tuple(map(tuple, swipe_down_mat)), 'current_score': curr_swipe_down_cost, 'previous_score': 0, 'parent_matrix': tuple(map(tuple, mat)), 'path': result + ",D", 'total_cost': total_cost + curr_swipe_down_cost})
    current_possible_moves.put({'matrix': tuple(map(tuple, swipe_left_mat)), 'current_score': curr_swipe_left_cost, 'previous_score': 0, 'parent_matrix': tuple(map(tuple, mat)), 'path': result + ",L", 'total_cost': total_cost + curr_swipe_left_cost})
    current_possible_moves.put({'matrix': tuple(map(tuple, swipe_right_mat)), 'current_score': curr_swipe_right_cost, 'previous_score': 0, 'parent_matrix': tuple(map(tuple, mat)), 'path': result + ",R", 'total_cost': total_cost + curr_swipe_right_cost})

    while (plays > 0) & (not found_2048):
        logic.possible_next_states.queue.clear()
        logic.get_next_states(current_possible_moves)
        leaves = list(logic.possible_next_states.queue)
        if len(leaves) == 0:
            print("GAME OVER! NO POSSIBLE MOVE")
            break
        backup_leaves = []
        randLocalFound = False
        while (not randLocalFound) & (len(leaves) != 0):
            next_state = leaves[random.randint(0, len(leaves)-1)]
            if next_state['current_score'] + next_state['previous_score'] > 0:
                print("The new next state is:", next_state, " plays remaining:", plays)
                randLocalFound = True
                # mat = next_state['parent_matrix']
                current_possible_moves.queue.clear()
                # new_possible_moves = list(filter(lambda x: x['parent_matrix'] == mat, leaves))
                # for each in new_possible_moves:
                    # current_possible_moves.put(each)
                    # print(each)
                current_possible_moves.put(next_state)
            else:
                leaves.remove(next_state)
                backup_leaves.append(next_state)

        if len(leaves) == 0:    # this check to choose randomly one node when all nodes have current and next scores as zeros for all nodes.
            next_state = leaves[random.randint(0, len(leaves)-1)]
            print("The new next state is:", next_state, " plays remaining:", plays)
            # mat = next_state['parent_matrix']
            current_possible_moves.queue.clear()
            # new_possible_moves = list(filter(lambda x: x['parent_matrix'] == mat, leaves))
            # for each in new_possible_moves:
                # current_possible_moves.put(each)
            current_possible_moves.put(next_state)
        found_2048 = logic.check_2048(next_state['matrix'])
        leaves.clear()
        backup_leaves.clear()
        plays -= 1

        # max_cost_node = max(leaves, key=lambda x: x['total_cost'])
        # output = str(max_cost_node['total_cost']) + max_cost_node['path'] + "\n"

