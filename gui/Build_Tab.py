from tkinter.ttk import *
from tkinter import *

import os

from GUI_tools import Tab

import GUI_commands
import project_vars




MIN_TRIM_DIFF = 1 # min # seconds you can trim a clip to

TEXT_OVERLAY_TEXT_BOX_WIDTH = 80

class Build_Tab(Tab.Tab):
    def __init__(self, master, tab_control):
        self.tab_control = tab_control
        Tab.Tab.__init__(self, master)
        
        if os.path.exists(project_vars.CURRENT_DATA_DIR_PATH):
            GUI_commands.init_current_if_needed()
            
            self.clip_data      = GUI_commands.get_current_clip_data()
            self.clip_pool_data = GUI_commands.get_clip_pool_data()
            self.gui_vars       = GUI_commands.get_gui_vars()
            
            self.clip_info_____widget_setup()
            self.text_overlay_____widget_setup()
            self.trim_clip_____widget_setup()
            self.accept_decline_____widget_setup()
            self.rating_____widget_setup()
            self.navigation_____widget_setup() #next and back buttons
            self.prune_clips_____widget_setup()
            self.progess_____widget_setup()
            self.rating_info_____widget_setup()
    
            
            self.grid_widgets()
		
        

    def clip_info_____widget_setup(self): 
        self.clip_info_lbl_frm = LabelFrame(self.master, text=" Clip Information: ")
        self.title_lbl_lbl = Label(self.clip_info_lbl_frm, text="Title: ")
        self.title_lbl     = Label(self.clip_info_lbl_frm, text=self.clip_data.title)
        
        self.duration_lbl_lbl = Label(self.clip_info_lbl_frm, text="Duration: ")
        self.duration_lbl     = Label(self.clip_info_lbl_frm, text=self.clip_data.duration_str)
     

    def text_overlay_____widget_setup(self):
        self.txt_overlay_lbl_frm   = LabelFrame(self.master, text=" Text Overlay: ")
    
        # top and bottom text overlay text boxes
        #self.l_path = StringVar()
        self.top_txt_lbl    = Label(self.txt_overlay_lbl_frm, text="Top Text: ")
        self.bottom_txt_lbl = Label(self.txt_overlay_lbl_frm, text="Bottom Text: ")
                 
        self.top_txt_txt_box = Entry(self.txt_overlay_lbl_frm)#,width=TEXT_OVERLAY_TEXT_BOX_WIDTH)
        self.top_txt_txt_box.insert(END, self.clip_data.top_txt) #default
        
        self.bottom_txt_txt_box = Entry(self.txt_overlay_lbl_frm)#,width=TEXT_OVERLAY_TEXT_BOX_WIDTH)
        self.bottom_txt_txt_box.insert(END, self.clip_data.bottom_txt) #default
        
        
        self.apply_txt_overlay_btn = Button(self.txt_overlay_lbl_frm, text="Apply Text Overlay", command = lambda: GUI_commands.apply_txt_overlay(self.top_txt_txt_box.get(), self.bottom_txt_txt_box.get(),self.master, self.tab_control, self.skip_evaluated_cbtn_sel.get(), self.skip_to_prority_cbtn_sel.get()))

        
        # log top and bottom text text boxes each time you edit them
        def log_top_txt_box(event):
            GUI_commands.log('top_text', self.top_txt_txt_box.get())
            self.clip_data = GUI_commands.get_current_clip_data()
        def log_bottom_txt_box(event):
            GUI_commands.log('bottom_text', self.bottom_txt_txt_box.get())
            self.clip_data = GUI_commands.get_current_clip_data()
        self.bind_to_edit(self.top_txt_txt_box, log_top_txt_box)
        self.bind_to_edit(self.bottom_txt_txt_box, log_bottom_txt_box)

        
        def use_txt_overlay_cbtn_clk():
            # top and bottom text overlay text boxes and apply text overlay btn disable when use text overlay cbtn not checked
            def update_txt_overlay_txt_widgets():
                self.top_txt_txt_box.configure( state = 'normal' )
                self.top_txt_txt_box.delete(0, "end")
                self.top_txt_txt_box.insert(END, self.clip_data.top_txt)
                self.bottom_txt_txt_box.configure( state = 'normal' )
                self.bottom_txt_txt_box.delete(0, "end")
                self.bottom_txt_txt_box.insert(END, self.clip_data.bottom_txt)
                
                self.apply_txt_overlay_btn.configure( state = 'normal' )
                
                if self.use_txt_overlay_cbtn_sel.get() == 0:
                    #self.top_txt_txt_box.insert(END, self.clip_data.top_txt)
                    self.top_txt_txt_box.configure( state = 'disabled' ) 
                    #self.bottom_txt_txt_box.insert(END, self.clip_data.bottom_txt)
                    self.bottom_txt_txt_box.configure( state = 'disabled' ) 
                    
                    self.apply_txt_overlay_btn.configure( state = 'disabled' )
                    
            #GUI_commands.log('top_text', self.top_txt_txt_box.get())
            #GUI_commands.log('bottom_text', self.bottom_txt_txt_box.get())        
            update_txt_overlay_txt_widgets()
            GUI_commands.log('use_text_overlay', self.use_txt_overlay_cbtn_sel.get())

            
            
        #use text overlay check button
        self.use_txt_overlay_cbtn_sel = IntVar(value = self.clip_data.use_txt_overlay)#value sets default
        self.use_txt_overlay_cbtn =   Checkbutton(self.txt_overlay_lbl_frm, text="Text Overlay", variable=self.use_txt_overlay_cbtn_sel, command = use_txt_overlay_cbtn_clk)
        use_txt_overlay_cbtn_clk() #disabled folder name by default if use_txt_overlay_cbtn is 0 by default

        
        
        
        
        
        
        
    
    
    
    
    def trim_clip_____widget_setup(self):
        self.trim_lbl_frm = LabelFrame(self.master, text=" Trip Clip: ")

#         # trim cbtn
#         def trim_cbtn_clk(event=None):
#             pass
# #             GUI_commands.log('use_trimmed_clip', self.trim_cbtn_sel.get())
# #              
# #             self.trim_wg.enable_all()
# #             self.auto_accept_trim_cbtn.config(state = 'normal')
# #             self.trim_clip_btn        .config(state = 'normal')
# #              
# #             if self.trim_cbtn_sel.get() == 0:
# #                 self.trim_wg.disable_all()
# #                 self.auto_accept_trim_cbtn.config(state = 'disabled')
# #                 self.trim_clip_btn        .config(state = 'disabled')
#                  
#          
#         self.trim_cbtn_sel = IntVar(value = self.clip_data.use_trimmed_clip)#value sets default     
#         self.trim_cbtn = Checkbutton(self.trim_lbl_frm, text="Trim Clip", variable=self.trim_cbtn_sel, command = trim_cbtn_clk)
        
        # auto accept cbtn
        self.auto_accept_trim_cbtn_sel = IntVar(value = self.gui_vars['auto_accept_trimmed_clip'])#value sets default     
        self.auto_accept_trim_cbtn = Checkbutton(self.trim_lbl_frm, text="Auto Accept")#, variable=self.auto_accept_trim_cbtn_sel)#, command = trim_cbtn_clk)
        self.set_var(self.auto_accept_trim_cbtn, self.auto_accept_trim_cbtn_sel)
        
        # trim clip btn
        self.trim_clip_btn = Button(self.trim_lbl_frm, text="Trim Clip And Re-Evaluate", command = lambda: GUI_commands.trim_clip(self.trim_wg.get(), self.auto_accept_trim_cbtn_sel.get(), self.master, self.tab_control, self.skip_evaluated_cbtn_sel.get(), self.skip_to_prority_cbtn_sel.get()))

        # trim widget group
        def trim_scales_update(event=None):
            GUI_commands.log('start_trim_time', self.trim_wg.start_scale.get())
            GUI_commands.log('end_trim_time'  , self.trim_wg.end_scale.get())
            
            # update clip data
            self.clip_data = GUI_commands.get_current_clip_data()

            if not self.clip_data.trim_times_diff_from_og():
                self.trim_clip_btn.config(state = 'disabled')
                GUI_commands.log('use_trimmed_clip', '')
            else:
                self.trim_clip_btn.config(state = 'normal')
                GUI_commands.log('use_trimmed_clip', 1)
                
#             print('in build_tab, ', )
            
        self.trim_wg = self.Trim_WG(self.trim_lbl_frm, max = self.clip_data.duration, min_diff = MIN_TRIM_DIFF,
                                    start_set = self.clip_data.start_trim_time,
                                    end_set   = self.clip_data.end_trim_time  , update_func=trim_scales_update) 
        
#         trim_cbtn_clk()
        trim_scales_update()
        
        # bind widgets to log
        self.bind_to_update(self.auto_accept_trim_cbtn, lambda: GUI_commands.log_gui_var('auto_accept_trimmed_clip', self.auto_accept_trim_cbtn_sel.get()))
#         self.bind_to_update(self.trim_wg.start_scale,   lambda: GUI_commands.log('start_trim_time', self.trim_wg.start_scale.get()))
#         self.bind_to_update(self.trim_wg.end_scale,     lambda: GUI_commands.log('end_trim_time'  , self.trim_wg.end_scale.get()))
        

        
    
    
    
    
    
    
    
    
    def accept_decline_____widget_setup(self):
        # accept and decline radio btns
        status  = StringVar()
        status.set(self.clip_data.status) #default
        
        # evaluation lbl frame
        self.eval_lbl_frm = LabelFrame(self.master, text=" Evaluation: ", fg = self.clip_data.eval_color)
        
        self.accept_rad_btn   = Radiobutton(self.eval_lbl_frm,text='Accept' , value='accepted' , variable = status, command = lambda: GUI_commands.accept (self.master, self.tab_control, self.skip_evaluated_cbtn_sel.get(), self.skip_to_prority_cbtn_sel.get()))
        self.decline_rad_btn  = Radiobutton(self.eval_lbl_frm,text='Decline', value='declined' , variable = status, command = lambda: GUI_commands.decline(self.master, self.tab_control, self.skip_evaluated_cbtn_sel.get(), self.skip_to_prority_cbtn_sel.get()))

        # replay and close btns
        self.replay_btn = Button(self.eval_lbl_frm, text="Replay Clip", command = GUI_commands.replay)
        self.close_btn  = Button(self.eval_lbl_frm, text="Close Clip" , command = GUI_commands.close_clip)


        # undo selection btn
        def undo_selection():
            status.set(None)
            GUI_commands.log('status', '')
        self.undo_selection_btn = Button(self.eval_lbl_frm, text="None", command = undo_selection)
        
        
        
    def rating_____widget_setup(self):
        self.rating_lbl    = Label(self.eval_lbl_frm, text="Rating: ")
        self.rating_sbox = Spinbox(self.eval_lbl_frm, from_ = 0, to = 10, width = 5,
                               validate = 'key', validatecommand = self.digits_only)#, command = log_rating)
        self.rating_sbox.delete(0, "end") #gets rid of 0 so the next line makes the default value 40 instead of 400
        self.rating_sbox.insert(0, self.clip_data.rating) #default 
 
        def log_rating(event = None):
            GUI_commands.log('rating', self.rating_sbox.get())
            self.clip_data = GUI_commands.get_current_clip_data()
        self.bind_to_edit(self.rating_sbox, log_rating)
        self.rating_sbox.configure(command = log_rating)
        log_rating()        
        
#         # ``````````````````````````````````````````````````````````````````````````````
#         self.rating_sbox.delete(0, "end") #gets rid of 0 so the next line makes the default value 40 instead of 400
#         print('in build tab, ', type(self.rating_sbox.get()))
#         print(self.rating_sbox['textvariable'])
        
        
        
    def navigation_____widget_setup(self):
        self.nav_lbl_frm = LabelFrame(self.master, text=" Navigation: ")
    
        self.skip_evaluated_cbtn_sel = IntVar(value = int(self.gui_vars['skip_evaluated']))#value sets default
        self.skip_evalutated_cbtn = Checkbutton(self.nav_lbl_frm, text="Skip Evaluated", variable=self.skip_evaluated_cbtn_sel, command = lambda: GUI_commands.log_gui_var('skip_evaluated', self.skip_evaluated_cbtn_sel.get()))

        # skip to priority cbtn
        self.skip_to_prority_cbtn_sel = IntVar(value = int(self.gui_vars['skip_to_priority']))#value sets default
        self.skip_to_priority_cbtn = Checkbutton(self.nav_lbl_frm, text="Skip To Priority", variable=self.skip_to_prority_cbtn_sel, command = lambda: GUI_commands.log_gui_var('skip_to_priority', self.skip_to_prority_cbtn_sel.get()))

        # next and back buttons
        self.back_btn = Button(self.nav_lbl_frm, text="Back", command = lambda: GUI_commands.back(self.master, self.tab_control, self.skip_evaluated_cbtn_sel.get(), self.skip_to_prority_cbtn_sel.get())) #lambda: GUI_commands.back(self.master, self)
        self.next_btn = Button(self.nav_lbl_frm, text="Next", command = lambda: GUI_commands.next(self.master, self.tab_control, self.skip_evaluated_cbtn_sel.get(), self.skip_to_prority_cbtn_sel.get()))



    def prune_clips_____widget_setup(self):
        self.prune_lbl_frm = LabelFrame(self.master, text=" Prune Options: ")
        
        def update_and_log_prune_widgets(event = None):
            self.prune_info_lbl.configure(text= self.clip_pool_data.get_prune_info_str(self.prune_cbtn_sel.get(), self.prune_rating_sbox.get(), self.prune_time_txt_box.get()))
            # print('in build tab, in update_and_log_prune_widgets, 
            GUI_commands.log_gui_var('prune_time', self.prune_time_txt_box.get())
            GUI_commands.log_gui_var('prune_rating', self.prune_rating_sbox.get())
            GUI_commands.log_gui_var('prune_clips', self.prune_cbtn_sel.get())
            
   
        # prune time text box
        self.prune_time_txt_box_lbl = Label(self.prune_lbl_frm, text="Prune To Minimum Time: ")
        self.prune_time_txt_box = Entry(self.prune_lbl_frm,width=5)
        self.prune_time_txt_box.insert(END, self.gui_vars['prune_time']) #default
        self.bind_to_edit(self.prune_time_txt_box, update_and_log_prune_widgets)
        
        # prune rating sbox lbl
        self.prune_sbox_lbl    = Label(self.prune_lbl_frm, text="Prune Clips Rated Below: ")
        
        # prune rating sbox
        self.prune_rating_sbox = Spinbox(self.prune_lbl_frm, from_ = 0, to = 10, width = 5,
                       validate = 'key', validatecommand = self.digits_only, command = update_and_log_prune_widgets)
        self.prune_rating_sbox.delete(0, "end") #gets rid of 0 so the next line makes the default value 40 instead of 400
        self.prune_rating_sbox.insert(0, int(self.gui_vars['prune_rating'])) #default 
        self.bind_to_edit(self.prune_rating_sbox, update_and_log_prune_widgets)
        

        # prune check button
        def prune_cbtn_clk():
            self.prune_time_txt_box.configure( state = 'normal' )
            self.prune_rating_sbox .configure( state = 'normal' )

            if self.prune_cbtn_sel.get() == 1:
                prune_row_dl = self.clip_pool_data.get_prune_row_dl(self.prune_cbtn_sel.get(), self.prune_rating_sbox.get(), self.prune_time_txt_box.get())
                GUI_commands.prune_clips(prune_row_dl)
                update_and_log_prune_widgets()
                self.prune_time_txt_box.configure( state = 'disabled' )
                self.prune_rating_sbox .configure( state = 'disabled' )                
        
        self.prune_cbtn_sel = IntVar(value = self.gui_vars['prune_clips'])#value sets default
        self.prune_cbtn =   Checkbutton(self.prune_lbl_frm, text="Prune Low Rated Clips", variable=self.prune_cbtn_sel, command = prune_cbtn_clk)
        
#         use_txt_overlay_cbtn_clk() #disabled folder name by default if use_txt_overlay_cbtn is 0 by default
        
        
        # prune info lbl
        self.prune_info_lbl    = Label(self.prune_lbl_frm)#, text= self.clip_pool_data.get_prune_info_str(prune_cbtn_sel.get(), self.prune_rating_sbox.get(), self.prune_time_txt_box.get() ) )
        
        prune_cbtn_clk()
        self.clip_pool_data = GUI_commands.get_clip_pool_data()
        update_and_log_prune_widgets()
        
        
    def progess_____widget_setup(self):
        self.prog_lbl_frm = LabelFrame(self.master, text=" Progress Information: ")
        self.total_time_lbl_lbl = Label(self.prog_lbl_frm, text='Total Time: ') 
        self.total_time_lbl     = Label(self.prog_lbl_frm, text=self.clip_pool_data.total_time_str) 
        
        self.clip_num_lbl_lbl = Label(self.prog_lbl_frm, text='Clip Number: ') 
        self.clip_num_lbl     = Label(self.prog_lbl_frm, text=self.clip_pool_data.clip_num_str) 
        
        self.a_clips_num_lbl_lbl = Label(self.prog_lbl_frm, text='# Clips Accepted:') 
        self.a_clips_num_lbl     = Label(self.prog_lbl_frm, text= self.clip_pool_data.num_accepted_clips) 
        
        self.d_clips_num_lbl_lbl = Label(self.prog_lbl_frm, text='# Clips Declined:') 
        self.d_clips_num_lbl     = Label(self.prog_lbl_frm, text= self.clip_pool_data.num_declined_clips) 
        
        self.p_clips_num_lbl_lbl = Label(self.prog_lbl_frm, text='# Clips Pruned:') 
        self.p_clips_num_lbl     = Label(self.prog_lbl_frm, text= self.clip_pool_data.num_pruned_clips) 
        
        self.prcnt_above_avg_lbl_lbl = Label(self.prog_lbl_frm, text='% Clips Above Avg:') 
        self.prcnt_above_avg_lbl     = Label(self.prog_lbl_frm, text= self.clip_pool_data.percent_above_avg_str + ' %') 
        
        self.prcnt_below_avg_lbl_lbl = Label(self.prog_lbl_frm, text='% Clips Below Avg:') 
        self.prcnt_below_avg_lbl     = Label(self.prog_lbl_frm, text= self.clip_pool_data.percent_below_avg_str + ' %') 
        

        
        
        
    def rating_info_____widget_setup(self):
        self.rating_info_lbl_frm = LabelFrame(self.master, text=" Ratings: ")
        starting_row_num = 1
        for r_num, rating_occ_d in enumerate(self.clip_pool_data.ratings_occ_str_dl):
            rating_lbl      = Label(self.rating_info_lbl_frm, text = rating_occ_d['rating'])
            num_occ_lbl     = Label(self.rating_info_lbl_frm, text = rating_occ_d['num_occ'])
            occ_percent_lbl = Label(self.rating_info_lbl_frm, text = rating_occ_d['occ_percent'])
            rating_lbl      .grid(column=1, row=starting_row_num + r_num, sticky='E', ipadx=5)
            num_occ_lbl     .grid(column=2, row=starting_row_num + r_num, sticky='E', ipadx=5)
            occ_percent_lbl .grid(column=3, row=starting_row_num + r_num, sticky='E', ipadx=5)
    
    
        
    def grid_widgets(self):
        self.master.grid_columnconfigure(3, weight=1)
    
    
        blank_lbl_1 = Label(self.prog_lbl_frm, text="") #for spacing 

        
        row_num = 1
        
        # clip info
        self.clip_info_lbl_frm      .grid(column=1, row=1, sticky='WE', columnspan=3, ipadx=5, ipady=5, padx=5, pady=5)
        self.title_lbl_lbl          .grid(column=1, row=1, sticky = 'w')
        self.title_lbl              .grid(column=2, row=1, sticky = 'w')
        self.duration_lbl_lbl       .grid(column=1, row=2, sticky = 'w')
        self.duration_lbl           .grid(column=2, row=2, sticky = 'w')
        
        # progress
        self.prog_lbl_frm           .grid(column=4, row=1, sticky='NSEW', rowspan = 4, padx=5, pady=5, ipadx=5, ipady=5)
        self.total_time_lbl_lbl     .grid(column=1, row=0    , sticky='W', padx=5)
        self.total_time_lbl         .grid(column=2, row=0)
        self.clip_num_lbl_lbl       .grid(column=1, row=1, sticky='W', padx=5)
        self.clip_num_lbl           .grid(column=2, row=1)
        self.a_clips_num_lbl_lbl    .grid(column=1, row=2, sticky='W', padx=5)
        self.a_clips_num_lbl        .grid(column=2, row=2)
        self.d_clips_num_lbl_lbl    .grid(column=1, row=3, sticky='W', padx=5)
        self.d_clips_num_lbl        .grid(column=2, row=3)
        self.p_clips_num_lbl_lbl    .grid(column=1, row=4, sticky='W', padx=5)
        self.p_clips_num_lbl        .grid(column=2, row=4)
        blank_lbl_1                 .grid(column=1, row=5) 
        self.prcnt_above_avg_lbl_lbl.grid(column=1, row=6, sticky='W', padx=5)
        self.prcnt_above_avg_lbl    .grid(column=2, row=6)        
        self.prcnt_below_avg_lbl_lbl.grid(column=1, row=7, sticky='W', padx=5)
        self.prcnt_below_avg_lbl    .grid(column=2, row=7)
        
   
        #text_overlay
        self.txt_overlay_lbl_frm    .grid(column=1, row=2,     columnspan=3, sticky='NSEW', padx=5, pady=5, ipadx=5, ipady=5)
        self.txt_overlay_lbl_frm.grid_columnconfigure(2, weight=1)
        
        self.use_txt_overlay_cbtn   .grid(column=1, row=1)
        self.apply_txt_overlay_btn  .grid(column=2, row=1, sticky = 'w', padx=5, pady=1)
        self.top_txt_lbl            .grid(column=1, row=2)
        self.top_txt_txt_box        .grid(column=2, row=2, columnspan = 1, sticky = 'WE', padx=5, pady=1)
        self.bottom_txt_lbl         .grid(column=1, row=3)
        self.bottom_txt_txt_box     .grid(column=2, row=3, columnspan = 1, sticky = 'WE', padx=5, pady=1)
        
        # trim
        self.trim_lbl_frm           .grid(column=1, row=3, columnspan=3, sticky='NSEW', padx=5, pady=5, ipadx=5, ipady=5)
        self.trim_lbl_frm.grid_columnconfigure(2, weight=1)
#         self.trim_cbtn              .grid(column=1, row=1)
        self.auto_accept_trim_cbtn  .grid(column=2, row=1, sticky="E", padx=5)
        self.trim_clip_btn          .grid(column=3, row=1, sticky="E", padx=5)
        self.trim_wg.start_lbl      .grid(column=1, row=2, sticky='W', padx=5)
        self.trim_wg.diff_lbl       .grid(column=2, row=2)
        self.trim_wg.end_lbl        .grid(column=3, row=2, sticky='E', padx=5)
        self.trim_wg.end_scale      .grid(column=1, row=3, columnspan=3, sticky="EW", padx=5)
        self.trim_wg.start_scale    .grid(column=1, row=4, columnspan=3, sticky="EW", padx=5)
        
        
        #eval
        self.eval_lbl_frm           .grid(column=1, row=4, sticky='NSEW', padx=5, pady=5, ipadx=5, ipady=5)
        
        #rating
        self.rating_lbl             .grid(column=1, row=row_num)
        self.rating_sbox            .grid(column=1, row=row_num + 1, sticky = 'w', padx=5)
        
        
        #accept_decline
        self.accept_rad_btn         .grid(column=2, row=row_num)
        self.decline_rad_btn        .grid(column=2, row=row_num + 1)
        self.undo_selection_btn     .grid(column=2, row=row_num + 2)
        self.close_btn              .grid(column=3, row=row_num    , sticky = 'WE')
        self.replay_btn             .grid(column=3, row=row_num + 1, sticky = 'WE')
        
        
        # prune clips
        self.prune_lbl_frm          .grid(column=3, row=4, sticky = 'NSEW', padx=5, pady=5, ipadx=5, ipady=5)
        self.prune_cbtn             .grid(column=1, row=row_num + 1)
        self.prune_time_txt_box_lbl .grid(column=1, row=row_num + 2, sticky = 'w')
        self.prune_time_txt_box     .grid(column=2, row=row_num + 2, sticky = 'w')
        self.prune_rating_sbox      .grid(column=2, row=row_num + 3, sticky = 'w')
        self.prune_sbox_lbl         .grid(column=1, row=row_num + 3, sticky = 'w')
        self.prune_info_lbl         .grid(column=1, row=row_num + 4, sticky = 'w', columnspan=2)
        
        
        
        
        #navigation
        self.nav_lbl_frm            .grid(column=2, row=4, sticky='NSEW', padx=5, pady=5,  ipady=5)
        self.skip_evalutated_cbtn   .grid(column=1, row=row_num    , sticky = 'w', columnspan=2)
        self.skip_to_priority_cbtn  .grid(column=1, row=row_num + 1, sticky = 'w', columnspan=2)
        self.back_btn               .grid(column=1, row=row_num + 2, sticky = 'e')
        self.next_btn               .grid(column=2, row=row_num + 2, sticky = 'w')
        
        # rating info
        self.rating_info_lbl_frm    .grid(column=5, row=1, rowspan = 4,sticky='NSEW', padx=5, pady=5,  ipady=5)

        
        
        row_num += 10
        
       # blank_lbl_3                 .grid(column=4, row=row_num)
        #blank_lbl_4                 .grid(column=5, row=row_num)
        '''
        SHOW_GRID_WIDTHS = True
        if SHOW_GRID_WIDTHS == True:
            NUM_COLS = 3
            lbl_l = []
            for col_num in range(NUM_COLS):
                color = 'black'
                if col_num % 2 == 0:
                    color = 'white'
                lbl_l.append(Label(self.master, text="", bg = color))
            row_num += 10
            for lbl_num, lbl in enumerate(lbl_l):
                lbl.grid(column=lbl_num + 1, row=row_num, sticky = 'we')

        
        '''
        
        
        
        
        
if __name__ == '__main__':
    import GUI
    GUI.main()