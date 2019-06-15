import praw,requests,re
import os
import shutil
import youtube_dl
import subprocess

# from selenium import webdriver

import requests
import time
from pytube import YouTube
from moviepy.editor import VideoFileClip
from wx.lib.agw.flatmenu import GetMRUEntryLabel

import file_system_utils
import credentials
import logger
import pool_clips_data_handler
import project_vars_handler

CLIP_DOWNLOAD_LOG_CSV_HEADER_LIST = ['download_success', 'download_time', 'save_name', 'duration', 'postId', 'postTitle', 'postSubmitter', 'postType', 'postURL', 'postSubreddit', 'postContent']
CLIP_DOWNLOAD_LOG_CSV_PATH = project_vars_handler.get_var('current_data_dir_path') + '/download_log.csv'# 'current_data/download_log.csv'


# VVVVV Internal VVVVV
def get_filename_from_path(file_path):
    return file_path.split('/')[-1]

#trim out the chars that will make tinker poop itself when it trys to put str in widget
def trim_bad_tk_chars(str):
    char_list = [str[j] for j in range(len(str)) if ord(str[j]) in range(65536)]
    out_str=''
    for j in char_list:
        out_str=out_str+j
#     print('FIX TRIM_BAD_TK_CHARS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
#     out_str = str
    return out_str
    

# VVVVV External VVVVV






# 
# def get_text_from_url(url):
#     time.sleep(10)
#     response = requests.get(url)
#     return response.text

def get_vid_length(filename):
#     result = subprocess.Popen(["ffprobe", filename],
#     stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
#     print(stdout)#211111``````````````````````````````````````````````````````````````````````````````````````````````
#     return [x for x in result.stdout.readlines() if "Duration" in x]

    clip = VideoFileClip(filename)
    duration = clip.duration 
    clip.reader.close()
    clip.audio.reader.close_proc()
    return int(duration)


# '1:36' -->  96
def time_str_to_total_seconds(time_str):
    time_str = duration_str.split(':')
    seconds = int( duration_split_str[1])
    minutes = int( duration_split_str[0])
    
    total_seconds = seconds + (minutes * 60)
    return total_seconds
    

def get_vid_duration__reddit(post_id):
        post = credentials.reddit.submission(id=post_id, url=None)
#         print('                                                        POST>MEDIA:  ', post.media)#````````````````````````````````````````````````````````````````````````````````````````````````
#         duration = int(post.media['reddit_video']['duration'])
        if post.media == None:
            return False
        return int(post.media['reddit_video']['duration'])

 
def get_vid_duration__youtube(post_info_d):
        myVideo = YouTube(post_info_d['postURL'])
        return int(myVideo.length) 
 

# # trys to return length of video in seconds, returns false if it cant tell
# def get_vid_duration(post_info_d):
#     
#     # youtube
#     if   post_info_d['postType'] == None:
#         myVideo = YouTube(post_info_d['postURL'])
#         return myVideo.length 
#     # reddit embedded 
#     elif post_info_d['postType'] == 'direct':
#         post = credentials.reddit.submission(id=post_info_d['postId'], url=None)
#         return post.media['reddit_video']['duration']
#     else:
#         raise ValueError('ERROR:  Dont know how to get duration of this --> post_info_d:  ', post_info_d)

        
        
def make_vid_save_name(post_num):
    num_zeros_to_add = 4 - len(str(post_num))
    return 'post_' + ('0' * num_zeros_to_add) + str(post_num)
        
        
def correct_failed_vid_audio_combine(save_dir_path, vid_save_title):
    print('in correct_failed_vid_audio_combine !!!!!!!!!!!!!!!!!!!!!!!!!!!!! ')#```````````````````````````````````````````
    full_vid_temp_save_path = save_dir_path + '/temp/' + vid_save_title + '.mp4'
    
    #check if it downloaded correctly by checking if correct file exists,
    #if it does, move it to correct folder, if not, combine, then move
#     if os.path.isfile(full_vid_temp_save_path) == False:
    vid_file_path    = save_dir_path + '/temp/' + vid_save_title + '.fhls-955.mp4'
    audio_file_path  = save_dir_path + '/temp/' + vid_save_title + '.fdash-AUDIO-1.m4a'
    output_file_path = save_dir_path + '/'      + vid_save_title + '.mp4'

    cmd = "ffmpeg -i " + vid_file_path + " -i " + audio_file_path + " -c copy " + output_file_path
    subprocess.call(cmd, shell=True)
        
    # move final video file to correct dir and delete temp folder
#     os.rename(full_vid_temp_save_path, save_dir_path + '/' + vid_save_title + '.mp4')
#     shutil.rmtree(save_dir_path + '/temp') # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    TOOK THIS  OUT TO FIX FILE NOT FOUND ERROR< MIGHT NEED !!!!!!!!!!

# downloads yt vid at highest resolution
def download_youtube_vid(videourl, path, save_title):
 
    yt = YouTube(videourl)
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    if not os.path.exists(path):
        os.makedirs(path)
    yt.download(path)
     
    print('in dl_utils, finding newest file_path...')#`````````````````````````````````````````````````````````````````````````````
    # rename saved video
    newest_file_path = file_system_utils.get_newest_file_path(path)
    print('in dl_utils, renameing...')#`````````````````````````````````````````````````````````````````````````````
    os.rename(newest_file_path, path + '//' + save_title + '.mp4')
# downloadYouTube('https://www.youtube.com/watch?v=zNyYDHCg06c', './videos/FindingNemo1')


def download_reddit_vid(video_url, save_dir_path, vid_save_title):

   # see options at https://github.com/rg3/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L89
    ydl_opts = {'outtmpl': save_dir_path + '/temp/' + vid_save_title + '.%(ext)s',
                'socket-timeout': 20,
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]'}
#                 'format':'137'} <------------------------------------------------------------------- this is what is making stuff fail, need to find a way to always use the highest resolution available
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url, ])
    

    try:
        # move final video file to correct dir and delete temp folder
        full_vid_temp_save_path = save_dir_path + '/temp/' + vid_save_title + '.mp4'
        os.rename(full_vid_temp_save_path, save_dir_path + '/' + vid_save_title + '.mp4')
        os.rmdir(save_dir_path + '/temp')
    except OSError:
        correct_failed_vid_audio_combine(save_dir_path, vid_save_title)
    
    
def log_to_clip_pool_csv(clip_save_path, post_info_d, clip_duration):
    print('                                                                                   logging to clip pool!!!!!!!!!!!!!!!!!!!!!')#1111`````
    row_d = {}
    for key, val in post_info_d.items():
        row_d[key] = val
    
    row_d['duration'] = clip_duration
    row_d['top_text'] = trim_bad_tk_chars(post_info_d['postTitle'])
    row_d['clip_path'] = os.path.abspath(clip_save_path)
    row_d['title'] = trim_bad_tk_chars(post_info_d['postTitle'])
    
    pool_clips_data_handler.add_to_clip_pool(row_d)
    
    

def log_attempted_download(clip_save_path, post_info_d, clip_duration, dl_time):
    # check if download was a success
    dl_success = False
    if os.path.isfile(clip_save_path):
        dl_success = True
        log_to_clip_pool_csv(clip_save_path, post_info_d, clip_duration)
        
    row_d = {}
    row_d['download_success'] = dl_success
    row_d['save_name'] = get_filename_from_path(clip_save_path)
    row_d['duration'] = clip_duration
    row_d['download_time'] = dl_time
    for key, val in post_info_d.items():
        row_d[key] = val
        
    logger.logSingle(row_d, CLIP_DOWNLOAD_LOG_CSV_PATH, True, CLIP_DOWNLOAD_LOG_CSV_HEADER_LIST)
    
    
def delete_download_log():
    if os.path.isfile(CLIP_DOWNLOAD_LOG_CSV_PATH):
        os.remove(CLIP_DOWNLOAD_LOG_CSV_PATH) 
            
def correct_youtube_vid_url(url, driver):
    driver.get(url)
    return driver.current_url

def re_install_pytube():        
    subprocess.call('pip install --upgrade --force-reinstall pytube', shell=True)
            
def wait_until_pytube_installed():
    while(True):
        try:
            import pytube
            return
        except ImportError as e:
            pass # module doesn't exist, deal with it.
        
        
        
def get_next_post_num():
    data_dl = logger.readCSV(CLIP_DOWNLOAD_LOG_CSV_PATH)
    return len(data_dl)
            
            
def get_error_message(error):
    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    return (template.format(type(error).__name__, error.args))
            
def str_from_list_in_error_msg(str_list, error):
    error_msg = get_error_message(error)
    for str in str_list:
        if str in error_msg:
            return True
    return False    


def delete_clip_pool_csv():
    csv_path = pool_clips_data_handler.POOL_CLIPS_DATA_CSV_PATH
    file_system_utils.delete_if_exists(csv_path)
    
    
def start_pos(start_from_pos, continue_from_last_pos):
    if start_from_pos == None:
        if continue_from_last_pos == True:
            starting_pos = get_next_post_num()
        else:
            starting_pos = 0
    else:
        starting_pos = start_from_pos
    return starting_pos
    
            
import download_vids
if __name__ == '__main__':
#     import pytube
    download_vids.test()
#     download_reddit_vid('https://v.redd.it/hmngsw5agv131/DASH_360', 'test', 'test_vid')
#     correct_failed_vid_audio_combine('vids_to_compile','post_0001' )
#     print(get_vid_duration__reddit("bvtsbd"))
#     download_youtube_vid('https://www.youtube.com/watch?v=nKp9d0XCrA0', 'vids', 'yt_test_dl.mp4')






