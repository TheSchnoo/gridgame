import sys

import math

import collections

from character import Character

EMPTY_SPACE = 0
SPEED_1 = 1
SPEED_2 = 1


def create_empty_board(dim):
    return [EMPTY_SPACE for x in range(dim*dim)]


def print_board(board, dim):
    counter = 0
    for x in range(len(board)):
        # print(board[counter])
        if counter % dim == 0:
            sys.stdout.write('[' + str(board[counter]))
        elif counter % dim == dim - 1:
            print(' ' + str(board[counter]) + ']')
        else:
            sys.stdout.write(' ' + str(board[counter]))
        counter += 1


# Create a character on the game board, with starting x and y positions,
# the board dimension, and an integer representation on the board
def update_board(board, dim, players):
    for key in players:
        player = players.get(key)
        p = get_x_y(player.pos, board)
        place = int(dim * p.y + p.x)
        if len(board) <= 0:
            print("ERROR: Empty board.")
            return
        elif place > len(board):
            print("ERROR: Character off the board.")
            return
        else:
            board[place] = player.token


def is_adjacent(player1_pos, player2_pos, dim):
    if player2_pos == player1_pos - 1 \
            or player2_pos == player1_pos + 1 \
            or player2_pos == player1_pos - dim \
            or player2_pos == player1_pos + dim:
            return True
    return False


def move_east(board, src, spaces):
    start = src.pos
    if board[start + spaces] == EMPTY_SPACE:
        board[start] = EMPTY_SPACE
        board[start + spaces] = src.token
        src.pos = start + spaces
        return start + spaces
    return start


def move_west(board, src, spaces):
    start = src.pos
    if board[start + spaces] == EMPTY_SPACE:
        board[start] = EMPTY_SPACE
        board[start - spaces] = src.token
        src.pos = start - spaces
        return start - spaces
    return start


def move_north(board, src, spaces):
    start = src.pos
    if board[start - (spaces*dim)] == EMPTY_SPACE:
        board[start] = EMPTY_SPACE
        board[start - (spaces*dim)] = src.token
        src.pos = start - (spaces*dim)
        return start - (spaces*dim)
    return start


def move_south(board, src, spaces):
    start = src.pos
    if board[start + (spaces * dim)] == EMPTY_SPACE:
        board[start] = EMPTY_SPACE
        board[start + (spaces*dim)] = src.token
        src.pos = start + (spaces * dim)
        return start + (spaces*dim)
    return start


# returns src's new position on the board
def get_x_y(src, board):
    src_x = src % math.sqrt(len(board))
    src_y = (src - src_x) / math.sqrt(len(board))

    Point = collections.namedtuple('Point', ['x', 'y'])
    return Point(src_x, src_y)


def move_x(board, src, horiz_dist):
    if horiz_dist >= 0:
        return move_east(board, src, SPEED_1)
    else:
        return move_west(board, src, SPEED_1)


def move_y(board, src, vert_dist):
    if vert_dist >= 0:
        return move_south(board, src, SPEED_1)
    else:
        return move_north(board, src, SPEED_1)


def follow(src, target, board):
    src_p = get_x_y(src.pos, board)
    target_p = get_x_y(target.pos, board)

    if abs(target_p.x - src_p.x) > abs(target_p.y - src_p.y):
        return move_x(board, src, target_p.x - src_p.x)
    else:
        return move_y(board, src, target_p.y - src_p.y)


def game_continues(players):
    count = 0
    for player in players.values():
        if player.health <= 0:
            count += 1
    if len(players) - count <= 1:
        return False
    return True


def find_target(src_player, players):
    for key in players:
        if not players.get(key) == src_player:
            if is_adjacent(src_player.pos, players.get(key).pos, math.sqrt(len(board))):
                return players.get(key)
    return


def process_player_turn(board, player_name, players):
    player = players.get(player_name)
    while player.endurance > 0:
        move = input('Your move: ')
        if move == 'u':
            move_north(board, player, player.speed)
        elif move == 'd':
            move_south(board, player, player.speed)
        elif move == 'r':
            move_east(board, player, player.speed)
        elif move == 'l':
            move_west(board, player, player.speed)
        elif move == 'a':
            player_target = find_target(player, players)
            if player_target:
                if is_adjacent(player1.pos, player_target.pos, math.sqrt(len(board))):
                    player_target.take_damage(player.attack)
                    print(player_name + " attacks! --> target health: " + str(player_target.health))
        player.endurance -= 1
        print_board(board, math.sqrt(len(board)))


def deal_damage(player, player_target):
    attack = player.calculate_damage()
    if attack == 0:
        print("ATTACK IS 0!")
    print(player_target.take_damage(attack))


def process_player_autoturn(board, player_name, players, strategy):

    player = players.get(player_name)
    player_target = ""
    for key in players:
        if key == 'player1':
            player_target = players.get(key)
            break

    if strategy == 'aggressive':
        for x in range(player.endurance):
            if is_adjacent(player.pos, player_target.pos, dim):
                # attack
                deal_damage(player, player_target)
                print(player_name + " attacks! --> target health: " + str(player_target.health))
            else:
                follow(player, player_target, board)
                print(player_name + " moves")
        print_board(board, math.sqrt(len(board)))


def process_turns(players):
    for key in players.keys():
        if not players.get(key).health <= 0:
            if key == "player1":
                process_player_turn(board, 'player1', players)
                if not game_continues(players):
                    break
            else:
                process_player_autoturn(board, key, players, "aggressive")
                if not game_continues(players):
                    break
        else:
            players.get(key).token = 0

        for p in players.values():
            p.endurance = p.max_endurance


if __name__ == '__main__':
    dim = 8
    board = create_empty_board(dim)
    player1 = Character(57, 1, 1, 1, 2, 2)
    player2 = Character(63, 2, 1, 1, 1, 2)
    player3 = Character(56, 3, 1, 1, 1, 2)
    player4 = Character(4, 4, 1, 1, 1, 2)
    player5 = Character(16, 5, 1, 1, 1, 2)
    players = {'player1': player1, 'player2': player2, 'player3': player3, 'player4': player4, 'player5': player5}
    update_board(board, dim, players)

    # print(get_x_y(8*8-1, board))

    print_board(board, dim)

    while game_continues(players):

        process_turns(players)
        update_board(board, dim, players)

        print("player1 health " + str(player1.health))
        print("player2 health " + str(player2.health))
        print("player3 health " + str(player3.health))
        print("player4 health " + str(player4.health))
        print("player5 health " + str(player5.health))
        print_board(board, dim)

    print("=====")
    print("=====")
    print_board(board, dim)

    for player in players:
        if not player.health == 0:
            print "player " + str(player.token) + " wins"
