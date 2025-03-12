for routine in self.routines:
            routine_button = tk.Button(root, text=routine, command=lambda: self.do_nothing(routine))
            routine_button.pack(pady=5)