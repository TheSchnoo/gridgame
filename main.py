from app import App
from service import battle_service, input_service, world_service
from service import character_service

if __name__ == '__main__':

    player_name = ""
    app = App()
    app.on_execute()

    name = "Moki"
    if app.character_pos == 0:
        name = "Joyce"
    elif app.character_pos == 1:
        name = "Wes"
    elif app.character_pos == 2:
        name = "Moki"
    character = character_service.get_character(name)

    print("You selected " + character.name)

    while 1:
        action = input("\nStart!\n(Type h for help) ")
        if action == 'm':
            world_service.execute(player_name)
        elif action == 'b':
            battle_service.execute(player_name)
        elif action == 'i':
            input_service.execute(player_name)
        elif action == 'q':
            break
        elif action == 'h':
            print("Help \n" +
                  "m = map, i = input, b = battle:")
