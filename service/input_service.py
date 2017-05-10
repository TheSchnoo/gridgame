from service import exp_service
from service import world_service


def execute(player_name):
    new_input = input('Input: ')
    if new_input == 'w' or 'weights':
        exp_service.register_workout(player_name)
    elif new_input == 'r' or 'run':
        exp_service.register_run(player_name)
        world_service.add_distance()
    elif new_input == 'walk':
        world_service.add_distance()

    exp_service.process_exp(player_name)
