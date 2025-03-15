from load import *
import tkinter as tk
from tkinter import ttk, PhotoImage
import winsound
from routine import routine
# TODO Tkinter GUI
# TODO do it without time.sleep


class bendapp:
    def __init__(self, root:tk.Tk) -> None:
        self.root = root

        self.root.title('Bend')
        self.root.geometry('400x700')
        
        self.routines = load_all_routines()
        self.pages = {}
        self.create_pages()

        self.frames = {}
        for page_name, pageClass in self.pages.items():
            page = pageClass(self.root, self, page_name)
            self.frames[page_name] = page
            page.grid(row=0, column=0, sticky='nsew')
        
        self.show_page('home')

    def create_pages(self) -> None:
        self.pages['home'] = Homepage
        for routine_name in self.routines.keys():
            self.pages[routine_name] = Routinepage

    def log(self, page_name:str) -> None:
        print(f'Page name {page_name}')

    

    def show_page(self, page_name:str) -> None:
        self.log(page_name)
        self.current_frame = self.frames[page_name]
        self.current_frame.tkraise()

            
        
class Homepage(tk.Frame):
    def __init__(self, root:tk.Tk, app:bendapp, name:str) -> None:
        super().__init__(root)

        self.configure(bg="lightblue", height=400, width=500)
        self.label = tk.Label(self, text='Welcome to Bend', font=('Consolas', 24))
        self.label.pack(pady=20, padx=20)
        self.routine_buttons = []

        for page_name in app.pages.keys():
            if page_name == 'home':
                continue
            routine_button = tk.Button(self, text=page_name, command=lambda page_name=page_name: app.show_page(page_name))
            self.routine_buttons.append(routine_button)
            routine_button.pack(pady=10)

class Routinepage(tk.Frame):
    def __init__(self, root:tk.Tk, app:bendapp, name: str) -> None:
        super().__init__(root)

        self.configure(bg="lightgray")

        self.name = name
        self.root = root
        self.routine = app.routines[name]
        
        self.label = tk.Label(self, text=f'{self.name}', font=('Consolas', 24))
        self.label.pack(pady=10)

        self.exercise_label = tk.Label(self, text='Exercise', font=('Consolas', 16))
        self.exercise_label.pack(pady=10)

        self.exercise_image = tk.Label(self, text=f'') # make it empty to hold image next
        self.exercise_image.pack(pady=10)


        self.progress = ttk.Progressbar(self, orient='horizontal', length=200, mode='determinate', maximum=100)
        self.progress.pack(pady=10)
        self.exercise_time = tk.Label(self, text='', font=('Consolas', 16))
        self.exercise_time.pack(pady=10)

        self.start_button = tk.Button(self, text='Start routine', command=lambda: self.start_routine())
        self.start_button.pack(padx=20)

        self.next_button = tk.Button(self, text='Next exercise', command=lambda: self.execute_next_exercise())
        self.next_button.pack(pady=20)

        self.running = False

        self.back_button = tk.Button(self, text='Back to home', command=lambda: app.show_page('home'))
        self.back_button.pack(pady=10)

    def start_routine(self) -> None:
        if not self.running:
            self.running = True
            self.current_index = 0
            exercise_name = self.routine.stages[self.current_index][0]
            self.interval_at_start(exercise_name, 3)

    def interval_at_start(self, exercise_name:str, interval:int) -> None:
        if interval == 0:
            self.execute_exercise_at(self.current_index)
            return
        self.exercise_label.config(text=f'Get ready for {exercise_name}!')
        image_path = f'./assets/img/exercise/{exercise_name}.png'
        try:
            exercise_image = PhotoImage(file=image_path)
        except:
            exercise_image = PhotoImage(file='./assets/img/exercise/Seated Fold.png')
        self.exercise_image.config(image=exercise_image)
        self.exercise_image.image = exercise_image

        self.exercise_time.config(text=f'{interval} seconds to go')
        self.progress['value'] = 0
        self.root.after(1000, self.interval_at_start, exercise_name, interval - 1)


    def execute_exercise_at(self, index) -> None:
        exercise, duration, exercise_index = self.routine.stages[index]
        self.exercise_label.config(text=f'{exercise}')
        
        self.progress['value'] = 0
        time_passed = 0
        self.execute_exercise(exercise, time_passed, duration, exercise_index)

    def execute_exercise(self, exercise, time_passed:int, duration:int, exercise_index:int) -> None:
        if exercise_index != self.current_index: # will not run if the exercise has been switched
            return
        # show image of exercise
        self.progress['value'] = time_passed / duration * 100
        self.exercise_time.config(text=f'{duration - time_passed} seconds remaining')
        print(f'{exercise} for {duration} seconds: {time_passed} seconds passed')

        # switch sides if necessary
        if time_passed == duration // 2 and exercise.switch:
            self.exercise_time.config(text='Switch sides')
            self.root.after(5000, self.execute_exercise, exercise, time_passed + 1, duration, exercise_index)
            return
        elif time_passed >= duration - 3 and time_passed < duration:
            winsound.Beep(500, 500)
            self.root.after(500, self.execute_exercise, exercise, time_passed + 1, duration, exercise_index)
            return
        elif time_passed == duration:
            self.exercise_time.config(text='')
            self.progress['value'] = 100
            self.root.after(1000, self.update_index)
            return
        else:
            self.root.after(1000, self.execute_exercise, exercise, time_passed + 1, duration, exercise_index)

    def execute_next_exercise(self) -> None:
        if self.running:
            self.update_index()

    def update_index(self) -> None:
        self.current_index += 1
        if self.current_index >= len(self.routine.stages):
            self.exercise_label.config(text='Routine complete!')
            self.running = False
        else:
            exercise_name = self.routine.stages[self.current_index][0]
            self.interval_at_start(exercise_name, 5)
            

if __name__ == '__main__':
    root = tk.Tk()
    app = bendapp(root)
    root.mainloop()

