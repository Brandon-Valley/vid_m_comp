import subprocess
import os
import time # just for testing 
import psutil

print('in vid_player_control, done with imports') #``````````````````````````````````````````````````````````

# VVVVV Internal VVVVV

def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;


# VVVVV External VVVVV

def open_vid(vid_file_path):
    print('in vid player, open, vid_file_path: ', vid_file_path)#````````````````````````````````````````````````````
    absolute_path = os.path.abspath(vid_file_path)
    subprocess.call(absolute_path,shell=True)
    

def close_vid_if_open():
    if checkIfProcessRunning('Video.UI.exe'):
        subprocess.call('taskkill /im Video.UI.exe /F',shell=True)
    
# open_vid('old/post_0001.mp4')
# time.sleep(5)
# close_vid_if_open()