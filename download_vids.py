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







#                                             Starting on post_info_d #:  23   title: They did it again...
#                                             Trying to download youtube video...
#                                             in new while statement...
#                                             Getting clip duration...
# b'36\n'
#                                               Attempting Download...
#  in dl utils downloading yt vid to :  C:/Users/Brandon/Documents/Personal_Projects/vid_m_comp_big_data/current_data/downloaded_clips/post_0023.mp4
# cmd:  youtube-dl -f best "https://m.youtube.com/watch?v=GHR5o5q87M4" -o C:/Users/Brandon/Documents/Personal_Projects/vid_m_comp_big_data/current_data/downloaded_clips/post_0023.mp4
# [youtube] GHR5o5q87M4: Downloading webpage
# [youtube] GHR5o5q87M4: Downloading video info webpage
# [youtube] GHR5o5q87M4: Downloading js player vflWp5u5m
# ERROR: Signature extraction failed: Traceback (most recent call last):
#   File "C:\Users\Brandon\AppData\Local\Programs\Python\Python35-32\lib\site-packages\youtube_dl\extractor\youtube.py", line 1342, in _decrypt_signature
#     video_id, player_url, s
#   File "C:\Users\Brandon\AppData\Local\Programs\Python\Python35-32\lib\site-packages\youtube_dl\extractor\youtube.py", line 1250, in _extract_signature_function
#     res = self._parse_sig_js(code)
#   File "C:\Users\Brandon\AppData\Local\Programs\Python\Python35-32\lib\site-packages\youtube_dl\extractor\youtube.py", line 1314, in _parse_sig_js
#     jscode, 'Initial JS player signature function name', group='sig')
#   File "C:\Users\Brandon\AppData\Local\Programs\Python\Python35-32\lib\site-packages\youtube_dl\extractor\common.py", line 1004, in _search_regex
#     raise RegexNotFoundError('Unable to extract %s' % _name)
# youtube_dl.utils.RegexNotFoundError: Unable to extract Initial JS player signature function name; please report this issue on https://yt-dl.org/bug . Make sure you are using the latest version; see  https://yt-dl.org/update  on how to update. Be sure to call youtube-dl with the --verbose flag and include its complete output.
#  (caused by RegexNotFoundError('Unable to extract Initial JS player signature function name; please report this issue on https://yt-dl.org/bug . Make sure you 



# ERROR: unable to download video data: <urlopen error [WinError 10060] A connection attempt failed because the connected party did not properly respond after 










# 
#                                             Starting on post_info_d #:  43   title: mexican kids roast black people in YouTube response video...
#                                             Trying to download youtube video...
#                                             in new while statement...
#                                             Getting clip duration...
# WARNING: Unable to extract video title
# ERROR: This video has been removed for violating YouTube's Terms of Service.
# Traceback (most recent call last):
#   File "C:\Users\Brandon\Documents\Personal_Projects\vid_m_comp\dl_utils.py", line 294, in <module>
#     download_vids.test()
#   File "C:\Users\Brandon\Documents\Personal_Projects\vid_m_comp\download_vids.py", line 238, in test
#     check_clip_duration_after_download = True
#   File "C:\Users\Brandon\Documents\Personal_Projects\vid_m_comp\download_vids.py", line 156, in download_vids
#     
#   File "C:\Users\Brandon\Documents\Personal_Projects\vid_m_comp\dl_utils.py", line 91, in get_vid_duration__youtube
#     dur_time_b = subprocess.check_output(cmd, shell=True)
#   File "C:\Users\Brandon\AppData\Local\Programs\Python\Python35-32\lib\subprocess.py", line 626, in check_output
#     **kwargs).stdout
#   File "C:\Users\Brandon\AppData\Local\Programs\Python\Python35-32\lib\subprocess.py", line 708, in run
#     output=stdout, stderr=stderr)
# subprocess.CalledProcessError: Command 'youtube-dl --get-duration "https://youtu.be/FKhGwLTmYj4"' returned non-zero exit status 1


















from selenium import webdriver
import youtube_dl #need for error detection
import time
import os
import pytube

# just for exception handling
import subprocess 
import prawcore
# import RegexNotFoundError

import file_system_utils
import get_post_info_dl
import dl_utils
import historical_data
import project_vars_handler
import custom_errors

import testing_utils
# from test.test_optparse import _check_duration
# from distutils.command.check import check

# PHANTOM_JS_PATH = 'C:/Users/Brandon/Downloads/phantomjs-2.1.1-windows/phantomjs-2.1.1-windows/bin/phantomjs.exe' ## SET YOU PATH TO phantomjs

class NoInternetError(Exception):
    pass

NO_INTERNET_YT_STR = b"ERROR: Unable to download webpage: <urlopen error [Errno 11001] getaddrinfo failed> (caused by URLError(gaierror(11001, 'getaddrinfo failed'),))\n"

# VIDS_TO_COMPILE_FOLDER_PATH = 'vids_to_compile'
CURRENT_DATA_DIR_PATH = project_vars_handler.get_var('current_data_dir_path')
DOWNLOADED_CLIPS_DIR_PATH = CURRENT_DATA_DIR_PATH + '/downloaded_clips'

MAX_CLIP_DURATION = 45 # seconds

INDENT = '                                            '

UN_BEATABLE_ERROR_STRINGS = ['ERROR: requested format not available',
                             'ERROR: No video formats found; please report',
                             'ERROR: Unable to download webpage: HTTP Error 404: Not Found']




def download_vids(num_posts, subreddit_list, dl_type = 'overwrite',QUICK_TEST = False, continue_from_last_pos = False, include_youtube_downloads = True, start_from_pos = None):
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



    print(INDENT + 'Getting starting pos...')
    start_pos = dl_utils.start_pos(start_from_pos, continue_from_last_pos)


    if dl_type == 'overwrite':
        print(INDENT + 'Deleting all files in %s...' %(DOWNLOADED_CLIPS_DIR_PATH))
        file_system_utils.delete_all_files_in_dir(DOWNLOADED_CLIPS_DIR_PATH)
        print(INDENT + 'Deleting pool_clips_data.csv and download_log.csv')
        file_system_utils.delete_if_exists(CURRENT_DATA_DIR_PATH + '/pool_clips_data.csv')
        file_system_utils.delete_if_exists(CURRENT_DATA_DIR_PATH + '/download_log.csv')
        
        
    print(INDENT + 'Getting list of previously evaluated postIds...')
    evaluated_post_id_l = historical_data.get_evaluated_post_id_l()
        
    print(INDENT + 'Getting dict list of saved, previously non-evaluated clips...')
    non_eval_clip_data_d = historical_data.get_non_eval_clip_data_d()


    for post_num, post_info_d in enumerate(post_info_dl[start_pos:]): 
        post_num += start_pos        
        while(True):
            try:
                fail_reason = None
                dl_start_time = time.time() 


                testing_utils.print_str_wo_error('\n' + INDENT + "Starting on post_info_d #:  %s   title: %s    url: %s ..." %(post_num, post_info_d['postTitle'], post_info_d['postURL']))
         
                vid_save_title =  dl_utils.make_vid_save_name(post_num)#'f_' + str(post_num) + '/' +
                vid_save_path = DOWNLOADED_CLIPS_DIR_PATH + '/' + vid_save_title + '.mp4'
                clip_duration = 0
                
                
                if post_info_d['postId'] in evaluated_post_id_l:
                    print(INDENT + 'This postId has been previously evaluated, skipping...')
                    fail_reason = 'prev_eval'
                
                # if vid has previously been downloaded but not evaluated and was saved,
                # just rename it from where it is saved instead of re-downloading
                elif post_info_d['postId'] in non_eval_clip_data_d.keys():
                    print(INDENT + 'Pulling from previously download...  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                    historical_data.pull_clip(non_eval_clip_data_d[post_info_d['postId']], vid_save_path)
                    clip_duration = dl_utils.get_vid_length(vid_save_path)
                
                # keep track of how often this happens, not dealing with it now b/c it seems like too much hassle
                elif post_info_d['postType'] == 'self':
                    print(INDENT + "post_info_d['postType'] == self, skipping... <-- ASSUMING THIS DOSNT HAPPEN MUCH, IF YOU SEE THIS MESSAGE TOO OFTEN, FIX THIS")
                    fail_reason = 'postType==self'
                
                
                # youtube video
                elif post_info_d['postType'] == None:
                    if not include_youtube_downloads:
                        print(INDENT + 'Youtube video, include_youtube_downloads == False so skipping...')
                        fail_reason ='incude_youtube_downloads==False'
                    else:
                        print(INDENT + '  Trying to download youtube video...')
        
                        # try to get clip duration
                        print(INDENT + '    Getting clip duration...')
                        clip_duration = False
                        try:
                            clip_duration = dl_utils.get_vid_duration__youtube(post_info_d['postURL'])
                        except ValueError as e:
                            print(e)
                            fail_reason ='error: value error: ' + str(e)
                        except subprocess.CalledProcessError as e:
                            if e.output == NO_INTERNET_YT_STR:
                                raise NoInternetError('ERROR:  No internet connection')
                            else:
                                print("Status : FAIL",  e.output)#`````````````````````````````````````````````````````````````````````````
                                
                                print(INDENT + 'Video not available, possably removed, skipping...')
                                fail_reason = 'error: youtube video unavailable, possably removed -- subprocess.CalledProcessError'
                        except custom_errors.NotYoutubeVideoError:
                            print(INDENT + 'not a youtube vid, skipping...')
                            fail_reason = 'error: url_not_youtube_vid'
#                         except RegexNotFoundError:
#                             print(INDENT + 'RegexNotFoundError on youtube vid, MIGHT be possable to fix, keep an eye on how often this happens')
#                             fail_reason = 'error: RegexNotFoundError' #vid is available, MIGHT be able to fix later, one time vid had title with weird chars but not always
                        
                        
                        
                        # download youtube video if clip duration was obtained and is less than MAX_CLIP_DURATION
                        if clip_duration != False:
                            if clip_duration < MAX_CLIP_DURATION:
                                print(INDENT + '  Attempting Download...')
                                dl_utils.download_youtube_vid(post_info_d['postURL'], vid_save_path)
                            else:
                                print(INDENT + '  Clip too long!  Moving on to next clip...')
                                fail_reason = 'clip_too_long'
        
                # embedded reddit video
                elif post_info_d['postType'] == 'direct':
        #             print('ONLY TESTING YOUTUBE VIDS< THIS IS A REDDIT VID BREAKING NOW!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')#````````````
        #             continue#`````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
        #             
                    
                    
                    print(INDENT + 'Trying to download reddit video...')
                    print(INDENT + 'Sleeping...')
                    time.sleep(1)
                    while True:
                        try:
                            #try to get vid duration
                            print(INDENT + 'Trying to get clip duration...')
                            check_clip_duration_after_download = False
                            clip_duration = dl_utils.get_vid_duration__reddit(post_info_d['postId'])
                            
                            if clip_duration == False:
                                check_clip_duration_after_download = True
                            elif clip_duration > MAX_CLIP_DURATION:
                                fail_reason = 'clip_too_long'
                                break
                            
        #                     if dl_utils.get_clip_duration__reddit(post_info_d['postID']) < MAX_CLIP_DURATION:
                            dl_utils.download_reddit_vid(post_info_d['postURL'], DOWNLOADED_CLIPS_DIR_PATH, vid_save_title)
                           
                            # delete video if its too long
                            if check_clip_duration_after_download == True:
                                clip_duration = dl_utils.get_vid_length(vid_save_path)
                                if clip_duration > MAX_CLIP_DURATION:
                                    print('  Video too long, deleting video...')
                                    os.remove(vid_save_path)
                                    fail_reason = 'clip_too_long'
                            break                   
                        
                        except (youtube_dl.utils.DownloadError, OSError) as e:
                            if dl_utils.str_from_list_in_error_msg(UN_BEATABLE_ERROR_STRINGS, e):
                                print(INDENT + 'Hit un-beatable error skipping clip...')
                                fail_reason = 'error: reddit: un-beatable error'
                            else:
                                dl_utils.correct_failed_vid_audio_combine(DOWNLOADED_CLIPS_DIR_PATH, vid_save_title)
                            break
                break
            except (NoInternetError, prawcore.exceptions.RequestException) as e:
                print(INDENT + 'No internet connection, sleeping then trying again...')
                time.sleep(1)
                        
                
                    
        # log all data from this attepted download, even if it was not a success
        print(INDENT + 'logging attempted download...')
        dl_time = time.time() - dl_start_time
        print(INDENT + '          Download attept time: ', dl_time)
        dl_utils.log_attempted_download(vid_save_path, post_info_d, clip_duration, dl_time, fail_reason)

        

def test():
    download_vids(500, ['dankvideos'], 'append', QUICK_TEST = True, continue_from_last_pos=True, include_youtube_downloads=True, start_from_pos = None)    
           
if __name__ == '__main__':
    test()
    print('done!')
    
    