import random


class Character(object):

    def __init__(self, pos, token, attack, speed, endurance, health):
        self.pos = pos
        self.token = token
        self.attack = attack
        self.speed = speed
        self.endurance = endurance
        self.health = health
        self.max_endurance = endurance

    def take_damage(self, damage):
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


def is_chosen(probability):
    return random.random() < probability


def calculate_attack(attack):
    if is_chosen(0.10):
        return attack*1.20
    elif is_chosen(0.10):
        return attack*.80
    return attack
