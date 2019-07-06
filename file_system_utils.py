import glob
import os
# from shutil import copyfile
import shutil
from distutils.dir_util import copy_tree
import ntpath
 
# VVVVV Internal VVVVV

 
# VVVVV External VVVVV
 
 
def get_newest_file_path(dir_path):
    list_of_files = glob.glob(dir_path + '/*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    # print (latest_file)
    return latest_file


def delete_all_files_in_dir(dir_path):
    for the_file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
            
def delete_all_dirs_in_dir_if_exists(dir_path):
    if os.path.exists(dir_path):
        for the_file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, the_file)
            try:
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)
            
def get_relative_path_of_files_in_dir(dir_path, file_type):
    # Getting the current work directory (cwd)
    thisdir = os.getcwd()
    
    path_list = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(dir_path):
        for file in f:
            if file_type in file:
#                 print(os.path.join(r, file))
                path_list.append(os.path.join(r, file))
    return path_list
            
            
# works for files and dirs
def copy_objects_to_dest(path_l, dest_dir_path):
    make_dir_if_not_exist(dest_dir_path)
    
    for path in path_l:
        if   os.path.isdir(path):
            copy_tree(path, dest_dir_path)
        elif os.path.isfile(path):
            shutil.copy(path, dest_dir_path)

            
            
            
            
def copy_files_to_dest(file_path_l, dest_dir_path): 
#     if os.path.isdir(dest_dir_path) == False:
#         os.mkdir(dest_dir_path)
    make_dir_if_not_exist(dest_dir_path)
               
    for file_path in file_path_l:
        shutil.copy(file_path, dest_dir_path )
            
            
def make_dir_if_not_exist(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        
def delete_if_exists(path):
    if os.path.exists(path):
        if   os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)
        else:
            raise Exception('ERROR:  Gave something that is not a file or a dir, bad path: ', path)
        
        
# gets size of dir (and maybe file?) in bytes
def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size
        

# returns oldest first, youngest last
def get_file_paths_in_dir_by_age(dirpath):
    a = [s for s in os.listdir(dirpath)
         if os.path.isfile(os.path.join(dirpath, s))]
    a.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
    
    abs_path_l = []
    for rel_path in a:
        abs_path_l.append(dirpath + '/' + rel_path)
    return abs_path_l



def is_path_creatable(pathname):
    '''
    `True` if the current user has sufficient permissions to create the passed
    pathname; `False` otherwise.
    '''
    # Parent directory of the passed path. If empty, we substitute the current
    # working directory (CWD) instead.
    dirname = os.path.dirname(pathname) or os.getcwd()
    return os.access(dirname, os.W_OK)

# returns true if path could be created and ends with ext
def is_file_path_valid(path, extention = None):
    if not is_path_creatable(path):
        return False
    if extention != None and not path.endswith(extention):
        return False
    return True
    
    
def get_filename_from_path(path):
    return ntpath.basename(path)
    
    
def rename_file_overwrite(src_file_path, dest_file_path):
    delete_if_exists(dest_file_path)
    os.rename(src_file_path, dest_file_path)
    
# SHOULD PROBABLY RENAME
# !!!!! ONLY WAY TO USE THIS FUNC:  file_system_utils.get_path_to_current_file(__file__) !!!!!
# returns absolute path to the dir that contains the file that calls this function,
# NOT the current working directory
# the only reason this function is here is because I know that
# if it isn't, I wont be able to find it later
def get_path_to_current_file(file_obj):
    return os.path.dirname(os.path.abspath(file_obj))








if __name__ == '__main__':
    print('in file_system_utils main...')
#     import download_vids
#     download_vids.download_vids(20, ['videomemes'])
#     print(get_relative_path_of_files_in_dir('vids_to_compile', '.mp4'))
    file_path_l = ['C:/Users/Brandon/Documents/Personal_Projects/reddit_comp/old/output.mp4',
                    'C:/Users/Brandon/Documents/Personal_Projects/reddit_comp/old/post_0000.mp4']
    dest_file_path = 'clips_to_compile'
    copy_files_to_dest(file_path_l, dest_file_path)






