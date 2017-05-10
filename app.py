import pygame

from service import character_service
from service import event_service
from service import world_service

SCREEN_X = 500
SCREEN_Y = 500
clock = pygame.time.Clock()

CHARACTER_SCREEN = 0
MAP_SCREEN = 2


class App:
    def __init__(self):
        self.character_pos = 0
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._pointer = None
        self.screen = 0
        self.offset = 0
        self.character = None

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((SCREEN_X, SCREEN_Y), pygame.HWSURFACE)
        self._running = True
        self.render_screen()

    def on_event(self, event):
        event_service.on_event(self, event)

    def on_loop(self):
        pass

    def on_render(self):
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
            self.on_cleanup()

        while (self._running):
            if self.screen == 0:
                if clock.tick() % 2 == 0:
                    self.update_pointer()
            self.render_screen()
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def render_pointer(self):
        if self.character_pos == 0:

            self._display_surf.blit(self._pointer, (100, 0 + self.offset))
        elif self.character_pos == 1:

            self._display_surf.blit(self._pointer, (230, 10 + self.offset))
        elif self.character_pos == 2:

            self._display_surf.blit(self._pointer, (400, 50 + self.offset))

    def clear_screen(self):
        self._display_surf.fill((0, 0, 0))
        # self._display_surf.blit(self._image_surf, (0, 0))

    def next_screen(self):
        self.clear_screen()
        self.screen += 1
        self.render_screen()

    def render_screen(self):
        self.clear_screen()
        if self.screen == CHARACTER_SCREEN:
            self.display_background("img/character_screen_base.jpg")

            self._pointer = pygame.image.load("img/dino.gif").convert()
            self.render_pointer()

        elif self.screen == 1:
            self._display_surf.fill((0, 0, 0))

        elif self.screen == MAP_SCREEN:
            # print(character_service.get_distance())
            world_name = character_service.get_current_world_name()
            if character_service.get_distance() == 0:
                display_world = world_service.get_world(world_name)
            else:
                display_world = world_service.get_traveling_world()
            print(display_world.name)
            self.display_background(display_world.image)

    def update_pointer(self):
        if self.offset == 0:
            self.offset = 5
        elif self.offset == 5:
            self.offset = 1
        elif self.offset == 1:
            self.offset = - 5
        elif self.offset == -5:
            self.offset = 0
        self.render_pointer()

    def display_background(self, image_url):
        picture = pygame.image.load(image_url).convert()
        picture = pygame.transform.scale(picture, (SCREEN_X, SCREEN_Y))
        self._image_surf = picture
        self._display_surf.blit(self._image_surf, (0, 0))

    def set_character(self, character):
        self.character = character

    def move(self, direction):
        current_world = world_service.get_world(character_service.get_current_world_name())
        world_service.add_distance(current_world, direction)


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
