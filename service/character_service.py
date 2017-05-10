import xml.etree.ElementTree as ET

from domain.character import Character

character_tree = ET.parse('xml/character.xml')
character_root = character_tree.getroot()


def find_character(character_name):
    for character in character_root.findall('character'):
        if character.attrib.get('name') == character_name:
            return character


def get_character(character_name):
    character = find_character(character_name)
    return Character(character.attrib.get('name'), pos=0, token='<', attack=int(character[1].text),
                     defense=int(character[2].text), speed=int(character[3].text),
                     endurance=int(character[4].text), health=int(character[0].text), strategy='',
                     team=character[5].text)


def print_stats(character):
    print("Character Name : " + character.name + "  ||  Team : " + character.team + "\n" +
          "Attack : " + str(character.attack) + "\n" +
          "Defense : " + str(character.defense) + "\n" +
          "Speed : " + str(character.speed) + "\n" +
          "Endurance : " + str(character.endurance) + "\n" +
          "Health : " + str(character.health))


def get_current_world_name():
    tree = ET.parse('xml/character.xml')
    root = tree.getroot()
    return root.findall('world')[0].text


def get_distance():
    return int(character_root.findall('distance')[0].text)
