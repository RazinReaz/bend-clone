from load import *
import tkinter as tk
from tkinter import ttk, PhotoImage
import winsound
from routine import routine
import states

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
        self.state = states.start(self.root, self, 0)
        self.running = False

        self.routine_name = tk.Label(self, text=f'{self.name}', font=('Consolas', 24))
        self.routine_name.pack(pady=10)

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

        self.button_frame = tk.Frame(self)
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)

        self.pause_button = tk.Button(self.button_frame, text='Pause', command=lambda: self.state.pause())
        self.pause_button.grid(row=0, column=0, sticky='ew')

        self.resume_button = tk.Button(self.button_frame, text='Resume', command=lambda: self.state.resume())
        self.resume_button.grid(row=0, column=1, sticky='ew')

        self.next_button = tk.Button(self.button_frame, text='Next exercise', command=lambda: self.state.next())
        self.next_button.grid(row=0, column=2, sticky='ew')

        self.button_frame.pack(pady=10, fill='x')

        self.back_button = tk.Button(self, text='Back to home', command=lambda: app.show_page('home')) #! kill the current, then change
        self.back_button.pack(pady=10)
    
    def change_state(self, state:states.RoutineState) -> None:
        self.state = state
        self.run_state()

    def run_state(self) -> None:
        self.state.run()
    
    def start_routine(self) -> None:
        if not self.running:
            self.running = True
            self.state.run()
            

if __name__ == '__main__':
    root = tk.Tk()
    app = bendapp(root)
    root.mainloop()

