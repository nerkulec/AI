from heapq import heappush, heappop

# Osiemnaste podejście

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
    def heuristic(comandos):
        return max(dists[c[1]][c[0]] for c in comandos)
    # draw_dists(dists)
    return heuristic

state_repr = lambda comandos: tuple(sorted(set(comandos)))

def move(board, comandos, direction):
    dx, dy = [(1,0), (0,1), (-1,0), (0,-1)][direction]
    return state_repr((com[0]+dx, com[1]+dy) if board[com[1]+dy][com[0]+dx] != '#' else com for com in comandos)

def draw_dists(dists):
    for y in range(len(dists)):
        for x in range(len(dists[0])):
            print(f'{dists[y][x]:3}', end='')
        print()

def search(board, comandos, goals, alpha=1):
    queue = [] # (priority, history, board)
    seen = set() # comandos
    heappush(queue, (0, '', comandos))
    heuristic = get_heuristic(board, goals)
    while queue:
        _, history, comandos = heappop(queue)
        if all(com in goals for com in comandos):
            return history
        for direction in range(4):
            new_comandos = move(board, comandos, direction)
            if new_comandos in seen:
                continue
            new_history = history + 'RDLU'[direction]
            new_priority = len(new_history) + alpha*heuristic(new_comandos)
            heappush(queue, (new_priority, new_history, new_comandos))
            seen.add(new_comandos)

with open("zad_input.txt", "r") as in_f:
    board = []
    for line in in_f:
        board.append(list(line[:-1]))
    goals = []
    comandos = []
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == 'S':
                board[y][x] = ' '
                comandos.append((x,y))
            elif board[y][x] == 'B':
                board[y][x] = ' '
                comandos.append((x,y))
                goals.append((x,y))
            elif board[y][x] == 'G':
                board[y][x] = ' '
                goals.append((x,y))
    comandos = state_repr(comandos)
    with open("zad_output.txt", "w") as out_f:
        print(search(board, comandos, goals, 0.99), file=out_f)
        # print(search(board, comandos, goals, 1))
        # print(search(board, comandos, goals, 0))
            
