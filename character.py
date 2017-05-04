import random

EMPTY_SPACE = 0


def print_attacks(attacks):
    for attack_key in attacks:
        print(attack_key + ": " + str(attacks.get(attack_key)))


class Character(object):

    def __init__(self, name, pos, token, attack, defense, speed, endurance, health, strategy):
        self.name = name
        self.pos = pos
        self.token = token
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.endurance = endurance
        self.health = health
        self.max_endurance = endurance
        self.strategy = strategy
        self.blocking = False

    # ============= DEFENSE =============

    def take_damage(self, damage):
        # if blocking, reduce damage taken
        if self.blocking:
            damage /= (10*self.defense)
            self.blocking = False
        # if defense high enough, get a chance of missing
        if is_chosen(self.defense/50):
            # chance of getting a miss
            if is_chosen(0.5):
                return self.health
        self.health -= damage
        return self.health

    # ============= OFFENSE =============

    def find_target(self, players, board):
        for key in players:
            if not players.get(key) == self:
                if board.is_adjacent(self.pos, players.get(key).pos) \
                        and players.get(key).health > 0:
                    return players.get(key)
        return

    def calculate_damage(self, damage):
        # randomizing factor
        endurance_penalty = 0
        miss_penalty = 0
        if not self.endurance == self.max_endurance:
            if is_chosen(0.1):
                endurance_penalty = 1-(self.max_endurance/100)*(5/self.endurance)
        if is_chosen(1-(2*self.attack/100)):
            miss_penalty = 0.5

        if is_chosen(endurance_penalty + miss_penalty):
            return 0

        return calculate_attack(damage)

    def choose_attack(self, target):
        attacks = {'1': self.attack}

        print_attacks(attacks)

        # list_attacks
        selected_attack = input("Which attack? ")

        # damage = select attacks from list
        damage = 0
        if attacks.get(selected_attack):
            damage = attacks.get(selected_attack)
        self.deal_damage(damage, target)

    def deal_damage(self, damage, player_target):
        self.face(player_target.pos)
        attack = self.calculate_damage(damage)

        # if defender is significantly faster than attacker, no directional effect
        if not player_target.speed >= self.speed * 2:
            if is_attack_from_side(self.token, player_target.token):
                attack *= 1.5
            elif is_attack_from_behind(self.token, player_target.token):
                attack *= 2.0

        if attack == 0:
            print("ATTACK IS 0!")

        print(self.name + " attacks! --> target health: " + str(player_target.health))
        print(player_target.take_damage(attack))
        player_target.face(self.pos)

    # ============= POSITIONING =============

    def face(self, position):
        if position == self.pos + 1:
            self.token = '>'
        elif position == self.pos - 1:
            self.token = '<'
        elif position > self.pos + 1:
            self.token = 'V'
        elif position < self.pos - 1:
            self.token = '^'

    def move_east(self, board):
        start = self.pos
        self.token = '>'
        target_space = start + 1
        if start % board.x_dim == board.x_dim - 1 and target_space > start:
            print("NO!")
        elif board.board[target_space] == EMPTY_SPACE:
            board.board[start] = EMPTY_SPACE
            board.board[target_space] = self.token
            self.pos = target_space
            return target_space
        return start

    def move_west(self, board):
        start = self.pos
        self.token = '<'
        target_space = start - 1
        if start % board.x_dim == 0 and target_space < start:
            print("NO!")
        elif board.board[target_space] == EMPTY_SPACE:
            board.board[start] = EMPTY_SPACE
            board.board[target_space] = self.token
            self.pos = target_space
            return target_space
        return start

    def move_north(self, board):
        start = self.pos
        self.token = '^'
        target_space = start - board.x_dim
        if target_space < 0:
            print("NO!")
        elif board.board[target_space] == EMPTY_SPACE:
            board.board[start] = EMPTY_SPACE
            board.board[target_space] = self.token
            self.pos = target_space
            return target_space
        return start

    def move_south(self, board):
        start = self.pos
        self.token = 'V'
        target_space = start + board.x_dim
        if target_space > len(board.board):
            print("NO!")
        elif board.board[target_space] == EMPTY_SPACE:
            board.board[start] = EMPTY_SPACE
            board.board[target_space] = self.token
            self.pos = target_space
            return target_space
        return start

    def move_x(self, board, horiz_dist):
        if horiz_dist >= 0:
            return self.move_east(board)
        else:
            return self.move_west(board)

    def move_y(self, board, vert_dist):
        if vert_dist >= 0:
            return self.move_south(board)
        else:
            return self.move_north(board)

    def follow(self, target, board):
        self_p = board.get_x_y(self.pos)
        target_p = board.get_x_y(target.pos)

        if abs(target_p.x - self_p.x) > abs(target_p.y - self_p.y):
            return self.move_x(board, target_p.x - self_p.x)
        else:
            return self.move_y(board, target_p.y - self_p.y)

    def travel(self, first_step, board):
        move_list = [first_step]
        steps = 1
        while steps < self.speed:
            next_move = input('And? ')
            move_list.append(next_move)
            steps += 1
        for move in move_list:
            if move == 'u':
                self.move_north(board)
            elif move == 'd':
                self.move_south(board)
            elif move == 'r':
                self.move_east(board)
            elif move == 'l':
                self.move_west(board)


# ============= HELPERS =============

def is_chosen(probability):
    return random.random() < probability


def calculate_attack(attack):
    if is_chosen(0.10):
        return attack*1.20
    elif is_chosen(0.10):
        return attack*.80
    return attack


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
