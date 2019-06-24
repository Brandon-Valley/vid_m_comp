from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import *

from tkinter import *

#import build_image
#import GUI_utils
import GUI
import Tab
import GUI_commands


#import pool_clips_data_handler

#import Advanced_Tab


TEXT_OVERLAY_TEXT_BOX_WIDTH = 80

class Upload_Tab(Tab.Tab):
    def __init__(self, master, tab_control):
        self.tab_control = tab_control
    
        Tab.Tab.__init__(self, master)
        
        

#         self.gui_vars       = GUI_commands.get_gui_vars()
        
        self.input_data_____widget_setup()

        
        self.grid_widgets()
        
    def input_data_____widget_setup(self):
        self.input_lbl_frm = LabelFrame(self.master, text=" Input Data: ")
        
        self.vid_path_txt_box_lbl       = Label(self.input_lbl_frm, text="Video Path: ")
        self.thumbnail_path_txt_box_lbl = Label(self.input_lbl_frm, text="Bottom Text: ")
                  
        self.vid_path_txt_box = Entry(self.input_lbl_frm)#,width=TEXT_OVERLAY_TEXT_BOX_WIDTH)
        self.vid_path_txt_box.insert(END, 'testtesttest') #default
         
        self.thumbnail_path_txt_box = Entry(self.input_lbl_frm)#,width=TEXT_OVERLAY_TEXT_BOX_WIDTH)
        self.thumbnail_path_txt_box.insert(END, 'teeeeeeeeeeest') #default
         
    def grid_widgets(self):
#         self.master.grid_columnconfigure(3, weight=1)
        
    
        self.input_lbl_frm              .grid(column=1, row=1, sticky='NSEW', rowspan = 300, padx=5, pady=5, ipadx=5, ipady=5)
        self.vid_path_txt_box_lbl       .grid(column=1, row=1)
        self.vid_path_txt_box           .grid(column=2, row=1)
        self.thumbnail_path_txt_box_lbl .grid(column=1, row=2)
        self.thumbnail_path_txt_box     .grid(column=2, row=2)

        
        
        
        
if __name__ == '__main__':
    GUI.main()