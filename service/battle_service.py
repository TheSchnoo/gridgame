import xml.etree.ElementTree as ET
from collections import OrderedDict

from service import level_service

tree = ET.parse('xml/character.xml')
character_root = tree.getroot()


# Determines if the game should continue
def game_continues(players):
    users_remain = False
    koombas_remain = False

    for player in players.values():
        if player.team == 'schnoos' and player.health > 0:
            users_remain = True
        else:
            if player.health > 0:
                koombas_remain = True

        if player.blocking:
            player.blocking = False

    if users_remain and koombas_remain:
        return True
    elif users_remain:
        print('The Schnoos win!')
    else:
        print('The Koombas win...')
    return False


# User-controlled character turns
def process_player_turn(board, player_name, players):
    player = players.get(player_name)
    while player.endurance > 0:
        move = input('Your move: ')
        if move == 'u' or move == 'd' or move == 'r' or move == 'l':
            player.travel(move, board)
        elif move == 'b':
            player.blocking = True
            player.endurance = 0
        elif move == 'a':
            player_target = player.find_target(players, board)
            if player_target:
                player.choose_attack(player_target)
        player.endurance -= 1
        board.update(players)
        board.print_board()


# CPU-controlled character turns
def process_player_autoturn(board, player_name, players):
    player = players.get(player_name)
    player_target = ""
    for potential_target in players.values():
        if potential_target.team == 'schnoos':
            player_target = potential_target
            break
    while player.endurance > 0:
        if board.is_adjacent(player.pos, player_target.pos):
            if player.strategy == 'aggressive':
                # attack
                player.choose_attack(player_target)
            elif player.strategy == 'defensive':
                if player.health > player_target.health:
                    # attack
                    player.choose_attack(player_target)
                else:
                    # block
                    player.blocking = True
                    player.endurance = 0
                print(player_name + " blocks")
        else:
            player.follow(player_target, board)
            print(player_name + " moves")
            # board.print_board()
        board.update(players)
        player.endurance -= 1
        # board.print_board()


# Assign turns for players in a game
def process_turns(board, players):
    for player in players.values():
        if not player.health <= 0:
            if player.team == 'schnoos':
                process_player_turn(board, player.name, players)
                if not game_continues(players):
                    break
            else:
                process_player_autoturn(board, player.name, players)
                if not game_continues(players):
                    break
        else:
            player.token = 0

    for p in players.values():
        p.endurance = p.max_endurance


def execute(player_name):

    board_and_players_list = level_service.build_board(player_name)

    board = board_and_players_list[0]
    players = board_and_players_list[1]

    players_sorted = OrderedDict(sorted(players.items(), key=lambda t: t[1].speed, reverse=True))

    while game_continues(players):
        process_turns(board, players_sorted)
        board.update(players)

        for player in players.values():
            print(player.name + " health: " + str(player.health))
        board.print_board()

    print("=====")
    print("=====")
    board.print_board()
