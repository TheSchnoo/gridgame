from pygame.locals import *
from service import character_service


def on_event(app, event):
    if event.type == QUIT:
        app._running = False

    elif event.type == KEYDOWN:
        if event.unicode == 'q':
            app._running = False
            app.on_cleanup()

        if app.screen == 0:
            character_screen_on_key_down(app, event)
        elif app.screen == 1:
            choice_on_key_down(app, event)
        elif app.screen == 2:
            map_on_key_down(app, event)


def character_screen_on_key_down(app, event):
    if event.key == 113:                    # 'q' key
        app._running = False
        app.on_cleanup()

    elif event.key == 13:                   # 'enter' key
        name = "Moki"
        if app.character_pos == 0:
            name = "Joyce"
        elif app.character_pos == 1:
            name = "Wes"
        elif app.character_pos == 2:
            name = "Moki"
        app.set_character(character_service.get_character(name))
        app.next_screen()
    elif event.key == 276:                  # Left arrow
        if app.character_pos == 0:
            app.character_pos = 2
        elif app.character_pos == 1:
            app.character_pos = 0
        elif app.character_pos == 2:
            app.character_pos = 1

    elif event.key == 275:                  # Right arrow
        if app.character_pos == 0:
            app.character_pos = 1
        elif app.character_pos == 1:
            app.character_pos = 2
        elif app.character_pos == 2:
            app.character_pos = 0

    else:
        print(event)
    app.render_character_screen()


def map_on_key_down(app, event):
    if event.key == 273:                    # Up arrow
        app.move('n')
    elif event.key == 274:                  # Down arrow
        app.move('s')
    elif event.key == 276:                  # Left arrow
        app.move('w')
    elif event.key == 275:                  # Right arrow
        app.move('e')


def choice_on_key_down(app, event):
    if event.unicode == 'm':
        app.screen = 2
    else:
        print(event)

