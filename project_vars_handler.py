import json_logger
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
VID_M_COMP_BIG_DATA_DIR_PATH = os.path.dirname(VID_M_COMP_DIR_PATH) + '\\vid_m_comp_big_data'

PROJECT_VARS_JSON_PATH = VID_M_COMP_DIR_PATH + "\\project_vars.json"

STR_REPLACE_D = {'<VID_M_COMP_PATH>'             : VID_M_COMP_DIR_PATH,
                 '<VID_M_COMP_BIG_DATA_DIR_PATH>': VID_M_COMP_BIG_DATA_DIR_PATH}

def load_vars_and_apply_replacements():
    project_vars_d = json_logger.read(PROJECT_VARS_JSON_PATH)
    for key, val in project_vars_d.items():
        for str_to_replace, replacement_str in STR_REPLACE_D.items():
            if str_to_replace in val:
                # print('FOUND STR TO REPLACE, val: ', val)#`````````````````````````````````````````````````
                project_vars_d[key] = val.replace(str_to_replace, replacement_str)
                # print('val after replace: ', val, val.replace(str_to_replace, replacement_str))#``````````````````````````````````````````````````
    return project_vars_d
    

def get_var(key):
    # project_vars_d = json_logger.read(PROJECT_VARS_JSON_PATH)
    project_vars_d = load_vars_and_apply_replacements()
    
    # print(project_vars_d)#``````````````````````````````````````````````````````````````````````````
    return project_vars_d[key]







# print(get_var("historical_data_dir_path"))

