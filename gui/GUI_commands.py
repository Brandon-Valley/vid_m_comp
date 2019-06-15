from threading import Thread
from tkinter import *
from tkinter.messagebox import showinfo

import Build_Tab
import Clip_Pool_Data
import Clip_Data
import clip_order
#import txt_logger

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


try:
    import text_overlay
    import compile_clips
except ImportError:
    print('import_fail')



#GUI_VARS_TXT_FILE_PATH = 'gui_vars.txt'
GUI_VARS_JSON_FILE_PATH = 'gui_vars.json'


#   VVVVV INTERNAL UTILITIES VVVVV

def restart_build_tab(master, tab_control, tab_pos):
    master.destroy()
    tab1 = Frame(tab_control)
    tab_control.insert(tab_pos,tab1, text='Build')
    tab_control.select(tab_pos)
    Build_Tab.Build_Tab(tab1, tab_control)


def navigate(move_amount, master, tab_control, skip_evaluated):
    try:
        vid_player_control.close_vid_if_open()
    except NameError:
        print('Cant close vid because cant import vid_player_pontrol')
    
    if skip_evaluated and not pool_clips_data_handler.non_eval_clips_exist():
        print('all evaluated')
        showinfo("Info", "All Clips Have Been Evaluated")
        return
        
    pool_clips_data_handler.move_current(move_amount)
    while (skip_evaluated and pool_clips_data_handler.read_from_current('status') != ''):
        pool_clips_data_handler.move_current(move_amount)
    restart_build_tab(master, tab_control, 0)
    
    try:
        vid_player_control.open_vid(pool_clips_data_handler.read_from_current('clip_path'))
    except NameError:
        print('Cant open vid because cant import vid_player_pontrol')
    
    
    
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
    json_logger.log_vars({header:str(value)}, GUI_VARS_JSON_FILE_PATH)
    
    
    
def back(master, tab_control, skip_evaluated):
    print('back')
    navigate(-1, master, tab_control, skip_evaluated)
   
def next(master, tab_control, skip_evaluated):
    print('next')
    navigate(1, master, tab_control, skip_evaluated)
    
def accept(master, tab_control, skip_evaluated):
    print('Clip accepted!')
    pool_clips_data_handler.write_to_current('status', 'accepted')
    next(master, tab_control, skip_evaluated)
    
def decline(master, tab_control, skip_evaluated):
    print('Clip declined!')
    pool_clips_data_handler.write_to_current('status', 'declined')
    next(master, tab_control, skip_evaluated)
    
def replay():
    vid_player_control.close_vid_if_open()
    vid_player_control.open_vid(pool_clips_data_handler.read_from_current('clip_path'))
    
def close_clip():
    vid_player_control.close_vid_if_open()
    
def prune_clips(prune_row_dl):
    print('prune')
    pool_clips_data_handler.prune_by_row_dl(prune_row_dl)
    
    
def apply_txt_overlay(top_text, bottom_text):
    print('apply text overlay')
    cur_clip_path = pool_clips_data_handler.read_from_current('clip_path')
    #trim off the .mp4
    trimmed_cur_clip_path = cur_clip_path[:-4]
    text_overlay_clip_path = trimmed_cur_clip_path + '__txt_overlay.mp4'
    
    def create_and_log_txt_overlay_clip():
        text_overlay.text_overlay(top_text, bottom_text, cur_clip_path, text_overlay_clip_path)
        pool_clips_data_handler.write_to_current('txt_overlay_clip_path', text_overlay_clip_path)
        print('done with making text overlay, saved in: ', text_overlay_clip_path)
        print('need to finish this thing !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        
    text_overlay_thread = Thread(target=create_and_log_txt_overlay_clip)#, args=(img_path_list[3], 'option_3' , qo_dict)))  
    text_overlay_thread.start()
    
    
    
    


    
# VVVVV COMPILE TAB VVVVV

def compile(output_path, play_output_btn, clip_sort_method_str, prog_widget_d):
    print('compile clips')
    
    play_output_btn.configure(state = "disabled")
    
    rated_clip_path_dl = pool_clips_data_handler.get_rated_clip_path_dl()
    ordered_clip_path_l = clip_order.order_rated_clip_paths(rated_clip_path_dl, clip_sort_method_str, 2, 2)
    
    compile_clips.compile_clips(ordered_clip_path_l, output_path, prog_widget_d)
    play_output_btn.configure(state = "normal")
    
def play_output(vid_path):
    print('play output')
    vid_player_control.close_vid_if_open()
    vid_player_control.open_vid(vid_path)
    
if __name__ == '__main__':
    import GUI
    GUI.main()   
