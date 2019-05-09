from heapq import heappush, heappop
import numpy as np

# Poprawiona poprawność, heura za słaba

class Board: #2d array of W, G
    def __init__(self, board, comandos=None, goals=None, dist=None):
        self.width = len(board[0])
        self.height = len(board)
        self.board = board #stored row by row
        self.comandos = comandos
        self.goals = goals
        self.dist = dist
    def __getitem__(self, pos): #accessed (x,y)
        return self.board[pos[1]][pos[0]]
    def __setitem__(self, pos, val): #accessed (x,y)
        self.board[pos[1]][pos[0]] = val
    def __contains__(self, pos):
        return self[pos] != '#'
    def __iter__(self):
        return (Pos(x, y) for x in range(self.width) for y in range(self.height))
    def set_dist(self):
        queue = []
        seen = set()
        self.dist = [[-1 for _ in range(self.width)] for _ in range(self.height)]
        [(heappush(queue, (0, goal)), seen.add(goal)) for goal in self.goals]
        while queue:
            dist, pos = heappop(queue)
            self.dist[pos[1]][pos[0]] = dist
            for new_pos in around(pos):
                if new_pos in board and new_pos not in seen:
                    heappush(queue, (dist+1, new_pos))
                    seen.add(new_pos)
    def get_dist(self, pos):
        return self.dist[pos[1]][pos[0]]
    def copy(self):
        return Board(self.board, self.comandos, self.goals, self.dist)
    def __repr__(self):
        return self.board
    def draw(self):
        for y in range(self.height):
            for x in range(self.width):
                print('K' if Pos(x,y) in self.comandos else 'G' if Pos(x,y) in self.goals else self.board[y][x], end='')
            print()
    def draw_dists(self):
        for y in range(self.height):
            for x in range(self.width):
                print(f'{self.dist[y][x]:3}', end='')
            print()
    def move(self, direction):
        d = [(1,0), (0,1), (-1,0), (0,-1)][direction]
        self.comandos = tuple(sorted((comando+d if comando+d in self else comando for comando in self.comandos)))

class Pos:
    def __init__(self, a, b=None):
        self.x, self.y = a if b is None else (a, b)
    def __add__(self, other):
        return Pos((self.x+other[0], self.y+other[1]))
    def __sub__(self, other):
        return Pos((self.x-other[0], self.y-other[1]))
    def __neg__(self):
        return Pos((-self.x, -self.y))
    def __eq__(self, other):
        return self.x == other[0] and self.y == other[1]
    def __getitem__(self, num):
        return [self.x, self.y][num]
    def copy(self):
        return Pos(self.x, self.y)
    def __repr__(self):
        return f"({self.x}, {self.y})"
    def __lt__(self, other):
        return self.x<other[0] or (self.x==other[0] and self.y < other[1])
    def __hash__(self):
        return hash((self.x, self.y))

def around(pos):
    return [pos+(1,0), pos+(0,1), pos+(-1,0), pos+(0,-1)]

def m_dist(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def search(board, alpha=1):
    queue = []
    heappush(queue, (0, '', board))
    seen = set()
    seen_lengths = dict()
    seen.add(board.comandos)

    depth = 0
    seen_size = 0
    max_priority = -1
    while queue:
        priority, history, board = heappop(queue)
        if all(comando in board.goals for comando in board.comandos):
            print(f'seen: {len(seen)}')
            return history
        if priority > max_priority:
            max_priority = priority
            # print(f'resolving priority: {priority}')
        # if history == 'DDDL':
        #     print('b')
        # if history == "DDDLDDL"[:len(history)]:
        #     print(f'resolving bad:      {priority}')
        # if history == "DRDDLL"[:len(history)]:
        #     print(f'resolving good:     {priority}')
        # if len(history) > depth:
        #     depth = len(history)
        #     print(f'depth: {depth}')
        # if len(seen) >= seen_size:
        #     print(f'seen: {seen_size}')
        #     seen_size += 1000
        for direction in range(4):
            new_board = board.copy()
            new_board.move(direction)
            # if new_board.comandos == frozenset({(2, 4), (1, 4)}):
            #     print('a')
            if new_board.comandos in seen:
                continue
            new_history = history+'RDLU'[direction]
            new_priority = len(new_history) + alpha*heuristic(new_board)
            # if new_history == "DDDLDDL"[:len(new_history)]:
            #     print(f'adding bad:         {new_priority}')
            # if new_history == "DRDDLL"[:len(new_history)]:
            #     print(f'adding good:        {new_priority}')
            heappush(queue, (new_priority, new_history, new_board))
            seen.add(new_board.comandos)
    else:
        return "NOT FOUND"

def heuristic(board): #choose a comando that his distance to the nearest goal is the highest
    return max(board.get_dist(c) for c in board.comandos)

with open("zad_input.txt", "r") as in_f:
    board = []
    for line in in_f:
        board.append(list(line[:-1]))
    board = Board(board)
    goals = []
    comandos = []
    for y in range(board.height):
        for x in range(board.width):
            if board[x,y] == 'S':
                board[x,y] = ' '
                comandos.append(Pos(x,y))
            elif board[x,y] == 'B':
                board[x,y] = ' '
                comandos.append(Pos(x,y))
                goals.append(Pos(x,y))
            elif board[x,y] == 'G':
                board[x,y] = ' '
                goals.append(Pos(x,y))
    board.comandos = tuple(sorted(comandos))
    board.goals = goals
    board.set_dist()
    with open("zad_output.txt", "w") as out_f:
        print(search(board), file=out_f)
        # print(search(board, 1))
        # print(search(board, 0))
            
