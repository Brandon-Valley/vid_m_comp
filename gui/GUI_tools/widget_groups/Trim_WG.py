from tkinter.ttk import *
from tkinter import *

from gui.GUI_tools import GUI_tools_utils





class Trim_WG():
    def __init__(self, 
                 master, 
                 max,
                 min,
                 min_diff,
                 display_type,
                 set_var):
        
        test_var = StringVar()
        self.txt_box = Entry(master, textvariable = test_var)#,width=TEXT_OVERLAY_TEXT_BOX_WIDTH) #````````````````````````````````````````````````````

        
        
        which_scale_moving = StringVar()
        
        def prevent_overlap_and_update_lbls(event=None):
            def _trying_to_overlap():
                return self.end_scale.get() < self.start_scale.get() + min_diff or self.start_scale.get() > self.end_scale.get() - min_diff
                
                
            if _trying_to_overlap():
                if   which_scale_moving.get() == 'start_scale':
                    self.start_scale.set(self.end_scale.get() - min_diff)
                elif which_scale_moving.get() == 'end_scale':
                    self.end_scale.set(self.start_scale.get() + min_diff)
                    
            start_scale_time_str.set(GUI_tools_utils.sec_to_min_str(start_val.get()))
            end_scale_time_str.set(GUI_tools_utils.sec_to_min_str(end_val.get()))
            diff_time_str.set(GUI_tools_utils.sec_to_min_str(end_val.get() - start_val.get()))
    
        
        start_val = IntVar(value = min)  # IntVars to hold
        end_val   = IntVar(value = max)  # values of scales
        self.start_scale  = Scale(master, from_=0, to=max, orient = "horizontal", showvalue=0, command=prevent_overlap_and_update_lbls)
        self.end_scale    = Scale(master, from_=0, to=max, orient = "horizontal", showvalue=0, command=prevent_overlap_and_update_lbls)
        set_var(self.start_scale, start_val)
        set_var(self.end_scale  , end_val)
#         self.start_scale.set(min)
#         self.end_scale  .set(max)
        
        start_scale_time_str = StringVar()
        end_scale_time_str = StringVar()
        diff_time_str = StringVar()
        
#         print('self.start_scale.get(): ', self.start_scale.get())#`````````````````````````````````````````````````````````
#         print('self.start_scale["variable"]: ', self.start_scale["variable"], type(self.start_scale["variable"]))#```````````````````````````````````````````````
#     
        
        start_scale_time_str.set(GUI_tools_utils.sec_to_min_str(start_val.get()))
        end_scale_time_str.set(GUI_tools_utils.sec_to_min_str(end_val.get()))

        diff_time_str.set(GUI_tools_utils.sec_to_min_str(end_val.get() - start_val.get()))
        
        self.start_lbl = Label(master, textvariable=start_scale_time_str)   # labels that will update
        self.end_lbl   = Label(master, textvariable=end_scale_time_str) # with IntVars as start_scale moves
        self.diff_lbl  = Label(master, textvariable=diff_time_str) # with IntVars as start_scale moves
    
        
        def start_scale_clk(event):
            which_scale_moving.set('start_scale')
            
        def end_scale_clk(event):
            which_scale_moving.set('end_scale')
        
        # bind to mouse clk
        self.start_scale.bind("<Button-1>",start_scale_clk)
        self.end_scale.bind("<Button-1>",end_scale_clk)
    
    
    
    def disable_all(self):
        self.start_scale.config(state = 'disabled')
        self.end_scale.config  (state = 'disabled')

    def enable_all(self):
        self.start_scale.config(state = 'normal')
        self.end_scale.config  (state = 'normal')
    
if __name__ == '__main__':
    import os
    sys.path.insert(1, os.path.join(sys.path[0], '..\\..')) # to import from parent dir
    #from parent dir
    import GUI
    GUI.main()
    
    
    