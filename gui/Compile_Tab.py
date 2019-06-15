from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
# from tkinter.colorchooser import *
from tkinter import filedialog

from tkinter import *

#import build_image
#import GUI_utils
import GUI
import Tab
import GUI_commands
# import project_vars_handler
#import pool_clips_data_handler

# import Advanced_Tab






OUTPUT_PATH_TEXT_BOX_WIDTH = 80
CLIP_SORT_METHODS_LIST = ['balanced_with_padding', 'random'] # the first in the list will be set by default

# DEFAULT_OUTPUT_PATH = project_vars_handler.get_var('current_data_dir_path') + '/compile_from_gui_output.mp4'

class Compile_Tab(Tab.Tab):
    def __init__(self, master, tab_control):
        self.tab_control = tab_control
    
        Tab.Tab.__init__(self, master)
        
#         self.clip_data      = GUI_commands.get_current_clip_data()
#         self.clip_pool_data = GUI_commands.get_clip_pool_data()
        self.gui_vars       = GUI_commands.get_gui_vars()
        
        self.clip_sort_____widget_setup()
        self.progress_____widget_setup()
        self.compile_____widget_setup()
        
        
        

        
        self.grid_widgets()
        
        
        
    def clip_sort_____widget_setup(self):
        # clip sort combobox
        self.clip_sort_cbox_lbl = Label(self.master, text="Clip Sort Method:")
        self.clip_sort_cbox = Combobox(self.master, state = 'readonly')
        self.clip_sort_cbox['values'] = CLIP_SORT_METHODS_LIST
        default_font_index = self.clip_sort_cbox['values'].index(CLIP_SORT_METHODS_LIST[0]) #default
        self.clip_sort_cbox.current(default_font_index) #set the selected item
        
        
    def progress_____widget_setup(self):
        self.prog_lbl_frm = LabelFrame(self.master, text=" Compile Progress: ")
        self.resize_pb_lbl = Label(self.prog_lbl_frm, text="Resize: ")
        self.resize_pb = Progressbar(self.prog_lbl_frm, length=300, mode='indeterminate')
        
        # dict of widgets that will be interacted with after compile btn pressed
        self.prog_widget_d = {'lbl_frm'   : self.prog_lbl_frm,
                              'resize_pb' : self.resize_pb}

        
        
    def compile_____widget_setup(self):
        self.compile_btn = Button(self.master, text="Compile Clips", command = lambda: GUI_commands.compile(self.output_path_txt_box.get(), self.play_output_btn, self.clip_sort_cbox.get(), self.prog_widget_d))
        
        self.output_path_txt_box_lbl = Label(self.master, text="Output Path: ")
                 
                 
        def output_path_text_box_updated(event = None):
            GUI_commands.log_gui_var('compiled_output_file_path', self.output_path_txt_box.get())
            
                 
        self.output_path_txt_box = Entry(self.master,width=OUTPUT_PATH_TEXT_BOX_WIDTH)
        self.output_path_txt_box.insert(END, self.gui_vars["compiled_output_file_path"]) #default
        self.output_path_txt_box.bind('<Expose>', xview_event_handler)#scrolls text to end if needed
        self.output_path_txt_box.bind("<FocusOut>", xview_event_handler)#scrolls text to end if needed when leave txt box focus
        self.bind_to_edit(self.output_path_txt_box, output_path_text_box_updated)
        
        
        def output_path_browse_btn_clk():
            #get file path and place it in text box
            dir = filedialog.askdirectory()
            self.output_path_txt_box.delete(0, "end")
            self.output_path_txt_box.insert(END, dir)
            
            output_path_text_box_updated()
            
        self.output_path_browse_btn = Button(self.master, text="Browse...", command = output_path_browse_btn_clk)
        self.play_output_btn = Button(self.master, text="Play Output", command = lambda: GUI_commands.play_output(self.output_path_txt_box.get()))

        






    def grid_widgets(self):
        blank_lbl_1 = Label(self.master, text="") #for spacing 
                                                                              
        row_num = 10
        
        # clip info
        self.compile_btn                .grid(column=1, row=row_num, sticky = 'e')
        self.output_path_txt_box_lbl    .grid(column=1, row=row_num + 1, sticky = 'e')
        self.output_path_txt_box        .grid(column=2, row=row_num + 1, sticky = 'e')
        self.output_path_browse_btn     .grid(column=3, row=row_num + 1)
        self.play_output_btn            .grid(column=1, row=row_num + 2)
        
        row_num += 10
        
        # configuration options
        self.clip_sort_cbox_lbl         .grid(column=1, row=row_num)
        self.clip_sort_cbox             .grid(column=1, row=row_num + 1)
        
        
        row_num += 10
        
        # compile progress (all inside lable frame wich is grid on btn clk
        self.resize_pb_lbl              .grid(column=1, row=row_num)
        
        
        

def xview_event_handler(e):
    e.widget.update_idletasks()
    e.widget.xview_moveto(1)
    e.widget.unbind('<Expose>')
        
        
        
if __name__ == '__main__':
    GUI.main()