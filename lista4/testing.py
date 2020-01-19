from reversi import Reversi, alphabeta, alphabeta_move
from util import Pos

game = Reversi()
history = Pos(2, 4), Pos(2, 5), Pos(2, 6), Pos(5, 4), Pos(3, 5), Pos(1, 7), Pos(5, 5), Pos(1, 4), Pos(3, 6), Pos(2, 3), Pos(1, 2), Pos(3, 2), Pos(6, 4), Pos(0, 1), Pos(1, 3), Pos(6, 6), Pos(5, 6), Pos(7, 4), Pos(0, 4), Pos(4, 6), Pos(4, 1), Pos(2, 1), Pos(2, 7), Pos(1, 6), Pos(1, 1), Pos(0, 3), Pos(4, 2), Pos(4, 5), Pos(5, 7), Pos(5, 2), Pos(7, 3), Pos(3, 0), Pos(0, 6), Pos(1, 5), Pos(5, 3), Pos(6, 3), Pos(7, 7), Pos(7, 6), Pos(0, 5), Pos(4, 7), Pos(6, 1), Pos(6, 2), Pos(0, 7), Pos(6, 0), Pos(5, 1), Pos(1, 0), Pos(4, 0), Pos(6, 7), Pos(3, 7), Pos(5, 0), Pos(7, 0), Pos(7, 2), Pos(6, 5)
game.simulate(history)
print('a')


