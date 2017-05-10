import xml.etree.ElementTree as ET

tree = ET.parse('xml/character.xml')
character_root = tree.getroot()


def register_workout(player_name):
    for character in character_root.findall('character'):
        if character.attrib.get('name') == player_name:
            new_exp = int(character[6].attrib.get('exp'))
            new_exp += 1
            character[6].attrib['exp'] = str(new_exp)
            tree.write('character.xml')
            break


def register_run(player_name):
    for character in character_root.findall('character'):
        if character.attrib.get('name') == player_name:
            new_exp = int(character[9].attrib.get('exp')) + 1
            character[6].attrib['exp'] = str(new_exp)
            tree.write('character.xml')
            break


def process_exp(player_name):

    # exp points as key, corresponding level as value
    experience_map = {'0': '1', '2': '2', '4': '3', '7': '4', '10': '5', '14': '6'}

    for character in character_root.findall('character'):
        if character.attrib.get('name') == player_name:
            for attribute in character:
                if attribute.attrib and attribute.attrib['exp'] in experience_map:
                    attribute.attrib['level'] = experience_map.get(attribute.attrib['exp'])
                    attribute.attrib['exp'] = str(0)
                    if attribute.tag == 'power_exp':
                        character[1].text = str(int(character[1].text) + int(attribute.attrib['level']))
            tree.write('character.xml')
            break
