from board import Board
from character import Character


def game_continues(players):
    count = 0
    for player in players.values():
        if player.name == "p1" and player.health <= 0:
            return False
        elif player.health <= 0:
            count += 1
    if len(players) - count <= 1:
        return False
    return True


def process_player_turn(board, player_name, players):
    player = players.get(player_name)
    while player.endurance > 0:
        move = input('Your move: ')
        if move == 'u':
            player.move_north(board)
        elif move == 'd':
            player.move_south(board)
        elif move == 'r':
            player.move_east(board)
        elif move == 'l':
            player.move_west(board)
        elif move == 'a':
            player_target = player.find_target(players, board)
            if player_target:
                print(player.name + " " + str(player_target.pos))
                # player_target.take_damage(player.attack)
                deal_damage(player, player_target)
                print(player_name + " attacks! --> target health: " + str(player_target.health))
        player.endurance -= 1
        board.update(players)
        board.print_board()


def is_attack_from_side(attacker, defender):
    if ((attacker == '>' or attacker == '<') and (defender == 'V' or defender == '^')) \
            or ((attacker == 'V' or attacker == '^') and (defender == '>' or defender == '<')):
        print("attack from side!")
        return True
    return False


def is_attack_from_behind(attacker, defender):
    if attacker == defender:
        print("attack from behind!")
        return True
    return False


def deal_damage(player, player_target):
    player.face(player_target.pos, board.x_dim)
    attack = player.calculate_damage()
    if is_attack_from_side(player.token, player_target.token):
        attack *= 1.5
    elif is_attack_from_behind(player.token, player_target.token):
        attack *= 2.0
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
            if board.is_adjacent(player.pos, player_target.pos):
                # attack
                deal_damage(player, player_target)
                print(player_name + " attacks! --> target health: " + str(player_target.health))
            else:
                player.follow(player_target, board)
                print(player_name + " moves")
        board.print_board()


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
    board = Board(dim, dim)
    player1 = Character("p1", 57, '<', 1, 1, 2, 2)
    player2 = Character("p2", 63, 'V', 1, 1, 1, 2)
    player3 = Character("p3", 49, '^', 1, 1, 1, 2)
    player4 = Character("p4", 4, '>', 1, 1, 1, 2)
    player5 = Character("p5", 16, '<', 1, 1, 1, 2)
    players = {'player1': player1, 'player2': player2, 'player3': player3, 'player4': player4, 'player5': player5}
    board.update(players)

    board.print_board()

    while game_continues(players):

        process_turns(players)
        board.update(players)

        print("player1 health " + str(player1.health))
        print("player2 health " + str(player2.health))
        print("player3 health " + str(player3.health))
        print("player4 health " + str(player4.health))
        print("player5 health " + str(player5.health))
        board.print_board()

    print("=====")
    print("=====")
    board.print_board()

    if player1.health > 0:
        print("player " + str(player1.name) + " wins")
    else:
        print("player " + str(player1.name) + " loses")
