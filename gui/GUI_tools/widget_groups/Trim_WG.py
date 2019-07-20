from tkinter.ttk import *
from tkinter import *

from gui.GUI_tools import GUI_tools_utils





class Trim_WG():
    def __init__(self, 
                 master, 
                 range,
                 min_diff,
                 type):
        
        
        which_scale_moving = StringVar()
        
        def prevent_overlap_and_update_lbls(event=None):
            def _trying_to_overlap():
                return self.start_scale.get() < self.end_scale.get() + min_diff or self.end_scale.get() > self.start_scale.get() - min_diff
                
            print('which_scale_moving: ', which_scale_moving.get())
                
            if _trying_to_overlap():
                print('trying to overlap!')
                if   which_scale_moving.get() == 'start_scale':
                    self.start_scale.set(self.end_scale.get() + min_diff)
                elif which_scale_moving.get() == 'end_scale':
                    self.end_scale.set(self.start_scale.get() - min_diff)
                    
            start_scale_time_str.set(GUI_tools_utils.sec_to_min_str(leftValue.get()))
            end_scale_time_str.set(GUI_tools_utils.sec_to_min_str(rightValue.get()))
            diff_time_str.set(GUI_tools_utils.sec_to_min_str(leftValue.get() - rightValue.get()))
    
        
        leftValue = IntVar()  # IntVars to hold
        rightValue = IntVar() # values of scales
        
        
        
        
        self.start_scale  = Scale(master, from_=0, to=range, orient = "horizontal", command=prevent_overlap_and_update_lbls, showvalue=0, label="VVV", variable=leftValue)
        self.start_scale.set(range)
        self.end_scale = Scale(master, from_=0, to=range, orient = "horizontal", command=prevent_overlap_and_update_lbls, showvalue=0, variable=rightValue)
    
        start_scale_time_str = StringVar()
        end_scale_time_str = StringVar()
        diff_time_str = StringVar()
        print('GUI_tools_utils.sec_to_min_str(leftValue.get()): ', GUI_tools_utils.sec_to_min_str(leftValue.get()))
        start_scale_time_str.set(GUI_tools_utils.sec_to_min_str(leftValue.get()))
        end_scale_time_str.set(GUI_tools_utils.sec_to_min_str(rightValue.get()))
        diff_time_str.set(GUI_tools_utils.sec_to_min_str(leftValue.get() - rightValue.get()))
        
        
        leftLabel = Label(master, textvariable=start_scale_time_str)   # labels that will update
        rightLabel = Label(master, textvariable=end_scale_time_str) # with IntVars as start_scale moves
        diff_lbl = Label(master, textvariable=diff_time_str) # with IntVars as start_scale moves
    
        # start_scale.config(state = 'disabled')
        # end_scale.config(state = 'disabled')
        
        def start_scale_clk(event):
            which_scale_moving.set('start_scale')
            
     
        def end_scale_clk(event):
            which_scale_moving.set('end_scale')
        
        
        self.start_scale.bind("<Button-1>",start_scale_clk)
        self.end_scale.bind("<Button-1>",end_scale_clk)
    
    
if __name__ == '__main__':
    import os
    sys.path.insert(1, os.path.join(sys.path[0], '..\\..')) # to import from parent dir
    #from parent dir
    import GUI
    GUI.main()
    
    
    