# wins 100% against random bot with 10 iterations
# 600 iterations is a 0.5s move
# 50 - 3 wins 70%


import random
from reversi import Reversi, random_move, alphabeta_move
from math import log, sqrt
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable):
        l = len(iterable)
        for i, e in enumerate(iterable):
            print('{}/{}'.format(i, l))
            yield e
try:
    from util import Pos, cacheit, timeit
except:
    from util_pypy import Pos, cacheit, timeit

c = sqrt(2)

class Node:
    def __init__(self, game: Reversi, parent):
        self.game = game
        self.player = game.other # player that made the last move ie the move that led to this state
        self.wins = 0
        self.games = 0
        self.parent = parent
        self.expanded = False
        self.children = {}

    @timeit
    def expand(self):
        assert not self.expanded
        moves = self.game.get_moves()
        if moves:
            for move in moves:
                game_copy = self.game.copy()
                game_copy.move(move)
                self.children[move] = Node(game_copy, self)
        else:
            game_copy = self.game.copy()
            game_copy.move(None)
            self.children[None] = Node(game_copy, self)
        self.expanded = True

    def update(self, winner):
        if winner == self.player:
            self.wins += 1
        self.games += 1
        if self.parent is not None:
            self.parent.update(winner)

    def get_winrate(self):
        return self.wins/self.games

    def get_uct(self, root):
        return self.get_winrate() + c*sqrt(log(root.games)/self.games)

    @timeit
    def simulate(self):
        simulated_game = self.game.copy()
        while not simulated_game.terminal():
            simulated_game.move(random_move(simulated_game))
        return simulated_game.winner()


class MCTS:
    def __init__(self, game: Reversi):
        self.root = Node(game, None)

    @timeit
    def select(self):
        selected = self.root
        while selected.expanded:
            if all(n.expanded for n in selected.children.values()):
                selected = max(selected.children.values(), key=lambda n: n.get_uct(self.root))
            else:
                selected = random.choice([n for n in selected.children.values() if not n.expanded])
        return selected

    def run(self, iterations):
        for _ in range(iterations):
            selected = self.select()
            selected.expand()
            winner = selected.simulate()
            selected.update(winner)

    def get_move(self):
        return max(self.root.children, key=lambda k: self.root.children[k].games)

    def make_move(self, move):
        self.root = self.root.children[move]
        

def search(node, game):
    same = 0
    while node.game.history[same] == game.history[same]:
        same += 1

def play_against_random(num_games, iterations):
    mcts_wins_as_first = 0
    mcts_wins_as_second = 0
    draws = 0
    for _ in tqdm(range(num_games//2)):
        game = Reversi()
        mcts = MCTS(game)
        for step in range(70):
            if step%2==0:
                mcts.run(iterations)
                move = mcts.get_move()
            else:
                move = random_move(game)
            game.move(move)
            mcts.make_move(move)
            if game.terminal():
                winner = game.winner()
                if winner == 1:
                    mcts_wins_as_first += 1
                elif winner == 0.5:
                    draws += 1
                break
    for _ in tqdm(range(num_games//2)):
        game = Reversi()
        mcts = MCTS(game)
        mcts.run(1)
        for step in range(70):
            if step%2==0:
                move = random_move(game)
            else:
                mcts.run(iterations)
                move = mcts.get_move()
            game.move(move)
            mcts.make_move(move)
            if game.terminal():
                winner = game.winner()
                if winner == 0:
                    mcts_wins_as_second += 1
                elif winner == 0.5:
                    draws += 1
                break
    print('winrate: {}+{}/{}, draws: {}'.format(mcts_wins_as_first, mcts_wins_as_second, num_games, draws))

def play_against_alphabeta(num_games, iterations, depth):
    mcts_wins_as_first = 0
    mcts_wins_as_second = 0
    draws = 0
    for _ in tqdm(range(num_games//2)):
        game = Reversi()
        mcts = MCTS(game)
        # mcts.run(20)
        for step in range(70):
            if step%2==0:
                mcts.run(iterations)
                move = mcts.get_move()
            else:
                move = alphabeta_move(game, depth)
            # mcts.make_move(move)
            game.move(move)
            mcts = MCTS(game)
            if game.terminal():
                winner = game.winner()
                if winner == 1:
                    mcts_wins_as_first += 1
                elif winner == 0.5:
                    draws += 1
                break
    for _ in tqdm(range(num_games//2)):
        game = Reversi()
        mcts = MCTS(game)
        # mcts.run(20)
        for step in range(70):
            if step%2==0:
                move = alphabeta_move(game, depth)
            else:
                mcts.run(iterations)
                move = mcts.get_move()
            # mcts.make_move(move)
            game.move(move)
            mcts = MCTS(game)
            if game.terminal():
                winner = game.winner()
                if winner == 0:
                    mcts_wins_as_second += 1
                elif winner == 0.5:
                    draws += 1
                break
    print('winrate: {}+{}/{}, draws: {}'.format(mcts_wins_as_first, mcts_wins_as_second, num_games, draws))


if __name__ == '__main__':
    timeit('START')
    play_against_random(40, 200)
    # play_against_alphabeta(20, 400, 3)
    timeit('SHOW')
