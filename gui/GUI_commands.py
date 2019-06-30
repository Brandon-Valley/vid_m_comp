from tkinter import *
from tkinter.messagebox import showinfo
import time # for testing
from threading import Thread
import os

import Build_Tab
import Clip_Pool_Data
import Clip_Data
import clip_order
import historical_data
import snappa_utils
#import txt_logger

# import vid_player_control

try:
    import vid_player_control
except:
    print('cant import vid_player_control')
    


# to be able to import from parent dir
import sys
parent_dir_path = ''
for dir in sys.path[0].split('\\')[0:-1]:
    parent_dir_path += dir + '\\'
sys.path.append(parent_dir_path[0:-1])

# from parent dir

import pool_clips_data_handler
import json_logger
import project_vars_handler
import youtube_upload
import file_system_utils


try:
    import text_overlay
    import compile_clips
except ImportError:
    print('import_fail')
    



GUI_VARS_JSON_FILE_PATH = 'gui_vars.json'
DL_SCHEDULE_JSON_PATH = '../dl_schedule.json'


#   VVVVV INTERNAL UTILITIES VVVVV

def restart_build_tab(master, tab_control, tab_pos):
    master.destroy()
    tab1 = Frame(tab_control)
    tab_control.insert(tab_pos,tab1, text='Build')
    tab_control.select(tab_pos)
    Build_Tab.Build_Tab(tab1, tab_control)


def navigate(move_amount, master, tab_control, skip_evaluated, skip_to_priority):
    start_time = time.time()
#     try:
#         vid_player_control.close_vid_if_open()
#     except NameError:
#         print('Cant close vid because cant import vid_player_pontrol')
    
    if skip_evaluated and not pool_clips_data_handler.non_eval_clips_exist():
        print('all evaluated')
        showinfo("Info", "All Clips Have Been Evaluated")
        return
    
    pool_clips_data_handler.write_to_current('priority_next', '')
    
    priority_row_num = False
    if skip_to_priority:
        priority_row_num = pool_clips_data_handler.get_next_priority_row_num()
        
    if priority_row_num != False:
        pool_clips_data_handler.move_current_to_row_num(priority_row_num)
    else:
        pool_clips_data_handler.move_current(move_amount)
        while (skip_evaluated and pool_clips_data_handler.read_from_current('status') != ''):
            pool_clips_data_handler.move_current(move_amount)
    restart_build_tab(master, tab_control, 0)
    
    try:
        vid_player_control.open_vid(pool_clips_data_handler.get_current_main_clip_path())
    except NameError:
        print('Cant open vid because cant import vid_player_pontrol')
        
    print('in gui utils, navigation total time: ', time.time() - start_time)
    
    
    
#   VVVVV INPUT COMMANDS VVVVV

def get_clip_pool_data():
    row_dl = pool_clips_data_handler.get_csv_row_dl()
    return Clip_Pool_Data.Clip_Pool_Data(row_dl)
    
def get_current_clip_data():
    row_dl = pool_clips_data_handler.get_csv_row_dl()

    for row_d in row_dl:
        if row_d['current'] == '1':
            return Clip_Data.Clip_Data(row_d)
    # if none are marked current (only happens with new csv)
    pool_clips_data_handler.write_to_current('current', '1')
    get_current_clip_data()
            
def get_gui_vars():
    #return txt_logger.readVars(GUI_VARS_TXT_FILE_PATH)
    return json_logger.read(GUI_VARS_JSON_FILE_PATH)

def init_current_if_needed():
    pool_clips_data_handler.init_current_if_needed()
    

            
            
            
#   VVVVV OUTPUT COMMANDS VVVVV

def log(header, value):
    pool_clips_data_handler.write_to_current(header, value)
    
def log_gui_var(header, value):
    #txt_logger.logVars(GUI_VARS_TXT_FILE_PATH, {header:str(value)})
    json_logger.log_vars({header:value}, GUI_VARS_JSON_FILE_PATH)
    
    
    
def back(master, tab_control, skip_evaluated, skip_to_priority):
    print('back')
    navigate(-1, master, tab_control, skip_evaluated, skip_to_priority)
   
def next(master, tab_control, skip_evaluated, skip_to_priority):
    print('next')
    navigate(1, master, tab_control, skip_evaluated, skip_to_priority)
    
def accept(master, tab_control, skip_evaluated, skip_to_priority):
    print('Clip accepted!')
    pool_clips_data_handler.write_to_current('status', 'accepted')
    next(master, tab_control, skip_evaluated, skip_to_priority)
    
def decline(master, tab_control, skip_evaluated, skip_to_priority):
    print('Clip declined!')
    pool_clips_data_handler.write_to_current('status', 'declined')
    next(master, tab_control, skip_evaluated, skip_to_priority)
    
def replay():
    vid_player_control.close_vid_if_open()
    vid_player_control.open_vid(pool_clips_data_handler.read_from_current('clip_path'))
    
def close_clip():
    vid_player_control.close_vid_if_open()
    
def prune_clips(prune_row_dl):
    pool_clips_data_handler.prune_by_row_dl(prune_row_dl)
    
    
def apply_txt_overlay(top_text, bottom_text, master, tab_control, skip_evaluated, skip_to_priority):
    print('apply text overlay')
    cur_clip_path = pool_clips_data_handler.read_from_current('clip_path')
    #trim off the .mp4
    trimmed_cur_clip_path = cur_clip_path[:-4]
    text_overlay_clip_path = trimmed_cur_clip_path + '__txt_overlay.mp4'
    
    def create_and_log_txt_overlay_clip():
        row_num = pool_clips_data_handler.get_cur_row_num()
        text_overlay.text_overlay(top_text, bottom_text, cur_clip_path, text_overlay_clip_path)
        pool_clips_data_handler.write_to_row_num(row_num, 'txt_overlay_clip_path', text_overlay_clip_path)
        pool_clips_data_handler.write_to_row_num(row_num, 'priority_next', '1')
        print('done with making text overlay, saved in: ', text_overlay_clip_path)
        
    text_overlay_thread = Thread(target=create_and_log_txt_overlay_clip)#, args=(img_path_list[3], 'option_3' , qo_dict)))  
    text_overlay_thread.start()
    next(master, tab_control, skip_evaluated, skip_to_priority)
    
    
    
    


    
# VVVVV COMPILE TAB VVVVV

def compile(output_path, play_output_btn, clip_sort_method_str, prog_widget_d):
    print('compile clips')
    
    def _compile_clips_thread():
        play_output_btn.configure(state = "disabled")
        
        rated_clip_path_dl = pool_clips_data_handler.get_rated_clip_path_dl()
        print('in gui_commands, len(rated_clip_path_dl)', len(rated_clip_path_dl))#```````````````````````````````````````````````````````
        ordered_clip_path_l = clip_order.order_rated_clip_paths(rated_clip_path_dl, clip_sort_method_str, 2, 2)
        print('in gui_commands, len(ordered_clip_path_l): ', ordered_clip_path_l)#````````````````````````````````````````````````
        
        compile_clips.compile_clips(ordered_clip_path_l, output_path, prog_widget_d)
        play_output_btn.configure(state = "normal")
    
    compile_thread = Thread(target=_compile_clips_thread)#, args=(img_path_list[3], 'option_3' , qo_dict)))  
    compile_thread.start()
    
    
    
def play_output(vid_path):
    print('play output')
    vid_player_control.close_vid_if_open()
    vid_player_control.open_vid(vid_path)
    
def log_and_delete_current_data():
    print('log and delete current data')
    historical_data.log_and_delete_current_data()
    
    
# really not the best way to be doing this
def is_file_path_valid(path, ext):
    return file_system_utils.is_file_path_valid(path, ext)
    
    
def compile_upload_log(tabs):
    print('Starting Compile, Upload, then Log/Delete...')
    compile(tabs['compile'].output_path_txt_box.get(), tabs['compile'].play_output_btn, tabs['compile'].clip_sort_cbox.get(), tabs['compile'].prog_widget_d)
    print('finished compile, starting upload...')
    upload(tabs['upload'].vid_path_txt_box.get(), tabs['upload'].title_txt_box.get(), tabs['upload'].descrip_txt_box.get(), tabs['upload'].tags_txt_box.get(), tabs['upload'].privacy_cbox.get(), tabs['upload'].thumbnail_path_txt_box.get())
    print('finished upload, logging/deleteing...')
    log_and_delete_current_data()
    print('Finished Compile, Upload, then Log/Delete')

    
    
# VVVVV DOWNLOAD TAB VVVVVV  

# VVVVV INTERNAL VVVVV
def event_name(dl_event_lbl_frm):
    return dl_event_lbl_frm["text"][1:-2]

# VVVVV EXTERNAL VVVVV
    
def get_dl_event_data_dl():
    if os.path.isfile(DL_SCHEDULE_JSON_PATH):
        dl_event_dl = json_logger.read(DL_SCHEDULE_JSON_PATH)
    else:
        dl_event_dl = []
    return dl_event_dl



    
def log_dl_event(dl_event_lbl_frm, day_cbox, schedule_event_cbtn_sel, time_txt_box, am_pm_cbox, subreddit_cbox):
    
    log_d = {"event_name"     : event_name(dl_event_lbl_frm), # remove the space at the start and the ': ' at the end
             "day"            : day_cbox.get(),
             "schedule_event" : schedule_event_cbtn_sel.get(),
             "time"           : time_txt_box.get(),
             "am_pm"          : am_pm_cbox.get(),
             "subreddit_l"    : subreddit_cbox['values']}
             
    # print('in gui_commands, log_d: ', log_d)#```````````````````````````````````````````````````````````````````````
        
    dl_event_dl = get_dl_event_data_dl()
        
    # add to data if event already exists    
    found = False
    for d_num, dl_event_d in enumerate(dl_event_dl):
        if dl_event_d['event_name'] == log_d['event_name']:
            found = True
            dl_event_dl[d_num] = log_d
            break
    
    # add new if event does not exist yet
    if found == False:
        dl_event_dl.append(log_d)
            
    json_logger.write(dl_event_dl, DL_SCHEDULE_JSON_PATH)
        
        
        
        
def del_dl_event(dl_event_lbl_frm):
    dl_event_dl = get_dl_event_data_dl()
    for d in dl_event_dl:
        if d['event_name'] == event_name(dl_event_lbl_frm):
            dl_event_dl.remove(d)
    json_logger.write(dl_event_dl, DL_SCHEDULE_JSON_PATH)
    
    
    
    
    
# VVVVV UPLOAD TAB VVVVV


def upload(vid_path, title, description, tags, privacy_status, thumbnail_path):
    print('Uploading Video...')
    title       = '"' + title       + '"'
    description = '"' + description + '"'
    tags        = '"' + tags        + '"'
    category = '23'
    youtube_upload.youtube_upload(vid_path, title, description, tags, category, privacy_status, thumbnail_path)
    
    
    
def open_snappa_in_chrome():
    snappa_utils.open_snappa_in_chrome()
    
def load_snappa_dl_as_thumbnail(thumbnail_path):
    snappa_utils.load_snappa_dl_as_thumbnail(thumbnail_path)
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == '__main__':
    import GUI
    GUI.main()   
