from tkinter.ttk import *
from tkinter import *

import os

from GUI_tools import Tab

import GUI_commands

# import sys
# sys.path.insert(1, os.path.join(sys.path[0], '..')) # to import from parent dir
# from parent dir
import project_vars


PATH_TEXT_BOX_WIDTH  = 80
TITLE_TEXT_BOX_WIDTH = 40

class Upload_Tab(Tab.Tab):
    def __init__(self, master, tab_control):
        self.tab_control = tab_control
    
        Tab.Tab.__init__(self, master)


        self.gui_vars = GUI_commands.get_gui_vars()
        
        self.input_data_____widget_setup()
        self.upload_info_____widget_setup()
        self.snappa_____widget_setup()

        self.grid_widgets()
        
        
    def update_upload_ability(self, event=None):
        self.upload_btn.configure( state = 'normal' )

        if self.title_txt_box.get() == '' or \
           not os.path.exists(self.vid_path_txt_box.get()) or \
           not os.path.exists(self.thumbnail_path_txt_box.get()):
            self.upload_btn.configure( state = 'disabled' )



    def thumbnail_path_txt_box_edit(self, event = None):
        GUI_commands.log_gui_var('thumbnail_path', self.thumbnail_path_txt_box.get())
        self.update_upload_ability()
        self.tabs['compile'].update_compile_upload_log_btn_state()
        GUI_commands.update_thumbnail_canvas(self.thumbnail_path_txt_box.get(), self.thumnail_canvas)


        
    def input_data_____widget_setup(self):
        self.input_lbl_frm = LabelFrame(self.master, text=" Input Data: ")
        
        # vid path
        self.vid_path_txt_box_lbl = Label(self.input_lbl_frm, text="Video Path: ")
                  
        def vid_path_txt_box_edit(event = None):
            GUI_commands.log_gui_var('compiled_output_file_path', self.vid_path_txt_box.get())
            self.update_upload_ability()
                
            
        self.vid_path_txt_box = Entry(self.input_lbl_frm,width=PATH_TEXT_BOX_WIDTH)
        self.vid_path_txt_box.insert(END, self.gui_vars["compiled_output_file_path"]) #default
        self.vid_path_txt_box.bind('<Expose>', xview_event_handler)#scrolls text to end if needed
        self.bind_to_edit(self.vid_path_txt_box, vid_path_txt_box_edit)
        
        def update_func(event = None):
            print('in upload tab, updated')
            self.vid_path_txt_box.xview_moveto(1)        
        def update_func_2(event = None):
            print('in upload tab, updated 2')
            self.vid_path_txt_box.xview_moveto(1)
            

        
        
        def vid_path_browse_btn_clk():
            self.path_tb_browse_btn_clk(self.vid_path_txt_box, 'file', '.mp4')
            vid_path_txt_box_edit()
            
        self.vid_path_browse_btn = Button(self.input_lbl_frm, text="Browse...", command = vid_path_browse_btn_clk)

        
        
        
        # thumbnail path
        self.thumbnail_path_txt_box_lbl = Label(self.input_lbl_frm, text="Thumbnail Path: ")

         
        self.thumbnail_path_txt_box = Entry(self.input_lbl_frm,width=PATH_TEXT_BOX_WIDTH)
        self.thumbnail_path_txt_box.insert(END, self.gui_vars['thumbnail_path']) #default
        self.thumbnail_path_txt_box.bind('<Expose>', xview_event_handler)#scrolls text to end if needed
        self.bind_to_edit(self.thumbnail_path_txt_box, self.thumbnail_path_txt_box_edit)
                
        def thumbnail_path_browse_btn_clk():
            self.path_tb_browse_btn_clk(self.thumbnail_path_txt_box, 'file')
            self.thumbnail_path_txt_box_edit()
            
        self.thumbnail_path_browse_btn = Button(self.input_lbl_frm, text="Browse...", command = thumbnail_path_browse_btn_clk)



    def upload_info_____widget_setup(self):
        self.upload_info_lbl_frm = LabelFrame(self.master, text=" Upload Information: ")
        
        # title    
        def title_txt_box_edit(event=None):
            self.update_upload_ability()
            self.tabs['compile'].update_compile_upload_log_btn_state()

        self.title_txt_box_lbl = Label(self.upload_info_lbl_frm, text="Video Title: ")
        self.title_txt_box = Entry(self.upload_info_lbl_frm,width=TITLE_TEXT_BOX_WIDTH)
        self.bind_to_edit(self.title_txt_box, title_txt_box_edit)

        # description
        self.descrip_txt_box_lbl = Label(self.upload_info_lbl_frm, text="Video Description: ")
        self.descrip_txt_box = Entry(self.upload_info_lbl_frm,width=TITLE_TEXT_BOX_WIDTH)
        self.descrip_txt_box.insert(END, self.gui_vars['description']) #default
        def log_description(event=None): GUI_commands.log_gui_var('description', self.descrip_txt_box.get())
        self.bind_to_edit(self.descrip_txt_box, log_description)

        # tags
        self.tags_txt_box_lbl = Label(self.upload_info_lbl_frm, text="Video Tags: ")
        self.tags_txt_box = Entry(self.upload_info_lbl_frm,width=TITLE_TEXT_BOX_WIDTH)
        self.tags_txt_box.insert(END, self.gui_vars['tags']) #default
        def log_tags(event=None): GUI_commands.log_gui_var('tags', self.tags_txt_box.get())
        self.bind_to_edit(self.tags_txt_box, log_tags)
        
        # Category
        self.category_cbox_lbl = Label(self.upload_info_lbl_frm, text="Category: ")
        self.category_cbox = Combobox(self.upload_info_lbl_frm, state = 'readonly')
        self.category_cbox['values'] = ['Comedy']
        self.category_cbox.current(0) #set the selected item
        
        # Privacy
        self.privacy_cbox_lbl = Label(self.upload_info_lbl_frm, text="Privacy Status: ")
        self.privacy_cbox = Combobox(self.upload_info_lbl_frm, state = 'readonly')
        self.privacy_cbox['values'] = ['public', 'private']
        self.privacy_cbox.current(0) #set the selected item
        
        # upload btn
        self.upload_btn = Button(self.upload_info_lbl_frm, text="Upload", command = lambda: GUI_commands.upload(self.vid_path_txt_box.get(), self.title_txt_box.get(), self.descrip_txt_box.get(), self.tags_txt_box.get(), self.privacy_cbox.get(), self.thumbnail_path_txt_box.get()))
        self.update_upload_ability()

        # thumbnail canvas
        self.thumnail_canvas = Canvas(self.upload_info_lbl_frm)#, width = w, height = h)
        GUI_commands.update_thumbnail_canvas(self.thumbnail_path_txt_box.get(), self.thumnail_canvas)





    def snappa_____widget_setup(self):
        self.snappa_lbl_frm = LabelFrame(self.master, text=" Snappa: ")
        
        self.open_snappa_btn = Button(self.snappa_lbl_frm, text="Open Snappa In Chrome", command = GUI_commands.open_snappa_in_chrome)
        
        # load snappa download as thumbnail btn
        def load_snappa_dl_as_thumb_btn_clk(event=None):
            GUI_commands.load_snappa_dl_as_thumbnail(project_vars.THUMBNAIL_PATH_INTENDED)
            self.thumbnail_path_txt_box.delete(0, "end")
            self.thumbnail_path_txt_box.insert(END, project_vars.THUMBNAIL_PATH_INTENDED)
            self.thumbnail_path_txt_box_edit()
            
#         self.load_snappa_dl_as_thumb_btn = Button(self.snappa_lbl_frm, text="Load Snappa Download\n as thumbnail", command = lambda: GUI_commands.load_snappa_dl_as_thumbnail(self.thumbnail_path_txt_box.get()))
        self.load_snappa_dl_as_thumb_btn = Button(self.snappa_lbl_frm, text="Load Snappa Download\n as thumbnail", command = load_snappa_dl_as_thumb_btn_clk)







        
    def grid_widgets(self):
#         self.master.grid_columnconfigure(3, weight=1)
        

        
        # input Information
        self.input_lbl_frm              .grid(column=1, row=1, sticky='', padx=5, pady=5, ipadx=5, ipady=5)
        self.vid_path_txt_box_lbl       .grid(column=1, row=1)
        self.vid_path_txt_box           .grid(column=2, row=1)
        self.vid_path_browse_btn        .grid(column=3, row=1, padx=5)
        self.thumbnail_path_txt_box_lbl .grid(column=1, row=2)
        self.thumbnail_path_txt_box     .grid(column=2, row=2)
        self.thumbnail_path_browse_btn  .grid(column=3, row=2, padx=5)

        # Upload Information
        self.upload_info_lbl_frm        .grid(column=1, row=2, sticky='NSW', padx=5, pady=5, ipadx=5, ipady=5)
        self.title_txt_box_lbl          .grid(column=1, row=1)
        self.title_txt_box              .grid(column=2, row=1)
        self.descrip_txt_box_lbl        .grid(column=1, row=2)
        self.descrip_txt_box            .grid(column=2, row=2)
        self.tags_txt_box_lbl           .grid(column=1, row=3)
        self.tags_txt_box               .grid(column=2, row=3)
        self.category_cbox_lbl          .grid(column=1, row=4)
        self.category_cbox              .grid(column=2, row=4, sticky = "W")
        self.privacy_cbox_lbl           .grid(column=1, row=5)
        self.privacy_cbox               .grid(column=2, row=5, sticky = "W")
        self.upload_btn                 .grid(column=1, row=6)
        self.thumnail_canvas            .grid(column=3, row=1, rowspan = 6, padx=5)
        
         # snappa
        self.snappa_lbl_frm             .grid(column=2, row=1, sticky='NW', rowspan = 2, padx=5, pady=5, ipadx=5, ipady=5)
        self.open_snappa_btn            .grid(column=1, row=1, padx=5, pady=5)
        self.load_snappa_dl_as_thumb_btn.grid(column=1, row=2, padx=5, pady=5)
        
def xview_event_handler(e):
    e.widget.update_idletasks()
    e.widget.xview_moveto(1)
    e.widget.unbind('<Expose>')
        
if __name__ == '__main__':
    import GUI
    GUI.main()