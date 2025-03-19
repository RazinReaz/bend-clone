from routine import routine
from exercise import exercise

import yaml

def load_exercises_from_yaml(yaml_file:str):
    with open(yaml_file, 'r') as file:
        exercise_dict = yaml.load(file, Loader=yaml.FullLoader)
    return exercise_dict

def load_routines_from_yaml(yaml_file:str):
    with open(yaml_file, 'r') as file:
        routines_dict = yaml.load(file, Loader=yaml.FullLoader)
    return routines_dict

def create_exercise(exercise_dict:dict) -> exercise:
    new_exercise = exercise(exercise_dict['name'], exercise_dict['difficulty'], exercise_dict['switch'])
    return new_exercise
    

def load_all_routines():
    routines = {}
    exercise_dicts = load_exercises_from_yaml('exercises.yaml')
    routines_dict = load_routines_from_yaml('routines.yaml')
    for routine_dict in routines_dict.values():
        routine_name = routine_dict["name"]
        new_routine = routine(routine_name)
        exercises_list = routine_dict['exercises'] # list of dictionaries

        for i, exercise_data in enumerate(exercises_list):
            exercise_name = exercise_data["name"]
            exercise_duration = exercise_data["duration"]
            new_exercise = create_exercise(exercise_dicts[exercise_name])
            new_routine.add_exercise(new_exercise, exercise_duration, i)
        routines[routine_name] = new_routine
    return routines

__all__ = ['load_all_routines']

if __name__ == '__main__':
    routines = load_all_routines()
    for routine_name, routine in routines.items():
        print(routine_name)
        print(routine)
        print('-----------------')