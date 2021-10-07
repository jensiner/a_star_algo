import copy

class State:
    def __init__(self, grid, depth=None):
        self.grid = grid
        self.fn = []
        self.depth = depth
        self.actions = []

    def current_fn(self):
        return self.fn[len(self.fn)-1]

    def printgrid(self):
        print(self.grid)


class PriorityQueue:
    def __init__(self):
        self.queue = []

    def __str__(self):
        return ''.join([str(i.grid) for i in self.queue])

    def getlength(self):
        return len(self.queue)

    def isEmpty(self):
        return len(self.queue) == 0

    def insert(self, data):
        self.queue.append(data)

    def delete(self):
        try:
            min = 0
            for i in range(len(self.queue)):
                if self.queue[i].current_fn() < self.queue[min].current_fn():
                    min = i
            item = self.queue[min]
            del self.queue[min]
            return item
        except IndexError:
            print()
            exit()

# take a txt file
def readfile(file):
    input_file = open(file, "r")
    file_content = []
    for line in input_file:
        for word in line.split():
            file_content.append(word)
    input_file.close()
    return file_content


# create 2 2D arrays: one initial state and the other goal state
def create_states(file_content):
    initial_state = []
    goal_state = []
    for i in range(len(file_content)):
        if i == 0 or i == 4 or i == 8 or i == 12:
            initial_state.append([])
        if i < 4:
            initial_state[0].append(file_content[i])
        if 3 < i < 8:
            initial_state[1].append(file_content[i])
        if 7 < i < 12:
            initial_state[2].append(file_content[i])
        if 11 < i < 16:
            initial_state[3].append(file_content[i])
        if i == 16 or i == 20 or i == 24 or i == 28:
            goal_state.append([])
        if 15 < i < 20:
            goal_state[0].append(file_content[i])
        if 19 < i < 24:
            goal_state[1].append(file_content[i])
        if 23 < i < 28:
            goal_state[2].append(file_content[i])
        if 27 < i:
            goal_state[3].append(file_content[i])
    return initial_state, goal_state


def h(current_state, goal_state):
    hn_total = 0
    # count h(n) using chessboard distance of tiles from goal state

    # for each tile in current state
    for i in range(4):
        for j in range(4):
            # find the tile in goal state, get index
            for goal_i in range(4):
                for goal_j in range(4):
                    if (current_state.grid[i][j] == goal_state.grid[goal_i][goal_j]) and current_state.grid[i][j] != '0':
                        x = abs(goal_i - i)
                        y = abs(goal_j - j)
                        hn_total = hn_total + max(x, y)
    # return sum
    return hn_total


# returns f(n) value
def f(current_state, hn_total):
    return current_state.depth + hn_total


def find_empty_tile(current_state):
    # returns index of empty tile
    empty_tile = None
    while empty_tile is None:
        for i in range(4):
            for j in range(4):
                if current_state.grid[i][j] == '0':
                    empty_tile = i, j
                    return i, j

def possible_moves(current_state, goal_state, seen_states, i, j, p_queue):
    # calculate move options (make sure have not already seen)
    moves = [-1, 0, 1]

    for a in range(len(moves)):
        for b in range(len(moves)):
            x = i + moves[a]
            y = j + moves[b]
            if (x, y) != (i, j) and -1 < x < 4 and -1 < y < 4:
                # define action taken
                if x == i and y == j - 1:
                    action = 1
                elif x == i - 1 and y == j - 1:
                    action = 2
                elif x == i - 1 and y == j:
                    action = 3
                elif x == i - 1 and y == j + 1:
                    action = 4
                elif x == i and y == j + 1:
                    action = 5
                elif x == i + 1 and y == j + 1:
                    action = 6
                elif x == i + 1 and y == j:
                    action = 7
                else:
                    action = 8
                # make move and create new State
                new_grid = copy.deepcopy(current_state)
                new_grid.grid[i][j] = current_state.grid[x][y]  # make move
                new_grid.grid[x][y] = current_state.grid[i][j]  # replace previous tile with '0'
                # make sure not in seen_states
                seen = False
                for item in seen_states:
                    if new_grid.grid == item.grid:
                        seen = True

                if not seen:
                    # add action and depth
                    new_grid.actions.append(action)
                    new_grid.depth = new_grid.depth + 1
                    # calculate fn
                    hn = h(new_grid, goal_state)
                    new_grid.fn.append(f(new_grid, hn))
                    # add to queue
                    p_queue.insert(new_grid)
                    seen_states.append(new_grid)
    return


def Astar_search(initial_state, goal_state, p_queue):
    # implement function
    current_state = initial_state
    seen_states = [initial_state]

    while current_state.grid != goal_state.grid:
        # identify '0' in current_state
        i, j = find_empty_tile(current_state)

        # change current_state to state with fewest f(n) based on queue
        possible_moves(current_state, goal_state, seen_states, i, j, p_queue)
        current_state = p_queue.delete()

    return current_state.depth, len(seen_states), current_state.actions, current_state.fn

# write to txt file
def writefile(file, depth, N, actions, fns):
    f = open(file, "a")
    f.write('\n')
    # write depth level
    # write number of nodes generates
    f.write('\n' + str(depth) + '\n' + str(N) + '\n')
    # write sequence of actions
    for item in actions:
        f.write(str(item) + " ")
    f.write('\n')
    # write values of fn
    for fn in fns:
        f.write(str(fn) + " ")

    f.close()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # read from file content to initialize initial and goal states
    file_content = readfile("Input1.txt")
    initial_state, goal_state = create_states(file_content)

    # create State objects using content read
    Goal = State(goal_state)
    Initial = State(initial_state, 0)

    # find fn of Initial
    hn_total = h(Initial, Goal)
    fn = f(Initial, hn_total)
    Initial.fn.append(fn)

    # initialize queue
    frontier = PriorityQueue()

    # run A* search algorithm
    d, N, actions, fns = Astar_search(Initial, Goal, frontier)
    # write to file
    writefile("Input1.txt", d, N, actions, fns)

    file_content2 = readfile("Input2.txt")
    initial_state2, goal_state2 = create_states(file_content2)
    Goal2 = State(goal_state2)
    Initial2 = State(initial_state2, 0)
    hn_total2 = h(Initial2, Goal2)
    fn2 = f(Initial2, hn_total2)
    Initial2.fn.append(fn2)
    frontier2 = PriorityQueue()
    d2, N2, actions2, fns2 = Astar_search(Initial2, Goal2, frontier2)
    writefile("Input2.txt", d2, N2, actions2, fns2)

    file_content3 = readfile("Input3.txt")
    initial_state3, goal_state3 = create_states(file_content3)
    Goal3 = State(goal_state3)
    Initial3 = State(initial_state3, 0)
    hn_total3 = h(Initial3, Goal3)
    fn3 = f(Initial3, hn_total3)
    Initial3.fn.append(fn3)
    frontier3 = PriorityQueue()
    d3, N3, actions3, fns3 = Astar_search(Initial3, Goal3, frontier3)
    writefile("Input3.txt", d3, N3, actions3, fns3)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
