# heuristic bot wins 10-0 in twice longer time than the analysis

from jungle_game import Jungle
from random import randrange as rand
from util_pypy import Pos, timeit
# from tqdm import tqdm

def m_dist(a, b):
    d = b-a
    return abs(d.x) + abs(d.y)

def heuristic(game: Jungle):
    points = {'r':4, 'c':1, 'd':2, 'w':3, 'j':5, 't':7, 'l':8, 'e':10, 
              'R':4, 'C':1, 'D':2, 'W':3, 'J':5, 'T':7, 'L':8, 'E':10}
    value = 0
    for animal in game.top_animals:
        value += points[animal]*4
    for animal in game.bot_animals:
        value -= points[animal]*4
    value -= min((m_dist(game.animals[a], Pos(3, 8)) for a in game.top_animals), default=0)
    value += min((m_dist(game.animals[a], Pos(3, 0)) for a in game.bot_animals), default=0)
    return value

@timeit
def analisys(game: Jungle, n):
    moves = game.get_moves()
    player = game.turn
    winrates = []
    for move in moves:
        ngame = game.copy()
        ngame.move(*move)
        top_wins = 0
        bot_wins = 0
        for _ in range(n//len(moves)):
            winner = ngame.winner()
            if winner is not None:
                if winner == 'top':
                    top_wins += 1
                else:
                    bot_wins += 1
                ngame = game.copy()
                ngame.move(*move)
            nmoves = ngame.get_moves()
            if len(nmoves) > 0:
                ngame.move(*nmoves[rand(len(nmoves))])
            else:
                break # no no
        if top_wins+bot_wins>0:
            if player == 'top':
                winrates.append(top_wins/(top_wins+bot_wins))
            else:
                winrates.append(bot_wins/(top_wins+bot_wins))
        else:
            winrates.append(0)
    return moves[max(range(len(moves)), key=lambda i: winrates[i])]

def random_move(game: Jungle):
    moves = game.get_moves()
    return moves[rand(len(moves))]

@timeit
def heuristic_move(game: Jungle, n):
    moves = game.get_moves()
    player = game.turn
    winrates = []
    for move in moves:
        ngame = game.copy()
        ngame.move(*move)
        top_wins = 0
        bot_wins = 0
        for _ in range(n//len(moves)):
            winner = ngame.winner()
            if winner is not None:
                ngame = game.copy()
                ngame.move(*move)
                if winner == 'top':
                    top_wins += 1
                else:
                    bot_wins += 1
            nmoves = ngame.get_moves()
            if ngame.turn == player:
                best_move = None
                if player == 'top':
                    best_value = -10000000
                    for nmove in nmoves:
                        tgame = ngame.copy()
                        tgame.move(*nmove)
                        value = heuristic(tgame)
                        if value > best_value:
                            best_move = nmove
                            best_value = value
                else:
                    best_value = 10000000
                    for nmove in nmoves:
                        tgame = ngame.copy()
                        tgame.move(*nmove)
                        value = heuristic(tgame)
                        if value < best_value:
                            best_move = nmove
                            best_value = value
                if best_move is None:
                    ngame.draw()
                    print(ngame.turn)
                    print(nmoves)
                    print(ngame.animals)
                ngame.move(*best_move)
            else:
                ngame.move(*nmoves[rand(len(nmoves))])
        if top_wins+bot_wins>0:
            if player == 'top':
                winrates.append(top_wins/(top_wins+bot_wins))
            else:
                winrates.append(bot_wins/(top_wins+bot_wins))
        else:
            winrates.append(0)
    return moves[max(range(len(moves)), key=lambda i: winrates[i])]

timeit('START')

h_wins = 0
a_wins = 0
players = [lambda g: heuristic_move(g, 4000), lambda g: analisys(g, 20000)]
# bot goes first
# top wins if draw => easier to win as top
# bot is lowercase, top is uppercase
for i in range(10):
    game = Jungle()
    # game.draw()
    winner = None
    h = ['bot', 'top'][i%2]
    print(i, f'heur on {h}')
    turn = 0
    while winner is None:
        move = players[(turn+i)%2](game) # exchange moves
        game.move(*move)
        turn += 1
        winner = game.winner(verbose=True)
        # game.draw()
    if winner == h:
        h_wins += 1
    else:
        a_wins += 1

timeit('SHOW')

print(h_wins, a_wins)