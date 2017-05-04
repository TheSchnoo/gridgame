import random

EMPTY_SPACE = 0


class Character(object):

    def __init__(self, name, pos, token, attack, speed, endurance, health, strategy):
        self.name = name
        self.pos = pos
        self.token = token
        self.attack = attack
        self.speed = speed
        self.endurance = endurance
        self.health = health
        self.max_endurance = endurance
        self.strategy = strategy
        self.blocking = False

    def take_damage(self, damage):
        # if blocking, reduce damage taken
        if self.blocking:
            damage /= 10
            self.blocking = False
        # if 'evasive' enough, get a chance of missing
        if is_chosen(self.speed/50):
            # chance of getting a miss
            if is_chosen(0.5):
                return self.health
        self.health -= damage
        return self.health

    def calculate_damage(self):
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

        return calculate_attack(self.attack)

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
        target_space = start + self.speed
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
        target_space = start - self.speed
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
        target_space = start - (self.speed * board.x_dim)
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
        target_space = start + (self.speed * board.x_dim)
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

    def find_target(self, players, board):
        for key in players:
            if not players.get(key) == self:
                if board.is_adjacent(self.pos, players.get(key).pos) \
                        and players.get(key).health > 0:
                    return players.get(key)
        return


def is_chosen(probability):
    return random.random() < probability


def calculate_attack(attack):
    if is_chosen(0.10):
        return attack*1.20
    elif is_chosen(0.10):
        return attack*.80
    return attack
