'''
Filename: 

Purpose: To make an attempt at my first GUI program. This is a sticky note app that (to the best of my abilities)
that works kinda like a real sticky note pad.

Author: Kavin Hooker
'''
import tkinter as tk
from tkinter import messagebox
import tkinter.simpledialog as simpledialog

class StickyNoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sticky Note")

        # Tracks the page number and names
        self.page_number = 1
        self.pages = {}
        self.page_names = {self.page_number: "Page 1"}  # Store page names

        # Sets the size of the sticky note window
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        # Creates a Frame to hold the entire content and set a gray border for the window
        self.window_frame = tk.Frame(self.root, bg='gray', bd=10)  # Gray border with padding 10
        self.window_frame.pack(fill=tk.BOTH, expand=True)

        # Makes the window movable
        self.is_moving = False
        self.offset_x = 0
        self.offset_y = 0

        # Creates a frame to hold the text area and buttons
        self.main_frame = tk.Frame(self.window_frame)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Creates a Text widget for writing
        self.text_area = tk.Text(self.main_frame, wrap=tk.WORD, height=15, width=30)
        self.text_area.grid(row=0, column=0, padx=10, pady=10)

        # Creates a frame for the buttons to the right of the text area
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.grid(row=0, column=1, padx=10, pady=10)

        # Creates buttons
        self.toggle_button = tk.Button(self.button_frame, text="Toggle Dark Mode", command=self.toggle_dark_mode)
        self.toggle_button.pack(fill=tk.X, pady=5)

        self.prev_button = tk.Button(self.button_frame, text="\u2B05 Previous", font=("Arial", 12), command=self.previous_page)
        self.prev_button.pack(fill=tk.X, pady=5)

        self.next_button = tk.Button(self.button_frame, text="\u27A1 Next        ", font=("Arial", 12), command=self.next_page)
        self.next_button.pack(fill=tk.X, pady=5)


        # Rip off page button
        self.ripoff_button = tk.Button(self.button_frame, text="\u2702 Rip off page", font=("Arial", 12), command=self.rip_off_page)
        self.ripoff_button.pack(fill=tk.X, pady=5)

        # Rename page button
        self.rename_button = tk.Button(self.button_frame, text="Rename Page", command=self.rename_page)
        self.rename_button.pack(fill=tk.X, pady=5)

        # Creates a simple menu to store pages
        self.pages[self.page_number] = ""

        # Binds mouse events to make window movable
        self.root.bind("<Button-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.do_move)
        self.root.bind("<ButtonRelease-1>", self.stop_move)

        # Applies the initial page color
        self.update_page_color()

    def start_move(self, event):
        # Initiates dragging
        self.is_moving = True
        self.offset_x = event.x
        self.offset_y = event.y

    def do_move(self, event):
        # Moves window while dragging
        if self.is_moving:
            delta_x = event.x - self.offset_x
            delta_y = event.y - self.offset_y
            self.root.geometry(f'+{self.root.winfo_x() + delta_x}+{self.root.winfo_y() + delta_y}')

    def stop_move(self, event):
        # Stops dragging
        self.is_moving = False

    def toggle_dark_mode(self):
        # Toggles between dark and light mode
        current_bg = self.root.cget('background')
        if current_bg == 'black':
            self.root.configure(background='white')
            self.text_area.configure(bg='white', fg='black')
            self.toggle_button.configure(bg='light gray', fg='black')
            self.prev_button.configure(bg='light gray', fg='black')
            self.next_button.configure(bg='light gray', fg='black')
            self.ripoff_button.configure(bg='light gray', fg='black')
            self.rename_button.configure(bg='light gray', fg='black')
        else:
            self.root.configure(background='black')
            self.text_area.configure(bg='black', fg='white')
            self.toggle_button.configure(bg='dark gray', fg='white')
            self.prev_button.configure(bg='dark gray', fg='white')
            self.next_button.configure(bg='dark gray', fg='white')
            self.ripoff_button.configure(bg='dark gray', fg='white')
            self.rename_button.configure(bg='dark gray', fg='white')

    def previous_page(self):
        # Goes to the previous page
        if self.page_number > 1:
            self.pages[self.page_number] = self.text_area.get(1.0, tk.END).strip()
            self.page_number -= 1
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, self.pages.get(self.page_number, ""))
            self.update_page_color()
        else:
            messagebox.showinfo("You can\'t do that", "You're already on the first page.")

    def next_page(self):
        # Goes to the next page
        self.pages[self.page_number] = self.text_area.get(1.0, tk.END).strip()
        self.page_number += 1
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, self.pages.get(self.page_number, ""))
        self.update_page_color()

    def rip_off_page(self):
        # Rips off the current page into a new movable window
        # Creates a new top-level window for the ripped-off sticky note
        ripoff_window = tk.Toplevel(self.root)
        ripoff_window.title(f"{self.page_names.get(self.page_number)} - {self.page_number}")

        # Sets the size of the new window
        ripoff_window.geometry("300x400")
        ripoff_window.resizable(False, False)

        # Creates a Text widget for writing in the new window
        ripoff_text_area = tk.Text(ripoff_window, wrap=tk.WORD, height=15, width=30)
        ripoff_text_area.pack(padx=10, pady=10)

        # Inserts the content of the current page into the ripoff window
        ripoff_text_area.insert(tk.END, self.text_area.get(1.0, tk.END).strip())

        # To make the new window movable
        ripoff_window.is_moving = False
        ripoff_window.offset_x = 0
        ripoff_window.offset_y = 0

        def start_move_ripoff(event):
            #Initiates dragging for the ripoff window
            ripoff_window.is_moving = True
            ripoff_window.offset_x = event.x
            ripoff_window.offset_y = event.y

        def do_move_ripoff(event):
            # Move the ripoff window while dragging
            if ripoff_window.is_moving:
                delta_x = event.x - ripoff_window.offset_x
                delta_y = event.y - ripoff_window.offset_y
                ripoff_window.geometry(f'+{ripoff_window.winfo_x() + delta_x}+{ripoff_window.winfo_y() + delta_y}')

        def stop_move_ripoff(event):
            # Stop dragging
            ripoff_window.is_moving = False

        # Binds mouse events to the ripoff window to make it draggable
        ripoff_window.bind("<Button-1>", start_move_ripoff)
        ripoff_window.bind("<B1-Motion>", do_move_ripoff)
        ripoff_window.bind("<ButtonRelease-1>", stop_move_ripoff)

    def rename_page(self):
        # Prompts the user to rename the current page
        new_name = simpledialog.askstring("Rename Page", f"Enter a new name for {self.page_names.get(self.page_number, 'Page')}:")

        if new_name:
            self.page_names[self.page_number] = new_name
            self.root.title(f"Sticky Note - {new_name}")

    def update_page_color(self):
        # Updates the background color of the current page
        color = self.root.cget('background')  # Get current window color
        self.text_area.configure(bg=color)

if __name__ == "__main__":
    root = tk.Tk()
    app = StickyNoteApp(root)
    root.mainloop()
