import glob
import os
# from shutil import copyfile
import shutil
 
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
            
            
            
def copy_files_to_dest(file_path_l, dest_dir_path): 
#     if os.path.isdir(dest_dir_path) == False:
#         os.mkdir(dest_dir_path)
    make_dir_if_not_exist(dest_dir_path)
               
    for file_path in file_path_l:
        shutil.copy(file_path, dest_dir_path )
            
            
def make_dir_if_not_exist(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        
def delete_if_exists(path):
    if os.path.exists(path):
        os.remove(path)
            

if __name__ == '__main__':
    print('in file_system_utils main...')
#     import download_vids
#     download_vids.download_vids(20, ['videomemes'])
#     print(get_relative_path_of_files_in_dir('vids_to_compile', '.mp4'))
    file_path_l = ['C:/Users/Brandon/Documents/Personal_Projects/reddit_comp/old/output.mp4',
                    'C:/Users/Brandon/Documents/Personal_Projects/reddit_comp/old/post_0000.mp4']
    dest_file_path = 'clips_to_compile'
    copy_files_to_dest(file_path_l, dest_file_path)






