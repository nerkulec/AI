import random

class Node:
    def __init__(self, move=None, parent=None, game=None):
        self.move = move
        self.wins = 0 # remembering wins for the player to move
        self.visits = 0
        self.children = []
        self.parent = parent
        self.untried_moves = game.get_moves()
        self.player_moved = 1-game.turn

    def select_child(self):
        return max(self.childNodes, key=lambda c: c.wins/c.visits + sqrt(2*log(self.visits)/c.visits))

    def add_child(self, move, game):
        new_node = Node(move=move, parent=self, game=game)
        self.children.append(new_node)
        self.untried_moves.remove(move)
        return new_node

    def update(self, result):
        self.visits += 1
        self.wins += result

    def UCT(game, max_iters):
        root = Node(game=game)
        for i in range(max_iters):
            node = root
            state = game.copy()

            # Select
            while node.untried_moves == [] and node.children != []: # node is fully expanded and non-terminal
                node = node.select_child()
                game.move(node.move)

            # Expand
            if node.untried_moves != []: # if we can expand (i.e. state/node is non-terminal)
                move = random.choice(node.untried_moves) 
                game.move(move)
                node = node.add_child(move, game) # add child and descend tree

            # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
            moves = game.get_moves()
            while moves != []: # while state is non-terminal
                game.move(random.choice(moves))
                moves = game.get_moves()

            # Backpropagate
            while node != None: # backpropagate from the expanded node and work back to the root node
                node.update(game.GetResult(node.playerJustMoved)) # state is terminal. Update node with result from POV of node.playerJustMoved
                node = node.parentNode
