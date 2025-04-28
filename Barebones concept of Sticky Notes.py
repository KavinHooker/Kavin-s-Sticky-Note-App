
import tkinter as tk
from tkinter import messagebox

class StickyNoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sticky Note")
        
        # Track the page number
        self.page_number = 1
        self.pages = {}

        # Set the size of the sticky note window
        self.root.geometry("400x400")
        self.root.resizable(False, False)
        
        # To make the window movable
        self.is_moving = False
        self.offset_x = 0
        self.offset_y = 0
        
        # Create a Text widget for writing
        self.text_area = tk.Text(self.root, wrap=tk.WORD, height=15, width=30)
        self.text_area.pack(padx=10, pady=10)
        
        # Create buttons
        self.toggle_button = tk.Button(self.root, text="Toggle Dark Mode", command=self.toggle_dark_mode)
        self.toggle_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.prev_button = tk.Button(self.root, text="Previous Page", command=self.previous_page)
        self.prev_button.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(self.root, text="Next Page", command=self.next_page)
        self.next_button.pack(side=tk.LEFT, padx=10)
        
        # Create a simple menu to store pages
        self.pages[self.page_number] = ""

        # Bind mouse events to make window movable
        self.root.bind("<Button-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.do_move)
        self.root.bind("<ButtonRelease-1>", self.stop_move)

    def start_move(self, event):
        #Initiate dragging
        self.is_moving = True
        self.offset_x = event.x
        self.offset_y = event.y

    def do_move(self, event):
        #Move window while dragging
        if self.is_moving:
            delta_x = event.x - self.offset_x
            delta_y = event.y - self.offset_y
            self.root.geometry(f'+{self.root.winfo_x() + delta_x}+{self.root.winfo_y() + delta_y}')

    def stop_move(self, event):
        #Stop dragging
        self.is_moving = False

    def toggle_dark_mode(self):
        #Toggle between dark and light mode
        current_bg = self.root.cget('background')
        if current_bg == 'black':
            self.root.configure(background='white')
            self.text_area.configure(bg='white', fg='black')
            self.toggle_button.configure(bg='light gray', fg='black')
            self.prev_button.configure(bg='light gray', fg='black')
            self.next_button.configure(bg='light gray', fg='black')
        else:
            self.root.configure(background='black')
            self.text_area.configure(bg='black', fg='white')
            self.toggle_button.configure(bg='dark gray', fg='white')
            self.prev_button.configure(bg='dark gray', fg='white')
            self.next_button.configure(bg='dark gray', fg='white')

    def previous_page(self):
        #Go to the previous page
        if self.page_number > 1:
            self.pages[self.page_number] = self.text_area.get(1.0, tk.END).strip()
            self.page_number -= 1
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, self.pages.get(self.page_number, ""))
        else:
            messagebox.showinfo("Info", "You're already on the first page.")

    def next_page(self):
        #Go to the next page
        self.pages[self.page_number] = self.text_area.get(1.0, tk.END).strip()
        self.page_number += 1
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, self.pages.get(self.page_number, ""))

if __name__ == "__main__":
    root = tk.Tk()
    app = StickyNoteApp(root)
    root.mainloop()
