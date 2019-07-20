
    
    
    
# import tkinter as 
from tkinter import *

VID_DURATION = 45
MIN_DIFF = 5

# self.duration: 72 --> '1:12'
def sec_to_min_str(total_sec):
    minutes = int(total_sec / 60)
    seconds = int(total_sec % 60)
    sec_str = str(seconds)
    if len(sec_str) < 2:
        sec_str = '0' + sec_str
    return str(minutes) + ':' + sec_str


def main():
    root = Tk()

    which_scale_moving = StringVar()
    
    def prevent_overlap_and_update_lbls(event=None):
        def _trying_to_overlap():
            return ts.get() < bs.get() + MIN_DIFF or bs.get() > ts.get() - MIN_DIFF
            
        print('which_scale_moving: ', which_scale_moving.get())
            
        if _trying_to_overlap():
            print('trying to overlap!')
            if   which_scale_moving.get() == 'ts':
                ts.set(bs.get() + MIN_DIFF)
            elif which_scale_moving.get() == 'bs':
                bs.set(ts.get() - MIN_DIFF)
                
        ts_time_str.set(sec_to_min_str(leftValue.get()))
        bs_time_str.set(sec_to_min_str(rightValue.get()))
        diff_time_str.set(sec_to_min_str(leftValue.get() - rightValue.get()))

    
    leftValue = IntVar()  # IntVars to hold
    rightValue = IntVar() # values of scales
    
    
    
    
    ts  = Scale(root, from_=0, to=VID_DURATION, orient = "horizontal", command=prevent_overlap_and_update_lbls, showvalue=0, label="VVV", variable=leftValue)
    ts.set(VID_DURATION)
    bs = Scale(root, from_=0, to=VID_DURATION, orient = "horizontal", command=prevent_overlap_and_update_lbls, showvalue=0, variable=rightValue)

    ts_time_str = StringVar()
    bs_time_str = StringVar()
    diff_time_str = StringVar()
    print('sec_to_min_str(leftValue.get()): ', sec_to_min_str(leftValue.get()))
    ts_time_str.set(sec_to_min_str(leftValue.get()))
    bs_time_str.set(sec_to_min_str(rightValue.get()))
    diff_time_str.set(sec_to_min_str(leftValue.get() - rightValue.get()))
    
    
    leftLabel = Label(root, textvariable=ts_time_str)   # labels that will update
    rightLabel = Label(root, textvariable=bs_time_str) # with IntVars as ts moves
    diff_lbl = Label(root, textvariable=diff_time_str) # with IntVars as ts moves

    # ts.config(state = 'disabled')
    # bs.config(state = 'disabled')
    
    def ts_clk(event):
        which_scale_moving.set('ts')
        
 
    def bs_clk(event):
        which_scale_moving.set('bs')
    
    
    ts.bind("<Button-1>",ts_clk)
    bs.bind("<Button-1>",bs_clk)
    
    ts.pack()
    bs.pack()
    rightLabel.pack()
    leftLabel.pack()
    diff_lbl.pack()
    
    
    root.mainloop()  
if __name__ == '__main__':
    main()   
