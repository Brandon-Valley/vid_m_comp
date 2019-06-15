# pip install --upgrade --force-reinstall pytube

# Video unavailable:   An exception of type KeyError occurred. Arguments:
# ('s',)

# youtube_dl.utils.DownloadError: ERROR: unable to rename file: [WinError 32] The process cannot access the file because it is being used by another process: 'vids_to_compile\\post_0051.fdash-VIDEO-1.mp4.part' -> 'vids_to_compile\\post_0051.fdash-VIDEO-1.mp4'

# Video unavailable:   An exception of type RegexMatchError occurred. Arguments:
# ('regex pattern (\\bc\\s*&&\\s*d\\.set\\([^,]+\\s*,\\s*\\([^)]*\\)\\s*\\(\\s*(?P<sig>[a-zA-Z0-9$]+)\\() had zero matches',)

#  raise RequestException(exc, args, kwargs)
# prawcore.exceptions.RequestException: error with request HTTPSConnectionPool(host='oauth.reddit.com', port=443): Max retries exceeded with url: /comments/bv8jws/?limit=2048&raw_json=1&sort=best (Caused by NewConnectionError('<urllib3.connection.VerifiedHTTPSConnection object at 0x18588A90>: Failed to establish a new connection: [Errno 11001] getaddrinfo failed',))

# raise DownloadError(message, exc_info)
# youtube_dl.utils.DownloadError: ERROR: No video formats found; please report this issue on https://yt-dl.org/bug . Make sure you are using the latest version; see  https://yt-dl.org/update  on how to update. Be sure to call youtube-dl with the --verbose flag and include its complete output.
    # causes  --->
        #    names = os.listdir(path)
        # FileNotFoundError: [WinError 3] The system cannot find the path specified: 'downloaded_clips/temp'

# youtube_dl.utils.DownloadError: ERROR: requested format not available  ----- also causes ^^^^

#178
# PermissionError: [Errno 13] Permission denied: 'C:\\Users\\Brandon\\Documents\\Personal_Projects\\reddit_comp\\current_data\\downloaded_clips\\temp\\post_0178.fhls-1235.mp4.ytdl'


from selenium import webdriver
import youtube_dl #need for error detection
import time
import os
 # "C:/Users/mt204e/Documents/other/p/reddit_comp/reddit_comp - Copy/current_data",      

import file_system_utils
import get_post_info_dl
import dl_utils
import project_vars_handler

import testing_utils
# from test.test_optparse import _check_duration
# from distutils.command.check import check

PHANTOM_JS_PATH = 'C:/Users/Brandon/Downloads/phantomjs-2.1.1-windows/phantomjs-2.1.1-windows/bin/phantomjs.exe' ## SET YOU PATH TO phantomjs

# VIDS_TO_COMPILE_FOLDER_PATH = 'vids_to_compile'
CURRENT_DATA_DIR_PATH = project_vars_handler.get_var('current_data_dir_path')
DOWNLOADED_CLIPS_DIR_PATH = CURRENT_DATA_DIR_PATH + '/downloaded_clips'

MAX_CLIP_DURATION = 45 # seconds

INDENT = '                                            '

UN_BEATABLE_ERROR_STRINGS = ['ERROR: requested format not available',
                             'ERROR: No video formats found; please report',
                             'ERROR: Unable to download webpage: HTTP Error 404: Not Found']



QUICK_TEST = True
def download_vids(num_posts, subreddit_list, dl_type = 'overwrite', continue_from_last_pos = False, include_youtube_downloads = False, start_from_pos = None):
    # add new dirs if don't already exist
    print(INDENT + 'Adding new dirs if needed...')
    file_system_utils.make_dir_if_not_exist(CURRENT_DATA_DIR_PATH)
    file_system_utils.make_dir_if_not_exist(DOWNLOADED_CLIPS_DIR_PATH)
    
    print(INDENT + 'QUICK_TEST:  ', QUICK_TEST)
    print(INDENT + 'Getting post_info_dl...')
    if QUICK_TEST == True or continue_from_last_pos == True:
        post_info_dl = get_post_info_dl.get_post_info_dl(num_posts, subreddit_list, quick_test = True)
    else:
        post_info_dl = get_post_info_dl.get_post_info_dl(num_posts, subreddit_list)


#     print('post_info_dl: ',  get_post_info_dl.get_post_info_dl(num_posts, subreddit_list))#111111```````````````````````````````````````````````````````````````````````
#     print('post_info_dl: ',  post_info_dl)#111111```````````````````````````````````````````````````````````````````````


    print(INDENT + 'Getting starting pos...')
    start_pos = dl_utils.start_pos(start_from_pos, continue_from_last_pos)


    # set up browser
    if include_youtube_downloads:
        print(INDENT + 'Setting up phanomJS browser ...')
        driver = webdriver.PhantomJS(PHANTOM_JS_PATH)



    
    if dl_type == 'overwrite':
        print(INDENT + 'Deleting all files in %s...' %(DOWNLOADED_CLIPS_DIR_PATH))
        file_system_utils.delete_all_files_in_dir(DOWNLOADED_CLIPS_DIR_PATH)
        dl_utils.delete_download_log()# just for testing !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        dl_utils.delete_clip_pool_csv()# just for testing!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    for post_num, post_info_d in enumerate(post_info_dl[start_pos:]): 
        post_num += start_pos
        
        dl_start_time = time.time()
        
        testing_utils.print_str_wo_error(INDENT + "Starting on post_info_d #:  %s   title: %s..." %(post_num, post_info_d['postTitle']))
 
        vid_save_title =  dl_utils.make_vid_save_name(post_num)#'f_' + str(post_num) + '/' +
        vid_save_path = DOWNLOADED_CLIPS_DIR_PATH + '/' + vid_save_title + '.mp4'
        clip_duration = 0
        
        # keep track of how often this happens, not dealing with it now b/c it seems like too much hassle
        if post_info_d['postType'] == 'self':
            pass
        
        # youtube video
        elif post_info_d['postType'] == None:
            if include_youtube_downloads:
                print(INDENT + 'Trying to download youtube video...')
                
                #make sure you are using the correct url
                if post_info_d['postURL'].startswith('https://youtu.be/'):
                    print(INDENT + '  Correcting URL...')
                    post_url = dl_utils.correct_youtube_vid_url(post_info_d['postURL'], driver)
                else:
                    post_url = post_info_d['postURL']
                    
    #             try:
    #                 clip_duration = dl_utils.get_vid_duration__youtube(post_info_d)
    #                 if clip_duration < MAX_CLIP_DURATION:
                        
                while(True):
                    print(INDENT + 'in new while statement...')
                    try:
                        print(INDENT + 'Getting clip duration...')
                        clip_duration = dl_utils.get_vid_duration__youtube(post_info_d)
                        if clip_duration < MAX_CLIP_DURATION:
                            print(INDENT + '  Attempting Download...')
                            dl_utils.download_youtube_vid(post_url, DOWNLOADED_CLIPS_DIR_PATH, vid_save_title)
                        else:
                            print(INDENT + '  Clip too long!  Moving on to next clip...')
    # 
    #                     print(INDENT + '  Attempting Download...')
    #                     dl_utils.download_youtube_vid(post_url, DOWNLOADED_CLIPS_DIR_PATH, vid_save_title)
    #                     print(INDENT + '    Finished Download...')
                        break
                    except KeyError as e:
                        message = dl_utils.get_error_message(e)
#                         template = "An exception of type {0} occurred. Arguments:\n{1!r}"
#                         message = template.format(type(e).__name__, e.args)
                        print(INDENT + '    Got KeyError (s), re-installing pytube and trying again, msg:  ' + message)
                        dl_utils.re_install_pytube()
                        dl_utils.wait_until_pytube_installed()
    #                     time.sleep(5) #```````````````````````````````````````````````````````````````````````````````````````````````
                    except pytube.exceptions.VideoUnavailable as e:
                        message = dl_utils.get_error_message(e)
                        print(INDENT + '    Video unavailable, moving on to next clip, msg:  ' + message)
                        
    

        # embedded reddit video
        elif post_info_d['postType'] == 'direct':
            print(INDENT + 'Trying to download reddit video...')
            print(INDENT + 'Sleeping...')
            time.sleep(1)
            while True:
                try:
                    #try to get vid duration
                    check_clip_duration_after_download = False
                    clip_duration = dl_utils.get_vid_duration__reddit(post_info_d['postId'])
                    
                    if clip_duration == False:
                        check_clip_duration_after_download = True
                    elif clip_duration > MAX_CLIP_DURATION:
                        break
                    
#                     if dl_utils.get_clip_duration__reddit(post_info_d['postID']) < MAX_CLIP_DURATION:
                    dl_utils.download_reddit_vid(post_info_d['postURL'], DOWNLOADED_CLIPS_DIR_PATH, vid_save_title)
                   
                    # delete video if its too long
                    if check_clip_duration_after_download == True:
                        clip_duration = dl_utils.get_vid_length(vid_save_path)
                        if clip_duration > MAX_CLIP_DURATION:
                            print('  Video too long, deleting video...')
                            os.remove(vid_save_path)
                    break                   
                
                except (youtube_dl.utils.DownloadError, OSError) as e:
                    if dl_utils.str_from_list_in_error_msg(UN_BEATABLE_ERROR_STRINGS, e):
                        print(INDENT + 'Hit un-beatable error skipping clip...')
                    else:
                        dl_utils.correct_failed_vid_audio_combine(DOWNLOADED_CLIPS_DIR_PATH, vid_save_title)
                    break
                
                
                    
        # log all data from this attepted download, even if it was not a success
        print(INDENT + 'logging attempted download...')
        dl_time = time.time() - dl_start_time
        print(INDENT + '          Download attept time: ', dl_time)
        dl_utils.log_attempted_download(vid_save_path, post_info_d, clip_duration, dl_time)

        

def test():
    download_vids(1000, ['dankvideos'], 'append', continue_from_last_pos=True, include_youtube_downloads=False, start_from_pos = None)    
           
if __name__ == '__main__':
    test()
    print('done!')
    
    