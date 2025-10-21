import heapq
import sys
from collections import deque

maze = [
    ["S", ".", ".", "#"],
    ["#", "#", ".", "#"],
    [".", ".", ".", "G"],
]


class MazeSolver:
    def __init__(self, maze, start, goal):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.actions = [
            (0, -1),
            (0, 1),
            (-1, 0),
            (1, 0),
        ]  # ["up", "down", "left", "right"]
        self.start = start
        self.goal = goal

    # function to check if a cell is within the confines of the 2D array of the maze. e.g. (-1, 0) is invalid
    def is_cell_valid(self, cell):
        cell_row, cell_col = cell[0], cell[1]
        rows, cols = self.rows, self.cols

        if not (0 <= cell_row < rows):
            return False
        return 0 <= cell_col < cols

    # function that constructs the path after the goal is found
    def construct_path(self, parent_mappings):
        path = []
        current = self.goal

        while current is not None:
            path.append(current)
            current = parent_mappings[current]

        path.reverse()
        return path

    # generate the frontiers of a node/cell
    def expand_cell(self, cell):
        if self.maze[cell[0]][cell[1]] == "#":
            return None

        new_cells = []

        for i in self.actions:
            new_cell = (cell[0] + i[0], cell[1] + i[1])

            if self.is_cell_valid(new_cell):
                new_cells.append(new_cell)

        return new_cells

    # bfs search to find the path
    def bfs(self):
        queue = deque()
        queue.append(self.start)
        visited = set()
        parent_mappings = {}
        parent_mappings[self.start] = None
        found_path = False

        while queue:
            current_cell = queue.popleft()

            if current_cell in visited:
                continue
            visited.add(current_cell)

            if current_cell == self.goal:
                found_path = True
                break

            children = self.expand_cell(current_cell)

            if children:
                for child in children:
                    if child not in visited and self.maze[child[0]][child[1]] != "#":
                        parent_mappings[child] = current_cell
                        queue.append(child)

        if found_path:
            path = self.construct_path(parent_mappings)
            print(f"Full path: {path}")
            print(f"Nodes visited: {len(visited)}")

        else:
            print("Path not found...")

    def heuristic(self, current):
        return abs(current[0] - self.goal[0]) + abs(current[1] - self.goal[1])

    def g_cost(self, current):
        return abs(current[0] - self.start[0]) + abs(current[1] - self.start[1])

    def f_cost(self, current):
        return self.heuristic(current) + self.g_cost(current)

    def a_star(self):
        queue = []
        queue.append((self.heuristic(self.start), self.start))
        heapq.heapify(queue)
        visited = set()
        came_from = {}
        came_from[self.start] = None
        found_path = False
        cost = 0

        while queue:
            f_cost, current_cell = heapq.heappop(queue)

            cost = f_cost + self.g_cost(current_cell)

            if current_cell in visited:
                continue
            visited.add(current_cell)

            if current_cell == self.goal:
                found_path = True
                break

            children = self.expand_cell(current_cell)

            if children:
                for child in children:
                    if child not in visited and self.maze[child[0]][child[1]] != "#":
                        came_from[child] = current_cell
                        heapq.heappush(queue, (self.heuristic(child), child))

        if found_path:
            path = self.construct_path(came_from)
            print(f"Full path: {path}")
            print(f"Cost: {cost}")
            print(f"Nodes visited: {len(visited)}")

        else:
            print("Path not found...")


# =======================================================================================================
#                                             TICTACTOE
# =======================================================================================================
import random

board = 0
iterator = 0


def make_board(n):
    global board
    board = [["." for _ in range(n)] for _ in range(n)]
    return


current_player = "X"
output = False  # this will be used to check if the game has come to an end
best_move = 0  # thi variable will be temporarily tracking the best move
lock = False  # this lock exists so that the Agent priotizes winning over blocking X


# this will be switching the two players
def switch():
    global current_player
    if current_player == "X":
        current_player = "O"
    else:
        current_player = "X"


# self explanortory
def is_cell_valid(cell):
    cell_row, cell_col = cell[0], cell[1]
    rows, cols = len(board), len(board[0])

    if not (0 <= cell_row < rows):
        return False
    return 0 <= cell_col < cols


# checks for a winner as well as the best move that the agent can make horizontally
def checkHorizontal():
    global output, current_player, best_move, lock, iterator
    i = 0  # row start index
    for list in board:
        j = 0  # column start index
        if len(board) == 5:
            iterator = 2
        else:
            iterator = 5
        while j < iterator:
            # checks if we have a winner
            if list[j] == list[j + 1] == list[j + 2] == list[j + 3] and list[j] != ".":
                output = True
                switch()
                return best_move
            # checks if the current player is the agent and the decides what best move it can make
            elif current_player == "O":
                if (
                    list[j] == list[j + 1] == list[j + 2] == "O"
                    and is_cell_valid((i, j - 1))
                    and board[i][j - 1] == "."
                ):
                    # when it finds the move that can make it win, it locks the lock so that other check algorithms don't waste time running as well as so that they dont outer the best move
                    lock = True
                    output = True
                    return (i, j - 1)
                elif (
                    list[j] == list[j + 1] == list[j + 2] == "X"
                    and is_cell_valid((i, j - 1))
                    and board[i][j - 1] == "."
                ):
                    return (i, j - 1)
                elif (
                    list[j] == list[j + 1] == list[j + 2] == "O"
                    and is_cell_valid((i, j + 3))
                    and board[i][j + 3] == "."
                ):
                    lock = True
                    output = True
                    return (i, j + 3)
                elif (
                    list[j] == list[j + 1] == list[j + 2] == "X"
                    and is_cell_valid((i, j + 3))
                    and board[i][j + 3] == "."
                ):
                    return (i, j + 3)
                elif (
                    list[j] == list[j + 1] == list[j + 3] == "O"
                    and board[i][j + 2] == "."
                ):
                    lock = True
                    output = True
                    return (i, j + 2)
                elif (
                    list[j] == list[j + 1] == list[j + 3] == "X"
                    and board[i][j + 2] == "."
                ):
                    return (i, j + 2)
                elif (
                    list[j] == list[j + 2] == list[j + 3] == "O"
                    and board[i][j + 1] == "."
                ):
                    lock = True
                    output = True
                    return (i, j + 1)
                elif (
                    list[j] == list[j + 2] == list[j + 3] == "X"
                    and board[i][j + 1] == "."
                ):
                    return (i, j + 1)
                elif j == 4:
                    if (
                        list[j + 1] == list[j + 2] == list[j + 3] == "O"
                        and list[j] == "."
                    ):
                        lock = True
                        output = True
                        return (i, j)
                    elif (
                        list[j + 1] == list[j + 2] == list[j + 3] == "X"
                        and list[j] == "."
                    ):
                        return (i, j)

            j = j + 1
        i = i + 1
    return best_move


# checks for a winner as well as the best move that the agent can make horizontally
def checkVertical():
    global board, best_move, output, lock, iterator
    j = 0  # column start index
    if len(board) == 5:
        iterator = 2
    else:
        iterator = 5
    while j < len(board):  # Checks if we haven't reached the last column
        i = 0
        while i < iterator:
            # this line checks if we have a winner, useful to both the human and the agent
            if (
                board[i][j] == board[i + 1][j] == board[i + 2][j] == board[i + 3][j]
                and board[i][j] != "."
            ):
                output = True
                switch()
                return best_move
            # this line checks if the current player is the Agent, and then decides the best move it can make
            elif current_player == "O":
                # This checks if the best move has alread been found in the horizontal check
                if lock:
                    return best_move
                elif (
                    board[i][j] == board[i + 1][j] == board[i + 2][j] == "O"
                    and is_cell_valid((i - 1, j))
                    and board[i - 1][j] == "."
                ):
                    # when it finds the move that can make it win, it locks the lock so that other check algorithms don't waste time running as well as so that they dont outer the best move
                    lock = True
                    output = True
                    return (i - 1, j)
                elif (
                    board[i][j] == board[i + 1][j] == board[i + 2][j] == "X"
                    and is_cell_valid((i - 1, j))
                    and board[i - 1][j] == "."
                ):
                    return (i - 1, j)
                elif (
                    board[i][j] == board[i + 1][j] == board[i + 2][j] == "O"
                    and is_cell_valid((i + 3, j))
                    and board[i + 3][j] == "."
                ):
                    lock = True
                    output = True
                    return (i + 3, j)
                elif (
                    board[i][j] == board[i + 1][j] == board[i + 2][j] == "X"
                    and is_cell_valid((i + 3, j))
                    and board[i + 3][j] == "."
                ):
                    return (i + 3, j)
                elif (
                    board[i][j] == board[i + 1][j] == board[i + 3][j] == "O"
                    and board[i + 2][j] == "."
                ):
                    lock = True
                    output = True
                    return (i + 2, j)
                elif (
                    board[i][j] == board[i + 1][j] == board[i + 3][j] == "X"
                    and board[i + 2][j] == "."
                ):
                    return (i + 2, j)
                elif (
                    board[i][j] == board[i + 2][j] == board[i + 3][j] == "O"
                    and board[i + 1][j] == "."
                ):
                    lock = True
                    output = True
                    return (i + 1, j)
                elif (
                    board[i][j] == board[i + 2][j] == board[i + 3][j] == "X"
                    and board[i + 1][j] == "."
                ):
                    return (i + 1, j)
                elif i == 4:
                    if (
                        board[i + 1][j] == board[i + 2][j] == board[i + 3][j] == "O"
                        and board[i][j] == "."
                    ):
                        lock = True
                        output = True
                        return (i, j)
                    elif (
                        board[i + 1][j] == board[i + 2][j] == board[i + 3][j] == "X"
                        and board[i][j] == "."
                    ):
                        return (i, j)
            i = i + 1
        j = j + 1
    return best_move


# checks for a winner as well as the best move that the agent can make Diagonally
def checkDiagonalRight():
    global board, best_move, output, lock
    # Magic, can be explained better in person
    i = 4
    j = -1
    n = 0
    m = 0
    while n <= len(board):
        temp_i = i
        temp_j = j
        m = m + 1
        q = 1
        while q <= m:
            i = i - 1
            j = j + 1
            if (
                board[i][j]
                == board[i - 1][j + 1]
                == board[i - 2][j + 2]
                == board[i - 3][j + 3]
                and board[i][j] != "."
            ):
                output = True
                switch()
                return best_move
            # this line checks if the current player is the Agent, and then decides the best move it can make
            elif current_player == "O":
                # This checks if the best move has alread been found in the horizontal or vertical check
                if lock:
                    return best_move
                elif (
                    board[i][j] == board[i - 1][j + 1] == board[i - 2][j + 2] == "O"
                    and is_cell_valid((i + 1, j - 1))
                    and board[i + 1][j - 1] == "."
                ):
                    # when it finds the move that can make it win, it locks the lock so that other check algorithms don't waste time running as well as so that they dont outer the best move
                    lock = True
                    output = True
                    return (i + 1, j - 1)
                elif (
                    board[i][j] == board[i - 1][j + 1] == board[i - 2][j + 2] == "X"
                    and is_cell_valid((i + 1, j - 1))
                    and board[i + 1][j - 1] == "."
                ):
                    return (i + 1, j - 1)
                elif (
                    board[i][j] == board[i - 1][j + 1] == board[i - 2][j + 2] == "O"
                    and is_cell_valid((i - 3, j + 3))
                    and board[i - 3][j + 3] == "."
                ):
                    lock = True
                    output = True
                    return (i - 3, j + 3)
                elif (
                    board[i][j] == board[i - 1][j + 1] == board[i - 2][j + 2] == "X"
                    and is_cell_valid((i - 3, j + 3))
                    and board[i - 3][j + 3] == "."
                ):
                    return (i - 3, j + 3)
                elif (
                    board[i][j] == board[i - 2][j + 2] == board[i - 3][j + 3] == "O"
                    and board[i - 1][j + 1] == "."
                ):
                    lock = True
                    output = True
                    return (i - 1, j + 1)
                elif (
                    board[i][j] == board[i - 2][j + 2] == board[i - 3][j + 3] == "X"
                    and board[i - 1][j + 1] == "."
                ):
                    return (i - 1, j + 1)
                elif (
                    board[i][j] == board[i - 1][j + 1] == board[i - 3][j + 3] == "O"
                    and board[i - 2][j + 2] == "."
                ):
                    lock = True
                    output = True
                    return (i - 2, j + 2)
                elif (
                    board[i][j] == board[i - 1][j + 1] == board[i - 3][j + 3] == "X"
                    and board[i - 2][j + 2] == "."
                ):
                    return (i - 2, j + 2)
                elif m == q:
                    if (
                        board[i - 1][j + 1]
                        == board[i - 2][j + 2]
                        == board[i - 3][j + 3]
                        == "O"
                        and board[i][j] == "."
                    ):
                        lock = True
                        output = True
                        return (i, j)
                    elif (
                        board[i - 1][j + 1]
                        == board[i - 2][j + 2]
                        == board[i - 3][j + 3]
                        == "X"
                        and board[i][j] == "."
                    ):
                        return (i, j)
            q = q + 1
        i = temp_i + 1
        j = temp_j
        n = n + 1
        if n >= (len(board) - 3):
            j = (len(board) - 3) - m
            m = m - 2
            i = len(board)
    return best_move


# checks for a winner as well as the best move that the agent can make Diagonally
def checkDiagonalLeft():
    # Magic, can be explained better in person
    global output, best_move, lock, iterator, board
    j = 4
    i = len(board)
    n = 0
    m = 0
    while n <= len(board):
        temp_i = i
        temp_j = j
        m = m + 1
        q = 1
        while q <= m:
            j = j - 1
            i = i - 1
            if (
                board[i][j]
                == board[i - 1][j - 1]
                == board[i - 2][j - 2]
                == board[i - 3][j - 3]
                and board[i][j] != "."
            ):
                output = True
                switch()
                return
            # this line checks if the current player is the Agent, and then decides the best move it can make
            elif current_player == "O":
                if lock:
                    return best_move
                elif (
                    board[i][j] == board[i - 1][j - 1] == board[i - 2][j - 2] == "O"
                    and is_cell_valid((i + 1, j + 1))
                    and board[i + 1][j + 1] == "."
                ):
                    # when it finds the move that can make it win, it locks the lock so that other check algorithms don't waste time running as well as so that they dont outer the best move
                    lock = True
                    output = True
                    return (i + 1, j + 1)
                elif (
                    board[i][j] == board[i - 1][j - 1] == board[i - 2][j - 2] == "X"
                    and is_cell_valid((i + 1, j + 1))
                    and board[i + 1][j + 1] == "."
                ):
                    return (i + 1, j + 1)
                elif (
                    board[i][j] == board[i - 1][j - 1] == board[i - 2][j - 2] == "O"
                    and is_cell_valid((i - 3, j - 3))
                    and board[i - 3][j - 3] == "."
                ):
                    lock = True
                    output = True
                    return (i - 3, j - 3)
                elif (
                    board[i][j] == board[i - 1][j - 1] == board[i - 2][j - 2] == "X"
                    and is_cell_valid((i - 3, j - 3))
                    and board[i - 3][j - 3] == "."
                ):
                    return (i - 3, j - 3)
                elif (
                    board[i][j] == board[i - 2][j - 2] == board[i - 3][j - 3] == "O"
                    and board[i - 1][j - 1] == "."
                ):
                    lock = True
                    output = True
                    return (i - 1, j - 1)
                elif (
                    board[i][j] == board[i - 2][j - 2] == board[i - 3][j - 3] == "X"
                    and board[i - 1][j - 1] == "."
                ):
                    return (i - 1, j - 1)
                elif (
                    board[i][j] == board[i - 1][j - 1] == board[i - 3][j - 3] == "O"
                    and board[i - 2][j - 2] == "."
                ):
                    lock = True
                    output = True
                    return (i - 2, j - 2)
                elif (
                    board[i][j] == board[i - 1][j - 1] == board[i - 3][j - 3] == "X"
                    and board[i - 2][j - 2] == "."
                ):
                    return (i - 2, j - 2)
                elif m == q:
                    if (
                        board[i - 1][j - 1]
                        == board[i - 2][j - 2]
                        == board[i - 3][j - 3]
                        == "O"
                        and board[i][j] == "."
                    ):
                        lock = True
                        output = True
                        return (i, j)
                    elif (
                        board[i - 1][j - 1]
                        == board[i - 2][j - 2]
                        == board[i - 3][j - 3]
                        == "X"
                        and board[i][j] == "."
                    ):
                        return (i, j)
            q = q + 1
        j = temp_j + 1
        i = temp_i
        n = n + 1
        if n >= (len(board) - 3):
            i = m + 2
            m = m - 2
            j = 0
    return best_move


def human():
    global board, current_player
    if type(check()) != bool:
        row, column = tuple(input("Enter row and column number e.g. 11: "))
        while True:
            row, column = int(row), int(column)
            cell = (row, column)
            if is_cell_valid(cell):
                if board[row][column] == ".":
                    board[row][column] = "X"
                    switch()
                    return
                else:
                    row, column = tuple(
                        input("pleas enter valid row and colunm number!! ")
                    )
            else:
                row, column = tuple(
                    input("pleas enter an existing row and colunm number!! ")
                )
    return


def check():
    global best_move, lock
    if not output:
        best_move = checkHorizontal()
        best_move = checkVertical()
        best_move = checkDiagonalLeft()
        best_move = checkDiagonalRight()
        lock = False
        return best_move
    return output


def check_full():
    global output
    count = 0
    for _ in board:
        for i in _:
            if i != ".":
                count = count + 1

    if count == 64:
        output = True


def agent():
    global best_move
    move = check()
    if type(move) != bool:
        if move == 0:
            while True:
                if len(board) == 8:
                    x = random.randint(0, 7)
                    y = random.randint(0, 7)
                else:
                    x = random.randint(0, 4)
                    y = random.randint(0, 4)
                if board[x][y] == ".":
                    board[x][y] = "O"
                    return
        else:
            board[move[0]][move[1]] = "O"
            best_move = 0
            return
    return


# print the board
def print_board(board):
    n = len(board[0])
    header = "   " + " ".join(str(c) for c in range(n))
    print(header)
    for r, row in enumerate(board):
        print(f"{r:2} " + " ".join(row))
    print()


def play_tic_tac_toe():
    global output, current_player
    board_size = int(input("Enter board size between 5 or 8: "))
    if board_size == 5:
        make_board(5)
    elif board_size == 8:
        make_board(8)
    while not output:
        current_player = "X"
        print_board(board)
        human()
        agent()
        check_full()

    print("----------------------------------------------")
    print("We have a winner!!>>>>|", current_player, "|<<<<<<<")
    print("----------------------------------------------")
    print_board(board)


if __name__ == "__main__":
    while True:
        print("What game would you like to play:")
        print(
            "1. Maze Game using BFS\n2. Maze Game using A* \n3. Tic-tac-toe game\n4. Exit",
        )

        choice = None

        while True:
            user_input = input("Enter your choice 1, 2, 3 or 4: ")

            if user_input in ["1", "2", "3", "4"]:
                choice = int(user_input)
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.\n")

        match choice:
            case 1:
                print_board(maze)
                maze_solver = MazeSolver(maze, (0, 0), (2, 3))
                maze_solver.bfs()
            case 2:
                print_board(maze)
                maze_solver = MazeSolver(maze, (0, 0), (2, 3))
                maze_solver.a_star()
            case 3:
                play_tic_tac_toe()
            case 4:
                print("Program Exited...")
                sys.exit()
            case _:
                print("Please enter a valid choice.")
