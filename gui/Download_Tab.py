from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import *

from tkinter import *
from tkinter.messagebox import showinfo


#import build_image
#import GUI_utils
import GUI
import Tab
import GUI_commands

#import pool_clips_data_handler

#import Advanced_Tab


DAYS_OF_THE_WEEK_L = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saterday', 'Sunday']
AM_PM_L = ['AM','PM']

class Download_Tab(Tab.Tab):
    def __init__(self, master, tab_control):
        self.tab_control = tab_control
        Tab.Tab.__init__(self, master)
        
        self.num_dl_events = 0
        self.dl_event_name_l = []
        # GUI_commands.init_current_if_needed()
        
        # self.clip_data      = GUI_commands.get_current_clip_data()
        # self.clip_pool_data = GUI_commands.get_clip_pool_data()
        self.gui_vars         = GUI_commands.get_gui_vars()
        
        self.dl_schedule_____widget_setup()
        self.subreddit_management_____widget_setup()        

        
        self.grid_widgets()
		
        
        
    def subreddits_lbox_clk(self, event = None):
        print('in dl tab, lbox clk')
        # will fail when init old event_data
        try:
            self.del_subreddit_btn.configure( state = 'normal' )
            for widget_num, widget in enumerate(self.add_subreddit_btn_l):
                if self.schedule_event_cbtn_sel_l[widget_num].get() == 0:
                    widget.configure( state = 'normal' )
              
            cur_selection_index = self.subreddits_lbox.curselection()
            print('self.subreddits_lbox.curselection(): ', self.subreddits_lbox.curselection())#```````````````````````````````````````````````````
            if cur_selection_index == ():
                # print('should disable now')#````````````````````````````````````````````````````````````````````````````````
                depend_widget_l = self.add_subreddit_btn_l + [self.del_subreddit_btn]
                for widget in depend_widget_l:
                    widget.configure( state = 'disabled' )
        except AttributeError:
            pass

        
        
        
        
        
        
    def dl_schedule_____widget_setup(self):
        self.dl_schedule_lbl_frm = LabelFrame(self.master, text=" Download Schedule: ")
        self.dl_event_name_txt_box_lbl = Label(self.dl_schedule_lbl_frm, text="Download Event Name:")
        
        # dl_event_name_txt_box
        def update_add_event_btn_state(event = None):
            self.add_dl_event_btn.configure( state = 'normal' )
            
            if self.dl_event_name_txt_box.get() in self.dl_event_name_l:
                self.add_dl_event_btn.configure( state = 'disabled' )
        
        self.dl_event_name_txt_box = Entry(self.dl_schedule_lbl_frm)
        self.bind_to_edit(self.dl_event_name_txt_box, update_add_event_btn_state)
        
        self.add_subreddit_btn_l = []
        self.schedule_event_cbtn_sel_l = []

       
        def add_dl_event(event_name, dl_event_data_d = None):
            def log_dl_event(event = None):
                print('in dl tab, logging dl_event')#```````````````````````````````````````````````````````````````````````````````````````````````````````
                GUI_commands.log_dl_event(dl_event_lbl_frm, day_cbox, schedule_event_cbtn_sel, time_txt_box, am_pm_cbox, subreddit_cbox)
                
            def update_schedule_event_cbtn(event = None):
                schedule_event_cbtn.configure( state = 'normal' )
                
                if len(subreddit_cbox['values']) == 0:
                    schedule_event_cbtn.configure( state = 'disabled' )
        
            dl_event_lbl_frm = LabelFrame(self.dl_schedule_lbl_frm, text= " " + event_name + ": ")
            
            # day_cbox
            day_cbox = Combobox(dl_event_lbl_frm, state = 'readonly', values = DAYS_OF_THE_WEEK_L, width = self.max_str_len_in_l(DAYS_OF_THE_WEEK_L) + 1)#, command = log_dl_event)
            day_cbox.current(0) #set the selected item
            day_cbox.bind("<<ComboboxSelected>>", log_dl_event)  # add to am_pm and maybe make into tab func !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # self.bind_to_click(day_cbox, log_dl_event)
            print('in dl tab, type(day_cbox): ', type(day_cbox))#```````````````````````````````````````````````````````````````````````
            
            
            # time text box
            time_txt_box = Entry(dl_event_lbl_frm, width = 5)
            time_txt_box.insert(END, '03:00')
            self.bind_to_edit(time_txt_box, log_dl_event)
            
            # am_pm_cbox
            am_pm_cbox = Combobox(dl_event_lbl_frm, state = 'readonly', values = AM_PM_L , width = 3)
            am_pm_cbox.current(1) #set the selected item
            am_pm_cbox.bind("<<ComboboxSelected>>", log_dl_event)
                
            # subreddit combobox and add btn
            subreddit_cbox = Combobox(dl_event_lbl_frm, state = 'readonly', values = [], width = self.max_str_len_in_l(self.gui_vars['subreddit_list']))#should be self.subreddits_lbox_values.get() but order got weird and Im lazy
            if len(subreddit_cbox['values']) > 0:
                subreddit_cbox.current(0) #set the selected item

            def add_subreddit_btn_clk():
                print('in dl tab, add subreddit')
                cur_selection_index = self.subreddits_lbox.curselection()
                # print('in dl tab, self.subreddits_lbox.get(cur_selection_index): ', self.subreddits_lbox.get(cur_selection_index[0]))#`````````````````````````````````````
                print("list(subreddit_cbox['values']).append(self.subreddits_lbox.get(cur_selection_index)):  ", list(subreddit_cbox['values']).append(self.subreddits_lbox.get(cur_selection_index)))#`````````````````````````
                subreddit_cbox['values'] = [(self.subreddits_lbox.get(cur_selection_index[0]))] + list(subreddit_cbox['values'])
                subreddit_cbox.current(0)
                update_schedule_event_cbtn()
                log_dl_event()
            add_subreddit_btn = Button(dl_event_lbl_frm, text="ADD", command = add_subreddit_btn_clk)
            
            self.add_subreddit_btn_l.append(add_subreddit_btn)

            
            # delete download event btn
            def delete_dl_event(event = None):
                print('in dl tab, delete event')#``````````````````````````````````````````````````````````````````````````````````````````````
                GUI_commands.del_dl_event(dl_event_lbl_frm)
                dl_event_lbl_frm.grid_forget()
                
            del_dl_event_btn = Button(dl_event_lbl_frm, text="Delete Event", command = delete_dl_event)

            
            #use schedule event check button
            schedule_event_cbtn_sel = IntVar(value = 0)#value sets default
            self.schedule_event_cbtn_sel_l.append(schedule_event_cbtn_sel)
            self.subreddits_lbox_clk()

            def schedule_event_cbtn_clk():
                print('in dl tab, schedule event')
                dl_event_widget_l = [day_cbox, time_txt_box, am_pm_cbox, add_subreddit_btn, del_dl_event_btn]
                for widget in dl_event_widget_l:
                    widget.configure( state = 'normal' )
                self.subreddits_lbox_clk()
                
                if schedule_event_cbtn_sel.get() == 1:
                    # if len(subreddit_cbox['values']) == 0:
                        # showinfo("Error", "You must add at least 1 subreddit before you can schedule this download event.")
                        # schedule_event_cbtn_sel.set(0)
                        # return
                    
                    for widget in dl_event_widget_l:
                        widget.configure( state = 'disabled' )
                # GUI_commands.log_dl_event(dl_event_lbl_frm, day_cbox, schedule_event_cbtn_sel, time_txt_box, am_pm_cbox, subreddit_cbox)
                log_dl_event()
            
            schedule_event_cbtn = Checkbutton(dl_event_lbl_frm, text="Schedule Event", variable=schedule_event_cbtn_sel, command = schedule_event_cbtn_clk)

            
            
            # load values from old dl_events if not adding new event
            if dl_event_data_d != None:
                day_cbox.current(DAYS_OF_THE_WEEK_L.index(dl_event_data_d['day']))
                time_txt_box.delete(0, "end")
                time_txt_box.insert(END, dl_event_data_d['time'])
                am_pm_cbox.current(AM_PM_L.index(dl_event_data_d['am_pm']))
                subreddit_cbox['values'] = dl_event_data_d['subreddit_l']
                if len(subreddit_cbox['values']) > 0:
                    subreddit_cbox.current(0)
                    
                schedule_event_cbtn_sel.set(dl_event_data_d['schedule_event'])
                schedule_event_cbtn_clk()
                
            log_dl_event()
            update_schedule_event_cbtn()

            
            
            
            
            
            # grid
            dl_event_lbl_frm    .grid(column=1, row=self.num_dl_events, columnspan = 3, sticky='NSEW', padx=5, pady=2, ipadx=5, ipady=5)
            schedule_event_cbtn .grid(column=1, row=1, padx=5)
            # day_cbox_lbl        .grid(column=2, row=1, padx=5)
            day_cbox            .grid(column=2, row=1, padx=5)
            time_txt_box        .grid(column=3, row=1, padx=5)
            am_pm_cbox          .grid(column=4, row=1, padx=5)
            add_subreddit_btn   .grid(column=5, row=1, padx=5)
            subreddit_cbox      .grid(column=6, row=1, padx=5)
            del_dl_event_btn    .grid(column=7, row=1, padx=5)
            
        
        # add_dl_event_btn
        def add_dl_event_btn_clk(event = None, dl_event_data_d = None):
            print('in dl tab, add')#```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
            self.num_dl_events += 1
            if dl_event_data_d == None:
                add_dl_event(self.dl_event_name_txt_box.get())
            else:
                add_dl_event(dl_event_data_d['event_name'], dl_event_data_d)
            self.dl_event_name_l.append(self.dl_event_name_txt_box.get())
            self.dl_event_name_txt_box.delete(0, "end") # clear self.dl_event_name_txt_box
            update_add_event_btn_state()
            
        
        self.add_dl_event_btn = Button(self.dl_schedule_lbl_frm, text="Add Event", command = add_dl_event_btn_clk)
        update_add_event_btn_state()
        
        
        # to level for reading in old download event data
        def load_dl_event_data():
            dl_event_data_dl = GUI_commands.get_dl_event_data_dl()
            if dl_event_data_dl == []:
                return
            
            for dl_event_data_d in dl_event_data_dl:
                add_dl_event_btn_clk(None, dl_event_data_d)
                
        load_dl_event_data()
            
                
        
        
        
    def subreddit_management_____widget_setup(self):
        self.subreddit_man_lbl_frm = LabelFrame(self.master, text=" Subreddit Management: ")
        self.new_subreddit_txt_box_lbl = Label(self.subreddit_man_lbl_frm, text="New Subreddit:")
        self.new_subreddit_txt_box = Entry(self.subreddit_man_lbl_frm)
        
        # subreddits list box
        def del_subreddit_btn_clk():
            print('in dl tab, delete subreddit')
            cur_selection_index = self.subreddits_lbox.curselection()
            self.subreddits_lbox.delete(cur_selection_index)
            GUI_commands.log_gui_var('subreddit_list', self.subreddits_lbox_values.get())

        # subreddit lbox, lable, delete btn, scrollbar
        self.subreddits_lbox_lbl  = Label(self.subreddit_man_lbl_frm, text="Subreddits: ")
        
        self.del_subreddit_btn    = Button(self.subreddit_man_lbl_frm, text="Delete Subreddit", command = del_subreddit_btn_clk) 
        self.subreddits_lbox_values = Variable(value = self.gui_vars['subreddit_list'])
        self.subreddits_lbox      = Listbox(self.subreddit_man_lbl_frm, listvariable = self.subreddits_lbox_values, height=5)#, font=("Helvetica", 12))
        self.bind_to_click(self.subreddits_lbox, self.subreddits_lbox_clk)
        self.subreddits_lbox_clk()
        
        
        self.subreddits_lbox_sbar = Scrollbar(self.subreddit_man_lbl_frm, orient="vertical", command=self.subreddits_lbox.yview)
             
        self.subreddits_lbox.config(yscrollcommand=self.subreddits_lbox_sbar.set)

        
        
        
        # add_new_subreddit_btn
        def add_new_subreddit_btn_clk(event = None):
            print('in dl tab, add new subreddit')
            if self.new_subreddit_txt_box.get() != '':
                GUI_commands.log_gui_var('subreddit_list', self.gui_vars['subreddit_list'] + [self.new_subreddit_txt_box.get()])
                self.subreddits_lbox.insert(END, self.new_subreddit_txt_box.get())
                self.new_subreddit_txt_box.delete(0, "end") # clear
    
        self.add_new_subreddit_btn = Button(self.subreddit_man_lbl_frm, text="ADD", command = add_new_subreddit_btn_clk)

    
        
    def grid_widgets(self):
        # self.master.grid_columnconfigure(3, weight=1)
        
        # download schedule
        self.dl_schedule_lbl_frm.grid_columnconfigure(1, weight=1) # make it so only the 1st col extends so the other widgets dont get stretched out
        self.dl_schedule_lbl_frm        .grid(column=1, row=1  , sticky='EWN', padx=5, pady=5, ipadx=5, ipady=5)
        self.dl_event_name_txt_box_lbl  .grid(column=1, row=100, sticky='E') # make lots of room for dl_event lbl frames
        self.dl_event_name_txt_box      .grid(column=2, row=100, sticky='WE', padx=5) # make lots of room for dl_event lbl frames
        self.add_dl_event_btn           .grid(column=3, row=100, sticky='WE', padx=5) # make lots of room for dl_event lbl frames
        
        # subreddit management
        self.subreddit_man_lbl_frm      .grid(column=2, row=1  , sticky='EWN', padx=5, pady=5, ipadx=5, ipady=5)
        self.new_subreddit_txt_box_lbl  .grid(column=1, row=1, columnspan = 2)
        self.new_subreddit_txt_box      .grid(column=1, row=2, padx=5)
        self.add_new_subreddit_btn      .grid(column=2, row=2)
        self.subreddits_lbox_lbl        .grid(column=1, row=3)
        self.subreddits_lbox            .grid(column=1, row=4, sticky='WE',  padx=(5, 0))
        self.subreddits_lbox_sbar       .grid(column=2, row=4, sticky='NSW')
        self.del_subreddit_btn          .grid(column=1, row=5, sticky='W', padx=5)
        
        
if __name__ == '__main__':
    GUI.main()