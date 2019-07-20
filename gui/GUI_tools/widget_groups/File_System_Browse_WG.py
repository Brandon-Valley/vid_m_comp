from tkinter.ttk import *
from tkinter import *




class File_System_Browse_WG():
    def __init__(self, 
                 master,
                 lbl_txt, 
                 tb_width = None, 
                 browse_for = 'dir',  # 'dir' or 'file'
                 file_type = None,    # '.jpg', '.mp4', ect...
                 init_path = None, 
                 focus_tb_after_browse = False,
                 tb_edit_func = None,
                 browse_btn_txt = 'Browse...'):
        self.lbl = Label(master, text = lbl_txt)
        
        # text box
        self.tb = Entry(master, width=tb_width)
#         print('in file_system sihfog, init_path: ', init_path)#`````````````````````````````````````````````````
        
        if init_path != None:
            self.tb.insert(END, init_path) #default
            
#         Tab.bind_to_update(self.tb, xview_event_handler)
            
        self.tb.bind('<Expose>', xview_event_handler)#scrolls text to end if needed
        self.tb.bind('<Enter>' , xview_event_handler)#scrolls text to end if needed
        self.tb.bind('<Leave>' , xview_event_handler)#scrolls text to end if needed
        self.tb.bind('<FocusIn>' , xview_event_handler)#scrolls text to end if needed
        
        if tb_edit_func != None:
            self.bind_to_edit(self.tb, tb_edit_func)

        # browse btn
        def browse_btn_clk():
            self.path_tb_browse_btn_clk(self.tb, browse_for, file_type)
            if tb_edit_func != None:
                tb_edit_func()
            
            if focus_tb_after_browse == True:
                self.tb.focus()
            
        self.btn = Button(master, text=browse_btn_txt, command = browse_btn_clk)        
        
        
    # should not be used outside this file
    def path_tb_browse_btn_clk(self, path_txt_box_widget, browse_for, file_type = None):
        #get file path and place it in text box
        
        if browse_for == 'file':
            if file_type == None:
                file_system_item = filedialog.askopenfilename()

            else:
                file_system_item = filedialog.askopenfilename(filetypes = (("Images", "*" + file_type), ("All files", "*")))#filetypes = (("Images", '*.png|*.jpg'), ("All files", "*")))#"*" + file_types   #,("Template files", '*.jpg'), 
        elif browse_for == 'dir':
            file_system_item = filedialog.askdirectory()
        else:
            raise Exception('ERROR:  In Tab.py, in path_tb_browse_btn_clk, invalid value for browse_for: ', browse_for)
        
        if len(file_system_item) != 0: # so if you X out of browse, you dont lose the path you started with
            path_txt_box_widget.delete(0, "end")
            path_txt_box_widget.insert(END, file_system_item)
        
        
        
        
        
        
def xview_event_handler(e):
    e.widget.update_idletasks()
    e.widget.xview_moveto(1)
    e.widget.unbind('<Expose>')
    
    
if __name__ == '__main__':
    import os
    sys.path.insert(1, os.path.join(sys.path[0], '..')) # to import from parent dir
    #from parent dir
    import GUI
    GUI.main()
    
    
    