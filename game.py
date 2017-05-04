from board import Board
from character import Character


# Determines if the game should continue
def game_continues(players):
    count = 0
    for player in players.values():
        if player.name == "p1" and player.health <= 0:
            return False
        elif player.health > 0 and player.blocking:
            player.blocking = False
        elif player.health <= 0:
            count += 1
    if len(players) - count <= 1:
        return False
    return True


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


def process_player_autoturn(board, player_name, players):

    player = players.get(player_name)
    player_target = ""
    for key in players:
        if key == 'player1':
            player_target = players.get(key)
            break
    while player.endurance > 0:
        if board.is_adjacent(player.pos, player_target.pos):
                if player.strategy == 'aggressive':
                    # attack
                    deal_damage(player, player_target)
                elif player.strategy == 'defensive':
                    if player.health > player_target.health:
                        # attack
                        deal_damage(player, player_target)
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


def process_turns(players):
    for key in players.keys():
        if not players.get(key).health <= 0:
            if key == "player1":
                process_player_turn(board, 'player1', players)
                if not game_continues(players):
                    break
            else:
                process_player_autoturn(board, key, players)
                if not game_continues(players):
                    break
        else:
            players.get(key).token = 0

        for p in players.values():
            p.endurance = p.max_endurance


if __name__ == '__main__':
    dim = 8
    board = Board(dim, dim)
    player1 = Character(name="p1", pos=57, token='<', attack=1,
                        defense=1, speed=3, endurance=2, health=2, strategy='')
    player2 = Character("p2", 63, 'V', 1, 1, 1, 1, 2, 'aggressive')
    player3 = Character("p3", 49, '^', 1, 1, 1, 1, 2, 'defensive')
    player4 = Character("p4", 4, '>', 1, 1, 1, 1, 2, 'aggressive')
    player5 = Character("p5", 16, '<', 1, 1, 1, 1, 2, 'aggressive')
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
