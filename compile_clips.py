
#   concat:out:a0 -> Stream #0:1 (aac)
# Press [q] to stop, [?] for help
# frame=    0 fps=0.0 q=0.0 size=       0kB time=-577014:32:22.77 bitrate=  -0.0kbits/s speed=N/A    
# [Parsed_concat_0 @ 00000128d3174f80] Input link in1:v0 parameters (size 1334x750, SAR 1:1) do not match the corresponding output link in0:v0 parameters (360x640, SAR 1:1)
# [Parsed_concat_0 @ 00000128d3174f80] Failed to configure output pad on Parsed_concat_0
# Error reinitializing filters!
# Failed to inject frame into filter network: Invalid argument
# Error while processing the decoded data for stream #42:0
# Conversion failed!






import os
from os import listdir
from os.path import isfile, join
#    
import subprocess
import cv2
import time
#  
import file_system_utils
import project_vars_handler


# VIDS_TO_COMPILE_FOLDER_PATH = 'vids_to_compile'
CLIPS_TO_COMPILE_DIR_PATH = project_vars_handler.get_var('current_data_dir_path') + '/clips_to_compile'
# OUTPUT_VID_DIMS = [1080, 720, 480, 360, 240, 144] # other heights can work, but not all, so stick to these because they're safe
                       
#                    w    h              
OUTPUT_VID_DIMS_L =[(3840,2160),
                    (2560,1440),
                    (1920,1080),
                    (1280, 720),
                     (854, 480),
                     (640, 360),
                     (426, 240)]

VID_CONCAT_FILE_PATH = 'concat_filepaths.txt'
# OUTPUT_VID_FILE_PATH = 'output.mp4'



def write_text_file(file_path, line_list):
    f = open(file_path, 'w', encoding='utf-8')
    # write to file
    for line in line_list:
        f.write(line + '\n')
    # cleanup
    f.close()
   
## do not delete until done with many full tests !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
# # make sure everyone ends with .mp4
# def clean_up_vid_extentions():
#     vid_filename_list = os.listdir(VIDS_TO_COMPILE_FOLDER_PATH)
#     
#     for vid_filename in vid_filename_list:
#         split_vid_filename = vid_filename.split('.')
#         if split_vid_filename[-1] != 'mp4':
#             new_vid_filename = split_vid_filename[0] + '.mp4'
#             os.rename(VIDS_TO_COMPILE_FOLDER_PATH + '/' + vid_filename, VIDS_TO_COMPILE_FOLDER_PATH + '/' + new_vid_filename)
    
    
# dont delete until you have done a LOT of testing !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# def get_height_of_vid(vid_file_path):
#     vid = cv2.VideoCapture(vid_file_path)
#     return vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

def get_vid_dims(vid_file_path):
    vid = cv2.VideoCapture(vid_file_path)
    return (vid.get(cv2.CAP_PROP_FRAME_WIDTH), vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    
def get_height_of_tallest_vid_in_dir(dir_path):
    vid_file_paths = file_system_utils.get_relative_path_of_files_in_dir(dir_path, '.mp4')
    
    max_height = 0
    for vid_file_path in vid_file_paths:
        height = get_vid_dims(vid_file_path)[1]
        if height > max_height:
            max_height = height
    return max_height

# dont delete until you have done a LOT of testing !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# def shortest_working_height(tallest_vid_height):
#     h = OUTPUT_VID_HEIGHTS[0]
#     for height in OUTPUT_VID_HEIGHTS[1:]:
#         if tallest_vid_height < height:
#             h = height
#         else:
#             break
#     return h

def smallest_working_dims(tallest_vid_height):
    dims = (0,0)
    
    if tallest_vid_height > OUTPUT_VID_DIMS_L[0][1]:
        raise Exception('ERROR:  Clip height > tallest height in OUTPUT_VID_DIMS_L: %s > %s' %(tallest_vid_height, OUTPUT_VID_DIMS_L[0][1]))
    
    for valid_dims in OUTPUT_VID_DIMS_L:
        if tallest_vid_height <= valid_dims[1]:
            dims = valid_dims
        else:
            return dims
#     return dims


# dont delete until you have done a LOT of testing !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# def resize_all_vids_in_dir(new_height, dir_path):
#     from moviepy.editor import VideoFileClip # this here so annoying msg / load doesnt happen every gui start
# 
#     vid_file_paths = file_system_utils.get_relative_path_of_files_in_dir(dir_path, '.mp4')
#     
#     for vid_file_path in vid_file_paths:
#         if new_height != get_height_of_vid(vid_file_path):
#             clip = VideoFileClip(vid_file_path)
# #             clip_resized = clip.resize(height=new_height) # make the height 360px ( According to moviePy documenation The width is then computed so that the width/height ratio is conserved.)
#             clip_resized = clip.resize(height=1080, width=1920) # make the height 360px ( According to moviePy documenation The width is then computed so that the width/height ratio is conserved.)
# 
#             clip_resized.write_videofile('temp.mp4')
#             
#             clip.reader.close()
#             clip.audio.reader.close_proc()
#             
#             os.remove(vid_file_path)
#             os.rename('temp.mp4', vid_file_path)
            
            
def get_scaled_width(dims, new_h):
    og_ratio = dims[0] / dims[1]
    return og_ratio * new_h
            
            
            
def resize_all_vids_in_dir(dims, dir_path):
    vid_file_paths = file_system_utils.get_relative_path_of_files_in_dir(dir_path, '.mp4')
    
    o_w = str(dims[0])
    o_h = str(dims[1])
    
    for vid_file_path in vid_file_paths:
        temp_file_path = 'temp_' + vid_file_path.split('\\')[-1] 
        
        
        vid_dims = get_vid_dims(vid_file_path)
        scaled_w = get_scaled_width(vid_dims, dims[0]) # put back in after test !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        if dims != vid_dims:  
            w_pad = str( int((dims[0] - scaled_w     / 4 ) ))
            h_pad = str( int((dims[1] - vid_dims[1]) / 2 ))
            cmd = 'ffmpeg -i ' + vid_file_path + ' -vf scale=' + o_w + ':' + o_h + ':force_original_aspect_ratio=decrease,pad=' + o_w + ':' + o_h + ':' + w_pad + ':' + h_pad + ',setsar=1 ' + temp_file_path + ' -y'
            print('cmd: ', cmd) #```````````````````````````````````````````````````````````````````````````````````````````````````````````````````         
#             cmd = 'ffmpeg -i ' + vid_file_path + ' -vf scale=' + str(dims[0]) + ':' + str(dims[1]) + ' temp.mp4'
            subprocess.call(cmd, shell=True)
             
            
            
            
            while(True):
                try:   
                    os.remove(vid_file_path)
                    break
                except PermissionError as e:
                    print('got permission error when deleting file, sleeping then trying again...')
                    time.sleep(1)
            
            
            while(True):
                try:   
                    os.rename(temp_file_path, vid_file_path)
                    break
                except PermissionError as e:
                    print('got permission error when re-sizing, sleeping then trying again...')
                    time.sleep(1)


    
def compile_all_clips_in_dir(clips_dir_path, output_vid_path):
#     from moviepy.editor import VideoFileClip, concatenate_videoclips # this here so annoying msg / load doesnt happen every gui start

    # build concat txt file
#     line_list = []
#     vid_filenames_to_compile = [f for f in listdir(clips_dir_path) if isfile(join(clips_dir_path, f))]
# 
#     for vid_filename in vid_filenames_to_compile:
#         vid_file_path = CLIPS_TO_COMPILE_DIR_PATH + '/' + vid_filename 
#         line_list.append('file ' + vid_file_path)
# #         print(line_list)#``````````````````````````````````````````````````````````````````````````````````````````````````````````````
#     write_text_file(VID_CONCAT_FILE_PATH, line_list)
#          
#      
#     # concat the files in the txt file
#     cmd = 'ffmpeg -f concat -i ' + VID_CONCAT_FILE_PATH + ' -c copy ' + output_vid_path + ' -y'
#     print('cmd: ', cmd)#`````````````````````````````````````````````````````````````````````````````````````````````````
#     subprocess.call(cmd, shell=True)


#     # this one works but cmd line str can be too long !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    vid_filenames_to_compile = [f for f in listdir(clips_dir_path) if isfile(join(clips_dir_path, f))]
    input_files_str = ''
    for vid_filename in vid_filenames_to_compile:
        vid_file_path = clips_dir_path + '/' + vid_filename 
        input_files_str += ' -i ' + vid_file_path
         
    num_clips = str(len(vid_filenames_to_compile))
  
    cmd = 'ffmpeg ' + input_files_str + ' -filter_complex "[0:v:0] [0:a:0] [1:v:0] [1:a:0] concat=n=' + num_clips + ':v=1:a=1 [v] [a]" -map "[v]" -map "[a]" ' + output_vid_path + ' -y'
    print('cmd: ', cmd)#`````````````````````````````````````````````````````````````````````````````````````````````````
  
    subprocess.call(cmd,shell=True) 


#     vid_filenames_to_compile = [f for f in listdir(clips_dir_path) if isfile(join(clips_dir_path, f))]
#     clip_list = []
#     for vid_filename in vid_filenames_to_compile:
#         clip = VideoFileClip(clips_dir_path + '/' + vid_filename)
#         clip_list.append(clip)
# #         clip.reader.close()
# #         clip.audio.reader.close_proc()
#     
#     final_clip = concatenate_videoclips(clip_list, method='compose')
#     final_clip.write_videofile(output_vid_path) 



#     compile_progress_clip_path        = clips_dir_path + '/prog/' + 'A.mp4'
#     temp_compile_progress_clip_path   = clips_dir_path + '/' + 'temp_prog.mp4'
#     compile_progress_clip_backup_path = clips_dir_path + '/temp_prog'# + 'A_backup.mp4'
#     vid_filenames_to_compile = [f for f in listdir(clips_dir_path) if isfile(join(clips_dir_path, f))]
#     cnt = 0# just for testing !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# 
#     while(len(vid_filenames_to_compile) > 1):
#         cnt += 1 # just for testing !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#         
# 
#         
#         
#         if os.path.isfile(compile_progress_clip_path):
#             clip_1_path = compile_progress_clip_path
#         else:
#             clip_1_path = clips_dir_path + '/' + vid_filenames_to_compile[0]
#         clip_2_path = clips_dir_path + '/' + vid_filenames_to_compile[1]
#         input_files_str = ' -i ' + clip_1_path + ' -i ' + clip_2_path
#         
#         
# #         input_files_str = ''
# #         for vid_filename in vid_filenames_to_compile[0:2]:
# #             vid_file_path = clips_dir_path + '/' + vid_filename 
# #             input_files_str += ' -i ' + vid_file_path
#             
#         print('input_files_str: ', input_files_str)
#              
# #         cmd = 'ffmpeg ' + input_files_str + ' -filter_complex "[0:v:0] [0:a:0] [1:v:0] [1:a:0] concat=n=2:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" ' + output_vid_path + ' -y'
#         cmd = 'ffmpeg ' + input_files_str + ' -filter_complex "[0:v:0] [0:a:0] [1:v:0] [1:a:0] concat=n=2:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" ' + 'temp.mp4' + ' -y'
#        
# #         print('sleeping...')
# #         time.sleep(5)
#         print('cmd: ', cmd)#````````````````````````````````````````````````````````````````````````````````````````````````````````````````
#         subprocess.call(cmd,shell=True) 
#         
#         file_system_utils.delete_if_exists(compile_progress_clip_path)
#         os.rename('temp.mp4', compile_progress_clip_path)
#         
#           
# #         for vid_filename in vid_filenames_to_compile[0:2]:
# #             vid_path = clips_dir_path + '/' + vid_filename
# #             if vid_path != compile_progress_clip_path: 
# #                 os.remove(vid_path)
# 
#         if clip_1_path != compile_progress_clip_path:
#             os.remove(clip_1_path)
#         os.remove(clip_2_path)
# 
# 
#   
#         vid_filenames_to_compile = [f for f in listdir(clips_dir_path) if isfile(join(clips_dir_path, f))]
#         
#         #copy the currently working vid so far just in case something goes wrong
# #         file_system_utils.copy_files_to_dest([compile_progress_clip_path], compile_progress_clip_backup_path + str(cnt))
#           
#     os.rename(compile_progress_clip_path, output_vid_path)








    
#     compile_progress_clip_path = clips_dir_path + '/' + 'A.mp4'
#     vid_filenames_to_compile = [f for f in listdir(clips_dir_path) if isfile(join(clips_dir_path, f))]
#     cnt = 0# just for testing !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#     while(len(vid_filenames_to_compile) > 1):
#         cnt += 1 # just for testing !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#         clip_0 = VideoFileClip(clips_dir_path + '/' + vid_filenames_to_compile[0])
#         clip_1 = VideoFileClip(clips_dir_path + '/' + vid_filenames_to_compile[1])
#           
#         final_clip = concatenate_videoclips([clip_0, clip_1], method='compose')
#         final_clip.write_videofile(compile_progress_clip_path) 
#          
#         clip_0.reader.close()
#         clip_0.audio.reader.close_proc()
#         clip_1.reader.close()
#         clip_1.audio.reader.close_proc()
#          
#         for vid_filename in vid_filenames_to_compile[0:2]:
#             vid_path = clips_dir_path + '/' + vid_filename
#             if vid_path != compile_progress_clip_path: 
#                 os.remove(vid_path)
#  
#         vid_filenames_to_compile = [f for f in listdir(clips_dir_path) if isfile(join(clips_dir_path, f))]
#          
#     os.rename(compile_progress_clip_path, output_vid_path)
         
#     compile_progress_vid_file_path = 'compile_progress.mp4'

    print('done with compile')
    
    

    
    
def compile_clips(clip_path_list, output_file_path, prog_widget_d = None):
    c_start = time.time()
    
    if prog_widget_d != None:
        prog_widget_d['lbl_frm'].grid(column=1, row=40)
    
#     print('in compile, about to comile these clips:  ', clip_path_list)
    print('copying accepted clips to new dir: ' + CLIPS_TO_COMPILE_DIR_PATH + ' ...')
    file_system_utils.copy_files_to_dest(clip_path_list, CLIPS_TO_COMPILE_DIR_PATH)
    
    print('resizing clips in dir...')
    if prog_widget_d != None:
        prog_widget_d['resize_pb'].start(10)
    
    tallest_vid_height = get_height_of_tallest_vid_in_dir(CLIPS_TO_COMPILE_DIR_PATH)
    output_vid_dims = smallest_working_dims(tallest_vid_height)
    resize_all_vids_in_dir(output_vid_dims, CLIPS_TO_COMPILE_DIR_PATH)
    
    print('resize complete, total time: ', time.time() - c_start)
    
    print('compiling all clips in:  ', clip_path_list)
    compile_all_clips_in_dir(CLIPS_TO_COMPILE_DIR_PATH, output_file_path)
    
    print('compile complete, total time: ', time.time() - c_start)
    
    
# resize_all_vids_in_dir(1080, VIDS_TO_COMPILE_FOLDER_PATH)
if __name__ == '__main__':
    start_time = time.time()
    print('in compile main!!!!!!!!!!!!')
#     compile_all_clips_in_dir('C:/Users/Brandon/Documents/Personal_Projects/reddit_comp/old', 'tttest_output.mp4' ) # OUTPUT_VID_FILE_PATH
    file_path_l = ['C:/Users/Brandon/Documents/Personal_Projects/reddit_comp/current_data/downloaded_clips/post_0001.mp4',
                   'C:/Users/Brandon/Documents/Personal_Projects/reddit_comp/current_data/downloaded_clips/post_0007.mp4']
#     compile_clips(file_path_l, 'test_output.mp4')
#     file_system_utils.copy_files_to_dest(file_path_l, 'current_data/test_copy')
#     resize_vid(file_path_l[1], 640)
#     resize_all_vids_in_dir(720, CLIPS_TO_COMPILE_DIR_PATH)

    clips_dir_path = 'C:/Users/Brandon/Documents/Personal_Projects/vid_m_comp_big_data/vids'
#     tallest_vid_height = get_height_of_tallest_vid_in_dir(clips_dir_path)
#     print('tallest_vid_height: ', tallest_vid_height)
#     output_vid_dims = smallest_working_dims(tallest_vid_height)
#     print('in comile main test, about to resize all vids in dir to dims: ', output_vid_dims)
#     resize_all_vids_in_dir(output_vid_dims, clips_dir_path)


    compile_all_clips_in_dir(clips_dir_path, clips_dir_path + '/big_vid.mp4')
    print('Test Compile Time: ', time.time() - start_time)


    print('done')



