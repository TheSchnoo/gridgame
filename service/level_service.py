import random
import xml.etree.ElementTree as ET

from domain.board import Board
from domain.character import Character
from service import character_service

character_tree = ET.parse('xml/character.xml')
level_tree = ET.parse('xml/levels.xml')
character_root = character_tree.getroot()
level_root = level_tree.getroot()


def find_level(level_number):
    for level in level_root.findall('level'):
        if level.attrib.get('number') == level_number:
            return level


def build_board(player_name):

    players = {}

    character = character_service.find_character(player_name)
    user = Character(character.attrib.get('name'), pos=0, token='<', attack=int(character[1].text),
                     defense=int(character[2].text), speed=int(character[3].text),
                     endurance=int(character[4].text),
                     health=int(character[0].text), strategy='', team=character[5].text)

    players[user.name] = user

    level = find_level("1")
    dim = int(level[0].text) # dim
    multiplier = int(level[2].text)  # koobas multiplier
    counter = 0
    grunt_xml = character_service("grunt")
    print(grunt_xml[5].text)

    while counter < int(level[1].text): # koombas

        location = random.randint(1, dim*dim-1)
        koomba = Character("koomba" + str(counter), location, 'V', int(grunt_xml[1].text)*multiplier,
                           int(grunt_xml[2].text)*multiplier, int(grunt_xml[3].text)*multiplier,
                           int(grunt_xml[4].text)*multiplier, int(grunt_xml[0].text)*multiplier, 'aggressive',
                           grunt_xml[5].text)
        players[koomba.name] = koomba
        counter += 1

    board = Board(dim, dim)

    # 'player4': player4, 'player5': player5}
    board.update(players)

    # board.print_board()

    return [board, players]
