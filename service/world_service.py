import xml.etree.ElementTree as ET

from domain.world import World
from service import battle_service

world_tree = ET.parse('xml/world.xml')
world_root = world_tree.getroot()
tree = ET.parse('xml/character.xml')
character_root = tree.getroot()


def print_world(world):
    distance = int(character_root.findall('distance')[0].text)

    if distance == 0:

        base_world_image = world.image

        if world.west_neighbor:
            base_world_image += "  <===="

        if world.east_neighbor:
            base_world_image += "  ====>"

        if world.north_neighbor:
            base_world_image = "\n    /\ " + \
                               "\n    ||" + \
                               "\n    ||" + base_world_image

        if world.south_neighbor:
            base_world_image = base_world_image + \
                               "\n    ||" + \
                               "\n    || " + \
                               "\n    \/"

        print(base_world_image)

    else:
        direction = character_root.findall('direction')[0].text

        if direction == 'n':
            print("| ^ |\n" +
                  "| ^ |\n" +
                  "| ^ |")
        elif direction == 's':
            print("| V |\n" +
                  "| V |\n" +
                  "| V |")
        elif direction == 'e':
            print("_______\n" +
                  ">  >  >\n" +
                  "-------")
        elif direction == 'w':
            print("_______\n" +
                  "<  <  <\n" +
                  "-------")


def add_distance(world, direction):
    # direction = character_root.findall('direction')[0].text
    distance = int(character_root.findall('distance')[0].text)

    if distance == 0:
        # direction = input("Direction? ")
        character_root.findall('direction')[0].text = direction

    distance_travelled = 1

    distance += distance_travelled

    target_world = ''
    target_distance = ''

    if direction == "n":
        target_world = world.north_neighbor
        target_distance = world.north_distance
    elif direction == "s":
        target_world = world.south_neighbor
        target_distance = world.south_distance
    elif direction == "e":
        target_world = world.east_neighbor
        target_distance = world.east_distance
    elif direction == "w":
        target_world = world.west_neighbor
        target_distance = world.west_distance

    if distance >= int(target_distance):
        character_root.findall('world')[0].text = target_world
        character_root.findall('distance')[0].text = '0'
    else:
        character_root.findall('distance')[0].text = str(distance)

    tree.write('xml/character.xml')

    return distance


def find_world(world_name):
    for world in world_root.findall('world'):
        if world.attrib.get('name') == world_name:
            return world


def get_world(world_name):
    world_xml = find_world(world_name)
    return World(world_xml.attrib.get('name'), north_neighbor=world_xml[1].text,
                 north_distance=world_xml[2].text, south_neighbor=world_xml[3].text,
                 south_distance=world_xml[4].text, east_neighbor=world_xml[5].text,
                 east_distance=world_xml[6].text, west_neighbor=world_xml[7].text,
                 west_distance=world_xml[8].text, image=world_xml[9].text)


def execute(player_name):
    world_xml = find_world()
    world0 = World(world_xml.attrib.get('name'), north_neighbor=world_xml[1].text,
                   north_distance=world_xml[2].text, south_neighbor=world_xml[3].text,
                   south_distance=world_xml[4].text, east_neighbor=world_xml[5].text,
                   east_distance=world_xml[6].text, west_neighbor=world_xml[7].text,
                   west_distance=world_xml[8].text, image=world_xml[9].text)

    print_world(world0)

    distance = add_distance(world0)

    world_xml = find_world()
    world1 = World(world_xml.attrib.get('name'), north_neighbor=world_xml[1].text,
                   north_distance=world_xml[2].text, south_neighbor=world_xml[3].text,
                   south_distance=world_xml[4].text, east_neighbor=world_xml[5].text,
                   east_distance=world_xml[6].text, west_neighbor=world_xml[7].text,
                   west_distance=world_xml[8].text, image=world_xml[9].text)

    # Some logic to decide when to battle
    # if not distance % 2 == 0:
    # battle_service.execute(player_name)

    # print_world(world1)


def get_traveling_world():
    return get_world("Path")
