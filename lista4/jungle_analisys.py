# bot making a random analysis

from jungle_game import Jungle
from random import randrange as rand
# from tqdm import tqdm

def heuristic(game: Jungle):
    points = {'r':3, 'c':2, 'd':3, 'w':4, 'j':5, 't':6, 'l':7, 'e':8, 'R':3, 'C':2, 'D':3, 'W':4, 'J':5, 'T':6, 'L':7, 'E':8}
    value = 0
    for animal in game.top_animals:
        value += points[animal]
    for animal in game.bot_animals:
        value -= points[animal]
    return value

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
                    best_value = -10000
                    for nmove in nmoves:
                        tgame = ngame.copy()
                        tgame.move(*nmove)
                        value = heuristic(tgame)
                        if value > best_value:
                            best_move = nmove
                            best_value = value
                else:
                    best_value = 10000
                    for nmove in nmoves:
                        tgame = ngame.copy()
                        tgame.move(*nmove)
                        value = heuristic(tgame)
                        if value < best_value:
                            best_move = nmove
                            best_value = value
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

top_wins = 0
bot_wins = 0
for i in range(100):
    print(i)
    game = Jungle()
    # game.draw()
    winner = None
    while True:
        # print(game.get_moves())
        # move = heuristic_move(game, 200)
        move = analisys(game, 20000)
        game.move(*move)
        winner = game.winner(verbose=True)
        # game.draw()
        if winner is not None: break
        # print(game.get_moves())
        move = random_move(game)
        game.move(*move)
        winner = game.winner(verbose=True)
        # game.draw()
        if winner is not None: break
    if winner == 'top':
        top_wins += 1
    else:
        bot_wins += 1
print(top_wins, bot_wins)