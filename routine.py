
import time
import winsound
import pyttsx3
from exercise import exercise


engine = pyttsx3.init()

def say_next_exercise(next_exercise) -> None:
    engine.say(f"Next {next_exercise}")
    engine.runAndWait()

class routine:
    def __init__(self, name:str) -> None:
        self.name: str = name
        self.stages: list[tuple] = []
    
    def add_exercise(self, exercise:exercise, time:int, index:int) -> None:
        self.stages.append((exercise, time, index))

    def __str__(self) -> str:
        routine_str = f'{self.name}\n'
        for stage in self.stages:
            routine_str += f'{stage[0]} for {stage[1]} seconds\n'
        return routine_str
    
    def _progress_bar(self, total_time:int, time_passed:int, max_width:int = 100, fill:str = '=') -> None:
        width = int(time_passed / total_time * max_width)
        print(f'[{width * fill}{(max_width - width) * "-"}]', end='\r')

        if time_passed == total_time:
            print()

    def interval_at_start(self, interval:int) -> None:
        for i in range(interval):
            self._progress_bar(interval, i, max_width=10, fill='*')
            time.sleep(1)
        self._progress_bar(interval, interval, max_width=10, fill='*')

    def exercise_first_half(self, stage:tuple) -> None:
        for i in range(stage[1] // 2):
            self._progress_bar(stage[1], i)
            time.sleep(1)

    def exercise_second_half(self, stage:tuple) -> None:
        for i in range(stage[1] // 2, stage[1]):
            self._progress_bar(stage[1], i)
            if i > stage[1] - 4:
                winsound.Beep(500, 500)
                time.sleep(0.5)
            else:
                time.sleep(1)
        self._progress_bar(stage[1], stage[1])


    
    def execute(self) -> None:
        for index, stage in enumerate(self.stages):
            # execute exercise
            
            print(f'{stage[0]} for {stage[1]} seconds')
            self.interval_at_start(5)
            self.exercise_first_half(stage) 
            if stage[0].switch:
                print("\nSwitch sides")
                winsound.Beep(500, 1000)   
                time.sleep(5)
            self.exercise_second_half(stage)
            if index < len(self.stages) - 1:
                say_next_exercise(self.stages[index + 1][0])

    

if __name__ == "__main__":
    toe_touch = exercise("Toe Touch", "easy", False)
    cross_leg_fold = exercise("Cross Leg Fold", "easy", True)
    wide_leg_bend = exercise("Wide Leg Bend", "easy", False)
    side_lunge = exercise("Side Lunge", "easy", True)
    reverse_lunge = exercise("Reverse Lunge", "easy", True)
    seated_fold = exercise("Seated Fold", "easy", False)
    hurdler = exercise("Hurdler", "easy", True)

    hamstring_1 = routine("Hamstring 1")
    hamstring_1.add_exercise(toe_touch, 30)
    hamstring_1.add_exercise(cross_leg_fold, 60)
    hamstring_1.add_exercise(wide_leg_bend, 30)
    hamstring_1.add_exercise(side_lunge, 60)
    hamstring_1.add_exercise(reverse_lunge, 60)
    hamstring_1.add_exercise(seated_fold, 30)
    hamstring_1.add_exercise(hurdler, 60)

    print(hamstring_1)
    hamstring_1.execute()


