import file_system_utils
import os


# assumes dir sturcture like this:"
# some_dir
#  |
#  |-- vid_m_comp
#  |   |-- project_vars_handler.py
#  |   |-- project_vars.json
#  |  
#  |-- vid_m_comp_big_data  


VID_M_COMP_DIR_PATH = file_system_utils.get_path_to_current_file(__file__)

# print('in project vars, VID_M_COMP_DIR_PATH: ', VID_M_COMP_DIR_PATH)#````````````````````````````````````````````

# print('in project_vars, : os.path.abspath( VID_M_COMP_DIR_PATH)', os.path.abspath( VID_M_COMP_DIR_PATH))#```````````````````````````````````````````````````````````````````````

VID_M_COMP_BIG_DATA_DIR_PATH = os.path.dirname(VID_M_COMP_DIR_PATH) + '\\vid_m_comp_big_data'

# print('in project vars, VID_M_COMP_BIG_DATA_DIR_PATH: ', VID_M_COMP_BIG_DATA_DIR_PATH)#````````````````````````````````````````````


HISTORICAL_DATA_DIR_PATH = VID_M_COMP_DIR_PATH + '\\historical_data'
POOL_CLIPS_DATA_CSV_PATH = VID_M_COMP_DIR_PATH + '\\pool_clips_data.csv'
CURRENT_DATA_DIR_PATH    = VID_M_COMP_BIG_DATA_DIR_PATH + '\\current_data'
THUMBNAIL_PATH_INTENDED  = CURRENT_DATA_DIR_PATH + '\\thumbnail.png'


# print('in project vars, THUMBNAIL_PATH_INTENDED: ', THUMBNAIL_PATH_INTENDED)#````````````````````````````````````````````











# print(get_var("historical_data_dir_path"))

