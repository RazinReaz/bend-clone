from load import *
import tkinter as tk
from tkinter import ttk, PhotoImage
import winsound
from routine import routine
import states
from PIL import Image, ImageTk


class bendapp:
    def __init__(self, root:tk.Tk) -> None:
        self.root = root

        self.root.title('Bend')
        self.root.geometry('300x600')
        
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
    def __init__(self, root: tk.Tk, app: bendapp, name: str) -> None:
        super().__init__(root)
        self.configure(bg="#f5f5f5", height=root.winfo_height(), width=root.winfo_width())

        # Title
        self.label = tk.Label(self, text="Welcome to Bend", font=("Helvetica", 20, "bold"), 
                              fg="#333", bg="#f5f5f5")
        self.label.pack(pady=20)

        # Frame for Routine Buttons
        self.button_frame = tk.Frame(self, bg="#f5f5f5")
        self.button_frame.pack(pady=10, fill="x")

        # Create Routine Buttons
        self.routine_buttons = []
        for index, page_name in enumerate(app.pages.keys()):
            if page_name == "home":
                continue
            btn = self.create_button(self.button_frame, page_name, "#030303", 
                                     lambda page=page_name: app.show_page(page))
            btn.grid(row=index, column=0, padx=5, pady=5, sticky="ew")
            self.routine_buttons.append(btn)

        # Make button frame expand
        self.button_frame.columnconfigure(0, weight=1)

    def create_button(self, parent, text, color, command):
        """Helper function to create styled buttons"""
        return tk.Button(parent, text=text, command=command, font=("Helvetica", 12), 
                         bg=color, fg="white", activebackground="#45a049", relief="flat", 
                         padx=10, pady=5)


class Routinepage(tk.Frame):
    def __init__(self, root: tk.Tk, app: bendapp, name: str) -> None:
        super().__init__(root)
        self.configure(bg="#f5f5f5", height=root.winfo_height(), width=root.winfo_width())

        self.name = name
        self.root = root
        self.app = app
        self.routine = app.routines[name]
        self.state = states.start(self.root, self, 0)
        self.running = False


        # Routine Name
        self.routine_name = tk.Label(self, text=f'{self.name}', font=('Helvetica', 12, 'bold'), fg="#333", bg="#f5f5f5")
        self.routine_name.pack(pady=10)

        # Exercise Label
        self.exercise_label = tk.Label(self, text='Exercise', font=('Helvetica', 10), fg="#555", bg="#f5f5f5")
        self.exercise_label.pack(pady=10)

         # 🟢 Create a frame that reserves space for the image
        self.image_frame = tk.Frame(self, width=200, height=200, bg="#f5f5f5")
        self.image_frame.pack(pady=10)

        # 🟢 Create a blank placeholder image
        self.placeholder_image = Image.new("RGBA", (200, 200), (255, 255, 255, 0))  # Transparent
        self.placeholder_image_tk = ImageTk.PhotoImage(self.placeholder_image)

        # 🟢 Create the Label and set the placeholder
        self.exercise_image = tk.Label(self.image_frame, image=self.placeholder_image_tk, bg="#f5f5f5", relief="ridge")
        self.exercise_image.image = self.placeholder_image_tk 
        self.exercise_image.pack(expand=True)

        # Progress Bar
        self.progress = ttk.Progressbar(self, orient='horizontal', length=250, mode='determinate', maximum=100)
        self.progress.pack(pady=10)

        self.exercise_time = tk.Label(self, text='', font=('Helvetica', 36), fg="#777", bg="#f5f5f5")
        self.exercise_time.pack(pady=5)

        # Start Button
        self.start_button = tk.Button(self, text='Start Routine', command=self.start_routine,
                                      font=("Helvetica", 10), bg="#030303", fg="white", 
                                      activebackground="#45a049", relief="flat", padx=10, pady=5)
        self.start_button.pack()

        # Control Buttons (Pause, Resume, Next)
        self.button_frame = tk.Frame(self, bg="#f5f5f5")
        self.button_frame.pack(padx=10, pady=10, fill='x')

        self.pause_button = self.create_button(self.button_frame, " Pause ", "#c6c6cc", lambda: self.state.pause_unpause())
        self.next_button = self.create_button(self.button_frame, "Next Exercise", "#c6c6cc", lambda: self.state.next())

        self.pause_button.grid(row=0, column=0, padx=5, sticky='ew')
        self.next_button.grid(row=0, column=1, padx=5, sticky='ew')

        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)

        # Back Button
        self.back_button = tk.Button(self, text='Back to Home', command=lambda: self.state.back_to_home(),
                                     font=("Helvetica", 10), bg="#f44336", fg="white", 
                                     activebackground="#d32f2f", relief="flat", padx=10, pady=5)
        self.back_button.pack(pady=10)

    def create_button(self, parent, text, color, command):
        """Helper function to create styled buttons"""
        return tk.Button(parent, text=text, command=command, font=("Helvetica", 10), bg=color, fg="#030303",
                         activebackground=color, relief="flat", padx=10, pady=5)

    def change_state(self, state) -> None:
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

