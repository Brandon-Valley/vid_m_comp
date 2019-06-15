import tkinter
import tkinter.ttk as ttk
import threading

def mainProgram(): # secure the main program initialization in its own def
    root = tkinter.Tk()
    frame = ttk.Frame()
    # You need to use indeterminate mode to achieve this
    pb = ttk.Progressbar(frame, length=300, mode='indeterminate')
    frame.pack()
    pb.pack()

    # Create a thread for monitoring loading bar
    # Note the passing of the loading bar as an argument
    barThread = threading.Thread(target=keepLooping, args=(pb,))
    # set thread as daemon (thread will die if parent is killed)
    barThread.daemon=True
    # Start thread, could also use root.after(50, barThread.start()) if desired
    barThread.start()

    pb.start(25)
    root.mainloop()

def keepLooping(bar):
    LOOPS = 0

    # Runs thread continuously (till parent dies due to daemon or is killed manually)
    while 1:
        """
        Here's the tricky part.
        The loading bar's position (for any length) is between 0 and 100.
        Its position is calculated as position = value % 100.    
        Resetting bar['value'] to 0 causes it to return to position 0,
        but naturally the bar would keep incrementing forever till it dies.
        It works, but is a bit unnatural.
        """
        if bar['value']==100:
            LOOPS += 1
            if LOOPS < 3:
                bar.config(value=0) # could also set it as bar['value']=0    

if __name__=='__main__':
    mainProgram()    
