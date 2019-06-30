import webbrowser
# import os

# to be able to import from parent dir
import sys
parent_dir_path = ''
for dir in sys.path[0].split('\\')[0:-1]:
    parent_dir_path += dir + '\\'
sys.path.append(parent_dir_path[0:-1])

# from parent dir
import file_system_utils


def open_snappa_in_chrome():   
    url = "https://snappa.com/app/graphic/d8334e8f-a11a-467c-a4ca-52fd4f748f26"
    chrome_browser = webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s")
    chrome_browser.open_new_tab(url)
    

# finds most recent download from snappa in downloads folder and renames it to thumbnail path
def load_snappa_dl_as_thumbnail(thumbnail_path):
    dl_file_paths = file_system_utils.get_file_paths_in_dir_by_age("C:\\Users\\Brandon\\Downloads")
    for file_path in reversed(dl_file_paths):
        file_name = file_system_utils.get_filename_from_path(file_path)
        if file_name.startswith('Untitled Design'):
            print('renaming: ', file_path)#`````````````````````````````````````````````````````````````````````````````
#             os.rename(file_path, thumbnail_path)
            file_system_utils.rename_file_overwrite(file_path, thumbnail_path)
            return
# load_snappa_dl_as_thumbnail('ddd')








