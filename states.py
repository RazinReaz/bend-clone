from abc import ABC, abstractmethod
import tkinter as tk
import winsound

class RoutineState(ABC):
    def __init__(self, root, page, exercise_index:int) -> None:
        super().__init__()
        self.root = root
        self.page = page
        self.exercise_index = exercise_index
        self.timer_id = None

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def pause(self):
        print("Pausing the routine")

    @abstractmethod
    def resume(self):
        print("Resuming the routine")

    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def render(self):
        pass

    def kill_current_timer(self):
        self.root.after_cancel(self.timer_id)

class start(RoutineState):
    def __init__(self, root, page, exercise_index:int) -> None:
        super().__init__(root, page, exercise_index)
        self.interval = 3
        
    def run(self):
        print(f"In state: START")
        if not self.page.running:
            self.render()
            return
        
        if self.interval == 0:
            self.next()
            return
        self.interval -= 1
        self.render()
        self.timer_id = self.root.after(1000, self.run)

    def pause(self):
        pass

    def resume(self):
        pass

    def next(self):
        self.root.after_cancel(self.timer_id)
        self.page.change_state(exercise(self.root, self.page, 0))
    
    def render(self):
        self.page.exercise_label.config(text='Get ready!')
        self.page.exercise_time.config(text=f'{self.interval}')
        self.page.progress['value'] = 0



class interval(RoutineState):
    def __init__(self, root, page, exercise_index:int) -> None:
        super().__init__(root, page, exercise_index)
        self.interval = 3

    def run(self):
        print(f"In state: INTERVAL")
        if self.interval == 0:
            self.next()
            return
        self.interval -= 1
        self.render()
        self.timer_id = self.root.after(1000, self.run)

    def pause(self):
        print("Pausing the interval")

    def resume(self):
        print("Resuming the interval")

    def next(self):
        # kill the scheduled function cal
        self.root.after_cancel(self.timer_id)
        self.page.change_state(exercise(self.root, self.page, self.exercise_index))
    
    def render(self):
        current_exercise_name:str = self.page.routine.stages[self.exercise_index][0].name
        self.page.exercise_label.config(text=f'Get ready for {current_exercise_name}!')
        image_path = f'./assets/img/exercise/{current_exercise_name}.png'
        try:
            exercise_image = tk.PhotoImage(file=image_path)
        except:
            exercise_image = tk.PhotoImage(file='./assets/img/exercise/Seated Fold.png')
        self.page.exercise_image.config(image=exercise_image)
        self.page.exercise_image.image = exercise_image

        self.page.exercise_time.config(text=f'{self.interval} seconds to go')
        self.page.progress['value'] = 0




class exercise(RoutineState):
    def __init__(self, root, page, exercise_index):
        super().__init__(root, page, exercise_index)
        self.exercise, self.duration = self.page.routine.stages[self.exercise_index][0], self.page.routine.stages[self.exercise_index][1]
        self.time_passed = 0

    def run(self):
        print(f"In state: EXERCISE, time_passed : {self.time_passed}")
        if self.time_passed == self.duration:
            self.next()
            return
        if self.time_passed == self.duration // 2 and self.exercise.switch:
            self.page.exercise_time.config(text='Switch sides')
            self.time_passed += 1
            self.timer_id = self.root.after(5000, self.run)
            return
        
        if self.time_passed > self.duration - 3 and self.time_passed < self.duration:
            winsound.Beep(500, 500)
            self.time_passed += 1


        self.render()
        self.time_passed += 1
        self.timer_id = self.root.after(1000, self.run)

    def pause(self):
        print("Pausing the exercise")
    
    def resume(self):
        print("Resuming the exercise")

    def next(self):
        self.root.after_cancel(self.timer_id)
        if self.exercise_index == len(self.page.routine.stages) - 1:
                self.page.change_state(complete(self.root, self.page, self.exercise_index))
                return
        self.page.change_state(interval(self.root, self.page, self.exercise_index + 1))

    def render(self):
        self.page.exercise_label.config(text=f'{self.exercise.name}')
        self.page.progress['value'] = self.time_passed / self.duration * 100
        self.page.exercise_time.config(text=f'{self.duration - self.time_passed} seconds remaining')


class complete(RoutineState):
    def __init__(self, root, page, exercise_index:int) -> None:
        super().__init__(root, page, exercise_index)
        self.interval = 5

    def run(self):
        print(f"In state: COMPLETE")
        self.render()
        if self.interval == 0:
            self.next()
            return
        self.interval -= 1
        self.timer_id = self.root.after(1000, self.run)
    
    def pause(self):
        pass

    def resume(self):
        pass

    def next(self):
        self.page.running = False
        self.root.after_cancel(self.timer_id)
        self.page.change_state(start(self.root, self.page, 0))

    def render(self):
        self.page.exercise_label.config(text='Routine complete!')
        self.page.exercise_time.config(text=f'You have completed the routine!')
        self.page.progress['value'] = 100