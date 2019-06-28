import json_logger

PROJECT_VARS_JSON_PATH = "C:/Users/Brandon/Documents/Personal_Projects/vid_m_comp/project_vars.json"#"C:\\Users\\mt204e\\Documents\\other\\p\\vid_m_comp\\project_vars.json"

def get_var(key):
    project_vars_d = json_logger.read(PROJECT_VARS_JSON_PATH)
    return project_vars_d[key]







# print(get_var('current_data_dir_path'))