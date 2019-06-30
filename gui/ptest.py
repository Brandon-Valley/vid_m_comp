from tkinter import *
from tkinter.ttk import *
import time
import threading

class Interface:
    def __init__(self, master):
        self.master = master
        self.browse_button= Button (master, text="Browse", command=self.browser)
        self.browse_button.pack()
        self.progressbar = Progressbar(mode="indeterminate", maximum=75)

    def browser (self):
        t = threading.Thread(target=self.read_file, args=("filename",))
        self.progressbar.pack()
        self.browse_button.config(state="disabled")
        self.master.config(cursor="wait")
        self.master.update()
        pbar_init = False
        
        
        t.start()
        while t.is_alive():
            if pbar_init == False:
                self.progressbar.start(10)
                pbar_init = True
#             self.progressbar.step(1)
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