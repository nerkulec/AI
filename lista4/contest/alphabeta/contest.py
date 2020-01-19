from reversi import Reversi, alphabeta_move

if __name__ == '__main__':
    end = False
    game = Reversi()
    print('RDY')
    while not end:
        command = input()
        if command == 'UGO':
            input()
            input()
        elif command == 'HEDID':
            input()
            input()
            his_move = int(input()), int(input())
            if his_move == -1, -1:
                his_move = None
            game.move(Pos(his_move))
        elif command == 'BYE':
            end = True
            break
        elif command == 'ONEMORE':
            game = Reversi()
            print('RDY')
            break
        my_move = alphabeta_move(game, depth=6)
        if my_move == None:
            my_move = Pos(-1, -1)
        print('IDO {} {}'.format(my_move.x, my_move.y))
    
