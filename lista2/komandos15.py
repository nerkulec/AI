# Działa

from heapq import heappush, heappop

class Board: #2d array of W, G
    def __init__(self, board, comandos=None, goals=None):
        self.width = len(board[0])
        self.height = len(board)
        self.board = board #stored row by row
        self.comandos = comandos
        self.goals = goals
    def __getitem__(self, pos): #accessed (x,y)
        return self.board[pos[1]][pos[0]]
    def __setitem__(self, pos, val): #accessed (x,y)
        self.board[pos[1]][pos[0]] = val
    def __contains__(self, pos):
        return 0<=pos[0]<self.width and 0<=pos[1]<self.height and self[pos] != '#'
    def __iter__(self):
        return (Pos(x, y) for x in range(self.width) for y in range(self.height))
    def copy(self):
        return Board(self.board, self.comandos, self.goals) # risky copy
    def __repr__(self):
        return self.board
    def draw(self):
        for y in range(self.height):
            for x in range(self.width):
                print('K' if Pos(x,y) in self.comandos else 'G' if Pos(x,y) in self.goals else self.board[y][x], end='')
            print()
    def move(self, direction):
        d = [(1,0), (0,1), (-1,0), (0,-1)][direction]
        self.comandos = frozenset(comando+d if comando+d in self else comando for comando in self.comandos)

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

def reduce_uncertainty(board, desired_uncertainty):
    counter = 0
    best_uncertainty = 1000000000000
    best_board = board
    history = ''
    while best_uncertainty>desired_uncertainty:
        counter += 1
        if counter > 60:
            break
        best_uncertainty = 1000000000000
        current_best_board = best_board
        for direction in range(4):
            new_board = best_board.copy()
            new_board.move(direction)
            uncertainty = len(new_board.comandos)
            if uncertainty<best_uncertainty:
                current_best_board = new_board
                best_uncertainty = uncertainty
                best_dir = direction
        best_board = current_best_board
        history += 'RDLU'[best_dir]
    return best_board, history

def spread(board):
    s = max(comando.x for comando in board.comandos) - min(comando.x for comando in board.comandos)
    s += max(comando.y for comando in board.comandos) - min(comando.y for comando in board.comandos)
    return s

def cluster(board, desired_spread):
    counter = 0
    best_spread = 1000000000000
    best_board = board
    history = ''
    while best_spread>desired_spread:
        counter += 1
        if counter > 40:
            break
        best_spread = 1000000000000
        current_best_board = best_board
        for direction in range(4):
            new_board = best_board.copy()
            new_board.move(direction)
            new_spread = spread(new_board)
            if new_spread<best_spread:
                current_best_board = new_board
                best_spread = new_spread
                best_dir = direction
        best_board = current_best_board
        history += 'RDLU'[best_dir]
    return best_board, history

def cluster2(board, desired_spread):
    queue = []
    heappush(queue, (0, '', board))
    seen = set()
    seen.add(board.comandos)
    depth = 0
    seen_size = 0
    while queue:
        priority, history, board = heappop(queue)
        if spread(board) <= desired_spread:
            return board, history
        for direction in range(4):
            new_board = board.copy()
            new_board.move(direction)
            if new_board.comandos not in seen:
                new_history = history+'RDLU'[direction]
                new_priority = len(new_history) + spread(new_board)
                heappush(queue, (new_priority, new_history, new_board))
                seen.add(new_board.comandos)
    
def elim_rows_cols(board):
    board = board.copy()
    for x in range(board.width-2):
        board.move(2)
    for y in range(board.height-2):
        board.move(3)
    return board, 'L'*(board.width-2)+'U'*(board.height-2)

def search(board):
    queue = []
    heappush(queue, (0, '', board))
    seen = set()
    seen.add(board.comandos)
    depth = 0
    seen_size = 0
    while queue:
        _, history, board = heappop(queue)
        if all(comando in board.goals for comando in board.comandos):
            print(f'seen: {len(seen)}')
            return history
        if len(history) > depth:
            depth = len(history)
            print(f'depth: {depth}')
        if len(seen) >= seen_size:
            print(f'seen: {seen_size}')
            seen_size += 10000
        for direction in range(4):
            new_board = board.copy()
            new_board.move(direction)
            if new_board.comandos not in seen:
                new_history = history+'RDLU'[direction]
                new_priority = len(new_history)
                heappush(queue, (new_priority, new_history, new_board))
                seen.add(new_board.comandos)
    else:
        return "NOT FOUND"

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
    board.comandos = frozenset(comandos)
    board.goals = goals
    board, history = elim_rows_cols(board)
    board.draw()
    with open("zad_output.txt", "w") as out_f:
        print(history+search(board), file=out_f)
            
