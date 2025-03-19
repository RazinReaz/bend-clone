from abc import ABC, abstractmethod
import tkinter as tk
import winsound
import threading
from PIL import Image, ImageTk  # Import Pillow


class RoutineState(ABC):
    def __init__(self, root, page, exercise_index:int) -> None:
        super().__init__()
        self.root = root
        self.page = page
        self.exercise_index = exercise_index
        self.timer_id = None
        self.paused = False

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def next(self) -> None:
        pass

    @abstractmethod
    def render(self) -> None:
        pass

    def back_to_home(self) -> None:
        if self.timer_id:
            self.root.after_cancel(self.timer_id) # because while paused, there is no timer id
        self.page.exercise_image.image = self.page.placeholder_image
        self.page.progress['value'] = 0
        self.page.exercise_time.config(text='')
        self.page.running = False
        self.page.change_state(start(self.root, self.page, 0))
        self.page.app.show_page('home')

    def pause_unpause(self) -> None:
        if self.timer_id:
            self.paused = True
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
            self.page.pause_button.config(text='Unpause')
        elif self.paused:
            self.page.pause_button.config(text=' Pause ')
            self.paused = False
            self.run()
        

class start(RoutineState):
    def __init__(self, root, page, exercise_index:int) -> None:
        super().__init__(root, page, exercise_index)

        
    def run(self) -> None:
        if not self.page.running: # when this page appears after state:COMPLETED
            self.render()
            return
        
        self.timer_id = self.root.after(1000, self.next)

    def next(self) -> None:
        self.root.after_cancel(self.timer_id)
        self.page.change_state(interval(self.root, self.page, 0))
    
    def render(self) -> None:
        self.page.routine_name.config(text=f'{self.exercise_index+1} of {len(self.page.routine.stages)}')
        self.page.exercise_label.config(text='Get ready!')
        self.page.progress['value'] = 0



class interval(RoutineState):
    def __init__(self, root, page, exercise_index:int) -> None:
        super().__init__(root, page, exercise_index)
        self.interval = 5
    

    def run(self) -> None:
        if self.interval == 0:
            self.next()
            return
        self.interval -= 1
        self.render()
        self.timer_id = self.root.after(1000, self.run)

    def next(self) -> None:
        self.root.after_cancel(self.timer_id)
        self.page.change_state(exercise(self.root, self.page, self.exercise_index))
    
    def render(self):
        current_exercise_name:str = self.page.routine.stages[self.exercise_index][0].name
        self.page.routine_name.config(text=f'{self.exercise_index+1} of {len(self.page.routine.stages)}')
        self.page.exercise_label.config(text=f'Get ready for {current_exercise_name}!')
        self.show_exercise_image(current_exercise_name)

        self.page.exercise_time.config(text=f'{self.interval}')
        self.page.progress['value'] = 0

    def show_exercise_image(self, current_exercise_name):
        image_path = f'./assets/img/exercise/{current_exercise_name}.png'

        try:
            image = Image.open(image_path)
        except:
            image = self.page.placeholder_image

        # Resize to consistent resolution (e.g., 200x200)
        image = image.resize((200, 200), Image.Resampling.LANCZOS)
        exercise_image = ImageTk.PhotoImage(image)
        self.page.exercise_image.config(image=exercise_image, bg="#f5f5f5")
        self.page.exercise_image.image = exercise_image  # Keep reference to avoid garbage collection




class exercise(RoutineState):
    def __init__(self, root, page, exercise_index):
        super().__init__(root, page, exercise_index)
        self.exercise, self.duration = self.page.routine.stages[self.exercise_index][0], self.page.routine.stages[self.exercise_index][1]
        self.time_passed = 0
    
    def beep_last_seconds(self, cutoff_time: int, before: int = 3) -> None:
        if self.time_passed == cutoff_time - before:
            def beep():
                for _ in range(before): 
                    winsound.Beep(500, 500) 
                    threading.Event().wait(0.5)  
            self.beep_thread = threading.Thread(target=beep, daemon=True)
            self.beep_thread.start()

    def run(self):
        if self.time_passed > self.duration:
            self.next()
            return
        if self.time_passed == self.duration // 2 and self.exercise.switch:
            self.page.exercise_time.config(text='Switch sides')
            self.time_passed += 1
            self.timer_id = self.root.after(5000, self.run)
            return
        if self.exercise.switch:
            self.beep_last_seconds(self.duration // 2)
        self.beep_last_seconds(self.duration)


        self.render()
        self.time_passed += 1
        self.timer_id = self.root.after(1000, self.run)

    def next(self):
        self.root.after_cancel(self.timer_id)
        if self.exercise_index == len(self.page.routine.stages) - 1:
                self.page.change_state(complete(self.root, self.page, self.exercise_index))
                return
        self.page.change_state(interval(self.root, self.page, self.exercise_index + 1))

    def render(self):
        self.page.exercise_label.config(text=f'{self.exercise.name}')
        self.page.progress['value'] = self.time_passed / self.duration * 100
        self.page.exercise_time.config(text=f'{self.duration - self.time_passed}')


class complete(RoutineState):
    def __init__(self, root, page, exercise_index:int) -> None:
        super().__init__(root, page, exercise_index)
        self.interval = 5

    def run(self):
        self.render()
        if self.interval == 0:
            self.next()
            return
        self.interval -= 1
        self.timer_id = self.root.after(1000, self.run)

    def next(self):
        self.page.running = False
        self.root.after_cancel(self.timer_id)
        self.page.change_state(start(self.root, self.page, 0))

    def render(self):
        self.page.exercise_label.config(text='Routine complete!')
        self.page.progress['value'] = 100