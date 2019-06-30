from tkinter import *
from tkinter.ttk import *
import time
import threading

class Interface:
    def __init__(self, master):
        self.master = master
        self.browse_button= Button (master, text="Browse", command=self.browser)
        self.browse_button.pack()
        self.progressbar = Progressbar(mode="determinate", maximum=75)

    def browser (self):
        t = threading.Thread(target=self.read_file, args=("filename",))
        self.progressbar.pack()
        self.browse_button.config(state="disabled")
        self.master.config(cursor="wait")
        self.master.update()

        t.start()
        while t.is_alive():
            self.progressbar.step(1)
            self.master.update_idletasks()  # or try self.master.update()
            t.join(0.1)

        self.progressbar.config(value="0")
        self.progressbar.pack_forget()
        self.browse_button.config(state="enabled")
        self.master.config(cursor="")

    def read_file (self, filename):
        time.sleep(7)  # actually do the read here

window = Tk()
starter = Interface(window)
window.mainloop()