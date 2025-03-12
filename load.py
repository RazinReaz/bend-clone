from routine import routine
from exercise import exercise

import yaml



def load_routines_from_yaml(yaml_file:str):
    with open(yaml_file, 'r') as file:
        routines_dict = yaml.load(file, Loader=yaml.FullLoader)
    return routines_dict

def create_exercise(exercise_dict:dict) -> exercise:
    new_exercise = exercise(exercise_dict['name'], exercise_dict['difficulty'], exercise_dict['switch'])
    return new_exercise
    

def load_all_routines():
    routines = {}
    routines_dict = load_routines_from_yaml('routines.yaml')
    for routine_name, routine_dict in routines_dict.items():
        new_routine = routine(routine_name)
        exercises_data = routine_dict['exercises'] # list of dictionaries

        for i, exercise_dict in enumerate(exercises_data):
            new_exercise = create_exercise(exercise_dict)
            new_routine.add_exercise(new_exercise, exercise_dict['duration'], i)
        routines[routine_name] = new_routine
    return routines

__all__ = ['load_all_routines']

if __name__ == '__main__':
    routines = load_all_routines()
    for routine_name, routine in routines.items():
        print(routine_name)
        print(routine)
        print('-----------------')