import collections
import math
import sys

EMPTY_SPACE = 0


class Board(object):

    def __init__(self, x_dim, y_dim):
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.board = [EMPTY_SPACE for x in range(x_dim*y_dim)]

    # returns src's new position on the board
    def get_x_y(self, src):
        src_x = src % math.sqrt(len(self.board))
        src_y = (src - src_x) / math.sqrt(len(self.board))

        Point = collections.namedtuple('Point', ['x', 'y'])
        return Point(src_x, src_y)

    # Create a character on the game board, with starting x and y positions,
    # the board dimension, and an integer representation on the board
    def update(self, players):
        for player in players.values():
            if player.health <= 0:
                player.token = EMPTY_SPACE
                # print(player.name + " " + str(player.token))
            p = self.get_x_y(player.pos)
            place = int(self.x_dim * p.y + p.x)
            if len(self.board) <= 0:
                print("ERROR: Empty board.")
                return
            elif place > len(self.board):
                print("ERROR: Character off the board.")
                return
            else:
                self.board[place] = player.token

    def print_board(self):
        counter = 0
        for x in range(len(self.board)):
            if counter % self.x_dim == 0:
                sys.stdout.write('[' + str(self.board[counter]))
            elif counter % self.x_dim == self.x_dim - 1:
                print(' ' + str(self.board[counter]) + ']')
            else:
                sys.stdout.write(' ' + str(self.board[counter]))
            counter += 1

    # Determines if two positions are adjacent to one another to the north,
    # south, east, or west
    def is_adjacent(self, pos1, pos2):
        if pos2 == pos1 - 1 \
                or pos2 == pos1 + 1 \
                or pos2 == pos1 - self.x_dim \
                or pos2 == pos1 + self.x_dim:
            return True
        return False
