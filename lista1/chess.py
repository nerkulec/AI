# B - Black King
# W - White King
# R - White Rook

# turn 0 - White to move
# turn 1 - Black to move

from collections import deque

def pos(a):
    return ({'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}[a[0]], int(a[1])-1)

def draw(w, r, b, turn):
    for y in range(7, -1, -1):
        for x in range(8):
            print('W ' if (x, y) == w else 'R ' if (x, y) == r else 'B ' if (x, y) == b else '. ', end="")
        print()
    print()

def on_board(pos):
    return 0<=pos[0]<8 and 0<=pos[1]<8

def around(pos):
    return [(pos[0]+1,pos[1]), (pos[0]+1,pos[1]+1), (pos[0],pos[1]+1), (pos[0]-1,pos[1]+1), (pos[0]-1,pos[1]), (pos[0]-1,pos[1]-1), (pos[0],pos[1]-1), (pos[0]+1,pos[1]-1)]

def mat(w, r, b, turn):
    if turn == 1 and (b[0] == r[0] or b[1] == r[1]):
        moves = get_moves(w, r, b, turn)
        return len(moves) == 0
    return False

def between(a, b, c, cord=None):
    if cord is None:
        return between(a, b, c, 0) and between(a, b, c, 1)
    return a[cord]==b[cord]==c[cord] and (a[cord^1] < b[cord^1] < c[cord^1] or a[cord^1] > b[cord^1] > c[cord^1])

def ch_dist(pos1, pos2):
    return max(abs(pos1[0]-pos2[0]), abs(pos1[1]-pos2[1]))

def get_moves(w, r, b, turn):
    moves = []
    if turn == 1:
        for new_b in around(b):
            if on_board(new_b) and ch_dist(new_b, w)>1: # na planszy i nie wchodzi na króla
                if (new_b[0] == r[0] and not between(new_b, w, r, 1)): # wchodzi pod wieżę (pion)
                    continue
                if (new_b[1] == r[1] and not between(new_b, w, r, 0)): # wchodzi pod wieżę (poziom)
                    continue
                moves.append((w, r, new_b, turn^1))
    if turn == 0:
        for new_w in around(w):
            if on_board(new_w) and ch_dist(new_w, b)>1 and new_w != r: # na planszy i nie wchodzi na króla i wieżę
                moves.append((new_w, r, b, turn^1))
        for new_r in [(r[0], i) for i in range(8)] + [(i, r[1]) for i in range(8)]: # ruchy wieży
            if between(new_r, w, r): # przekracza króla w
                continue
            if between(new_r, b, r): # przekracza króla b
                continue
            if new_r in around(b):
                continue
            moves.append((w, new_r, b, turn^1))
    return moves

def BFS(w, r, b, turn):
    if type(w) is str:
        w, r, b = pos(w), pos(r), pos(b)
    if type(turn) is str:
        turn = 0 if turn == "white" else 1
    queue = deque()
    queue.append([(w, r, b, turn)])
    seen = set()
    depth = 0
    seen.add((w, r, b, turn))
    while queue:
        path = queue.popleft()
        if len(path)-1 > depth:
            depth = len(path)-1
            print(depth)
        last_move = path[-1]
        if mat(*last_move):
            return path
        for move in get_moves(*last_move):
            if move not in seen:
                queue.append(path+[move])
                seen.add(move)
                
a = BFS("a1", "a6", "f7", 1)
[draw(*line) for line in a] # white h6 a4 d4
print(len(a)-1) # white h6 a4 d4

# with open("zad1_input.txt", "r") as in_f:
#     with open("zad1_output.txt", "w") as out_f:
#         for line in in_f:
#             turn, w, r, b = line.split()
#             moves = BFS(w, r, b, turn)
#             #[draw(move) for move in moves]
#             out_f.write(str(len(moves)-1)+'\n')

