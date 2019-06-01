# make board a double sided class with constant time access both ways

# TODO: change to use mutable Pos

from util_pypy import Pos, deepcopy

class Jungle: # Capitals on top, capitals' cave is '%'
    def __init__(self, top_animals=None, bot_animals=None, animals=None, animal_board=None, turn=None, last_capture=None):
        self.width = 7
        self.height = 9
        self.dirs = [Pos(1,0), Pos(0,1), Pos(-1,0), Pos(0,-1)]
        if turn is None:
            self.turn = 'bot'
            self.other = 'top'
            self.last_capture = 0
        else:
            self.turn = turn
            self.other = 'bot' if turn == 'top' else 'top'
            self.last_capture = last_capture
        self.board = ['..#%#..', 
                      '...#...', 
                      '.......', 
                      '.~~.~~.', 
                      '.~~.~~.', 
                      '.~~.~~.', 
                      '.......', 
                      '...#...', 
                      '..#*#..']
        self.strengths = {'r':1, 'c':2, 'd':3, 'w':4, 'j':5, 't':6, 'l':7, 'e':8,
                          'R':1, 'C':2, 'D':3, 'W':4, 'J':5, 'T':6, 'L':7, 'E':8}
        if top_animals is None:
            self.top_animals = set('LDRJTCEW')
            self.bot_animals = set('ldrjtcew')
            self.animals = {'L':Pos(0,0), 'D':Pos(1,1), 'R':Pos(0,2), 'J':Pos(2,2),
                                'T':Pos(6,0), 'C':Pos(5,1), 'E':Pos(6,2), 'W':Pos(4,2),
                                'l':Pos(6,8), 'd':Pos(5,7), 'r':Pos(6,6), 'j':Pos(4,6),
                                't':Pos(0,8), 'c':Pos(1,7), 'e':Pos(0,6), 'w':Pos(2,6)}
            self.animal_board = [['/' for _ in range(self.width)] for _ in range(self.height)]
            for animal, pos in self.animals.items():
                self.animal_board[pos.y][pos.x] = animal
        else:
            self.top_animals = top_animals
            self.bot_animals = bot_animals
            self.animals = animals
            self.animal_board = animal_board

    def copy(self):
        return Jungle(self.top_animals.copy(), self.bot_animals.copy(), self.animals.copy(), deepcopy(self.animal_board), self.turn, self.last_capture)

    def can_move(self, predator, direction):
        pos = self.animals[predator]
        field = self.board[pos.y][pos.x]
        npos = pos+self.dirs[direction]
        if not (0<=npos.x<self.width and 0<=npos.y<self.height): # nie na planszy
            return False
        nfield = self.board[npos.y][npos.x]
        prey = self.animal_board[npos.y][npos.x]
        if predator in 'tTlL' and nfield == '~': # skok nad wodą
            while nfield != '.':
                if prey == 'rR':
                    return False
                npos += self.dirs[direction]
                nfield = self.board[npos.y][npos.x]
                prey = self.animal_board[npos.y][npos.x]
        prey = self.animal_board[npos.y][npos.x]
        if nfield == '.' and prey == '/': # normalny ruch
            return True
        if predator in 'rcdwjtle' and prey in 'rcdwjtle': # bicie swoich
            return False
        if predator in 'RCDWJTLE' and prey in 'RCDWJTLE': # bicie swoich
            return False
        if nfield == '~' and predator not in 'rRtTlL': # wchodzenie do wody
            return False
        if predator in 'rR' and field == '~' and nfield == '.' and prey != '/': # wychodzenie z wody
            return False
        if predator in 'rR' and nfield == '~': # rat to water
            return True
        if predator in 'rcdwjtle' and nfield == '*': # wchodzenie do własnej jamy
            return False
        if predator in 'RCDWJTLE' and nfield == '%': # wchodzenie do własnej jamy
            return False
        if field == '#' and prey != '/': # atakowanie z pułapki
            return False
        if nfield == '#': # atakowanie/wchodzenie do pułapki
            return True
        if predator in 'rcdwjtle' and nfield == '%': # winning
            return True
        if predator in 'RCDWJTLE' and nfield == '*': # winning
            return True
        if predator in 'rR' and prey in 'eE': # szczur vs słoń
            return True
        if predator in 'eE' and prey in 'rR': # słoń vs szczur
            return False
        if self.strengths[predator] >= self.strengths[prey]: # atak
            return True
        else:
            return False

    def winner(self, verbose=False):
        if self.animal_board[0][3] != '/':
            if verbose: print('bot won by entering cave')
            return 'bot'
        if self.animal_board[8][3] != '/':
            if verbose: print('top won by entering cave')
            return 'top'
        if len(self.top_animals) == 0:
            if verbose: print('bot won by eliminating top')
            return 'bot'
        if len(self.bot_animals) == 0:
            if verbose: print('top won by eliminating bot')
            return 'top'
        if self.last_capture >= 30:
            top = tuple(sorted(map(lambda x: self.strengths[x], self.top_animals)))
            bot = tuple(sorted(map(lambda x: self.strengths[x], self.bot_animals)))
            if bot > top:
                if verbose: print('bot won by stalling with better animals')
                return 'bot'
            elif top > bot:
                if verbose: print('top won by stalling with better animals')
                return 'top'
            else:
                if verbose: print('top won by stalling with same animals')
                return 'top'
        return None
            
    def get_moves(self):
        moves = []
        for animal in (self.top_animals if self.turn == 'top' else self.bot_animals):
            for direction in range(4):
                if self.can_move(animal, direction):
                    moves.append((animal, direction))
        return moves

    def move(self, animal, direction): # assume legal
        pos = self.animals[animal]
        d = self.dirs[direction]
        npos = pos + d
        nfield = self.board[npos.y][npos.x]
        if animal in 'tTlL' and nfield == '~':
            while nfield != '.':
                npos += d
                nfield = self.board[npos.y][npos.x]
        prey = self.animal_board[npos.y][npos.x]
        if prey != '/':
            if prey in self.top_animals:
                self.top_animals.remove(prey)
            else:
                self.bot_animals.remove(prey)
            del self.animals[prey]
            self.last_capture = 0
        else:
            self.last_capture += 1
        self.animal_board[pos.y][pos.x] = '/'
        self.animal_board[npos.y][npos.x] = animal
        self.animals[animal] = npos
        self.turn, self.other = self.other, self.turn

    def draw(self):
        for y in range(self.height):
            print(''.join(self.board[y])+' '+''.join(['.' if self.animal_board[y][x] == '/' else self.animal_board[y][x] for x in range(self.width)]))
        print()

if __name__ == '__main__':
    test = Jungle()
    while True:
        test.draw()
        print(test.get_moves())
        i = input()
        test.move(i[0], int(i[1]))
        win = test.winner()
        if(win is not None):
            print(f'Winner is {win}')
            break
