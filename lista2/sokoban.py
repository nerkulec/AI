# Działa
# Zaliczone
from heapq import heappush, heappop

class Board: #2d array of W, G
    def __init__(self, board, boxes=None):
        self.width = len(board[0])
        self.height = len(board)
        self.board = board #stored row by row
        if boxes is None:
            self.boxes = [pos for pos in self if self[pos] == 'B']
        else:
            self.boxes = boxes
    def __getitem__(self, pos): #accessed (x,y)
        return self.board[pos[1]][pos[0]]
    def __setitem__(self, pos, val): #accessed (x,y)
        self.board[pos[1]][pos[0]] = val
    def __contains__(self, pos):
        return 0<=pos[0]<self.width and 0<=pos[1]<self.height and self[pos] != 'W'
    def __iter__(self):
        return (Pos(x, y) for x in range(self.width) for y in range(self.height))
    def copy(self):
        return Board([row.copy() for row in self.board], self.boxes.copy())
    def move_box(self, pos, pos2):
        self[pos] = '.'
        self[pos2] = 'B'
        for i in range(len(self.boxes)):
            if self.boxes[i] == pos:
                self.boxes[i] = pos2
    def __repr__(self):
        return self.board
    def draw(self):
        for y in range(self.height):
            for x in range(self.width):
                print(self.board[y][x], end='')
            print()
    def __hash__(self):
        return hash(tuple(map(tuple, self.board)))
    def __eq__(self, other):
        return hash(self) == hash(other)

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
    def __hash__(self):
        return hash((self.x, self.y))

def around(pos):
    return [pos+(1,0), pos+(0,1), pos+(-1,0), pos+(0,-1)]

def get_moves(board, pos):
    moves = []
    for direction, new_pos in enumerate(around(pos)):
        new_board = board
        #new_board = board.copy()
        if new_pos in board:
            if new_board[new_pos] == 'B':
                d = new_pos-pos
                if new_pos+d in new_board and new_board[new_pos+d] != 'B':
                    new_board = board.copy() #risky copy
                    new_board.move_box(new_pos, new_pos+d)
                else:
                    continue
            moves.append(((new_board, new_pos), 'RDLU'[direction]))
    return moves

def search(board, goals, sokoban):
    queue = []
    heappush(queue, (0, '', (board, sokoban)))
    seen = set()
    seen.add((board, sokoban))
    depth = 0
    while queue:
        priority, history, move = heappop(queue)
        if len(history) > depth:
            depth = len(history)
            print(depth)
        board, sokoban = move
        if all(board[goal] == 'B' for goal in goals):
            print(len(seen))
            return history
        moves = get_moves(*move)
        for new_move, direction in moves:
            if new_move not in seen:
                new_history = history + direction
                priority = len(new_history) + heuristic(new_move, goals)
                heappush(queue, (priority, new_history, new_move))
                seen.add(new_move)
    else:
        return "NOT FOUND"

def m_dist(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def heuristic(move, goals):
    board, sokoban = move
    boxes = board.boxes
    return sum(min(m_dist(goal, box) for goal in goals) for box in boxes)

with open("zad_input.txt", "r") as in_f:
    board = []
    goals = []
    for line in in_f:
        board.append(list(line[:-1]))
    board = Board(board)
    for y in range(board.height):
        for x in range(board.width):
            if board[x,y] == 'G':
                board[x,y] = '.'
                goals.append(Pos(x,y))
            elif board[x,y] == 'K':
                board[x,y] = '.'
                sokoban = Pos(x,y)
            elif board[x,y] == '+':
                board[x,y] = '.'
                goals.append(Pos(x,y))
                sokoban = Pos(x,y)
            elif board[x,y] == '*':
                board[x,y] = 'B'
                goals.append(Pos(x,y))
    with open("zad_output.txt", "w") as out_f:
        print(search(board, goals, sokoban), file=out_f)
            
# Zaliczone