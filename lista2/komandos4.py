from heapq import heappush, heappop

# Setne podejście
# Uproszczony, przechodzi wszystkie testy z alpha = 0.99

def get_dists(board, goals):
    queue = []
    seen = set()
    dists = [[-1 for _ in range(len(board[0]))] for _ in range(len(board))]
    for goal in goals:
        heappush(queue, (0, goal))
        seen.add(goal)
    while queue:
        dist, pos = heappop(queue)
        dists[pos[1]][pos[0]] = dist
        for direction in [(1,0), (0,1), (-1,0), (0,-1)]:
            new_pos = (pos[0] + direction[0], pos[1] + direction[1])
            if board[new_pos[1]][new_pos[0]] != '#' and new_pos not in seen:
                heappush(queue, (dist+1, new_pos))
                seen.add(new_pos)
    return dists

def get_heuristic(board, goals):
    dists = get_dists(board, goals)
    def heuristic(board):
        comandos = [(x, y) for x in range(len(board[0])) for y in range(len(board)) if board[y][x] == 'S']
        return max(dists[c[1]][c[0]] for c in comandos)
    # draw_dists(dists)
    return heuristic

def move(board, direction):
    dx, dy = [(1,0), (0,1), (-1,0), (0,-1)][direction]
    comandos = [(x, y) for x in range(len(board[0])) for y in range(len(board)) if board[y][x] == 'S']
    comandos = [(com[0]+dx, com[1]+dy) if board[com[1]+dy][com[0]+dx] != '#' else com for com in comandos]
    new_board = [[board[y][x] if board[y][x] == '#' else 'S' if (x,y) in comandos else ' ' for x in range(len(board[0]))] for y in range(len(board))]
    return tuple(tuple(row) for row in new_board)

def draw_dists(dists):
    for y in range(len(dists)):
        for x in range(len(dists[0])):
            print(f'{dists[y][x]:3}', end='')
        print()

def search(board, goals, alpha=1):
    queue = [] # (priority, history, board)
    seen = set() # board
    heappush(queue, (0, '', board))
    heuristic = get_heuristic(board, goals)
    while queue:
        _, history, board = heappop(queue)
        comandos = [(x, y) for x in range(len(board[0])) for y in range(len(board)) if board[y][x] == 'S']
        if all(com in goals for com in comandos):
            return history
        for direction in range(4):
            new_board = move(board, direction)
            if new_board in seen:
                continue
            new_history = history + 'RDLU'[direction]
            new_priority = len(new_history) + alpha*heuristic(new_board)
            heappush(queue, (new_priority, new_history, new_board))
            seen.add(new_board)

with open("zad_input.txt", "r") as in_f:
    board = []
    for line in in_f:
        board.append(list(line[:-1]))
    goals = []
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == 'B':
                board[y][x] = 'S'
                goals.append((x,y))
            elif board[y][x] == 'G':
                board[y][x] = ' '
                goals.append((x,y))
    board = tuple(tuple(row) for row in board)
    with open("zad_output.txt", "w") as out_f:
        print(search(board, goals, 0.99), file=out_f)
        # print(search(board, goals, 1))
        # print(search(board, goals, 0))
            
