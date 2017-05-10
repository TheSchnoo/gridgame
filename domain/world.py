class World(object):

    def __init__(self, name, north_neighbor, north_distance, south_neighbor, south_distance,
                 east_neighbor, east_distance, west_neighbor, west_distance, image):
        self.name = name
        self.west_distance = west_distance
        self.west_neighbor = west_neighbor
        self.east_distance = east_distance
        self.east_neighbor = east_neighbor
        self.south_distance = south_distance
        self.south_neighbor = south_neighbor
        self.north_distance = north_distance
        self.north_neighbor = north_neighbor
        self.image = image

            # " \n" + \
            # "/*****\     \n" + \
            # "|[]   |     \n" + \
            # "|   []|   /*****\  \n" + \
            # "|  _  |  |[] _   |\n" + \
            # "|_| |_|  |__| |__|"

    def set_image(self, image):
        if self.name == "Whistler":
            self.image = "   /\    " + \
                         "  /   \/\  " + \
                         " /   /\  \ " + \
                         "/   /   \ \ "

        elif self.name == "Ocean":
            self.image = "~~~~~~~~~~~~" + \
                         "~~~~~~~~~~~~" + \
                         "ooo~~ooooo~~" + \
                         "oooo~ooooooo"