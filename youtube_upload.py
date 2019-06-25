import subprocess


# 
# API_KEY = 'AIzaSyATOtqcASYH3wjVPZwm5c__953LAWajVQE'
# 
# id = '988531244418-jmn22hr6fsghvdas6ldl7n5sc657lbo8.apps.googleusercontent.com'
# 
# secret = 'AcF4ovus31s5Qs5rjz-8AWte'
# 
# "C:\Users\Brandon\Documents\Personal_Projects\vid_m_comp_big_data\current_data\downloaded_clips\post_0004.mp4"
# 
# python upload_video.py --file="C:\Users\Brandon\Documents\Personal_Projects\vid_m_comp_big_data\current_data\downloaded_clips\post_0004.mp4" --title="auto_test_upload" --description="AUTO_upload_TEST" --keywords="Memes, GTA" --category="22" --privacyStatus="private"
# 
# 
# python upload_thumbnail.py --video-id=TienN2RYmQw --file="C:\Users\Brandon\Downloads\Untitled Design (1).png"



#  https://studio.youtube.com/channel/UC3cuK7299GycX8OMbpjSFqQ/videos/upload?filter=%5B%5D&sort=%7B"columnType"%3A"date"%2C"sortOrder"%3A"DESCENDING"%7D
def get_video_id_from_output(output):
#     split_output_str_l = str(output).split()
    return str(output)[33:-33]


def youtube_upload(vid_file_path, title, description, keywords, category, privacy_status, thumbnail_pic_path):
    vid_upload_cmd  = 'python upload_video.py'
    vid_upload_cmd += ' --file='          + vid_file_path 
    vid_upload_cmd += ' --title='         + title 
    vid_upload_cmd += ' --description='   + description 
    vid_upload_cmd += ' --keywords='      + keywords 
    vid_upload_cmd += ' --category='      + category 
    vid_upload_cmd += ' --privacyStatus=' + privacy_status 
    
    print('IN YOUTUBE_UPLOAD, testing, commented out actual upload code, put back in !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')#`````````````````````  
    print(vid_upload_cmd)
    
#     output = subprocess.check_output(vid_upload_cmd, stderr=subprocess.STDOUT, shell=True)
#     print(output)
#     vid_id = get_video_id_from_output(output)
#     print(vid_id)
#     
#     thumbnail_upload_cmd  = 'python upload_thumbnail.py'
#     thumbnail_upload_cmd += ' --video-id=' + vid_id
#     thumbnail_upload_cmd += ' --file='     + thumbnail_pic_path
#     
#     print(thumbnail_upload_cmd)
#     
#     subprocess.call(thumbnail_upload_cmd,shell=True)

    
    
    
    
    
if __name__ == '__main__':
    vid_file_path = "C:\\Users\\Brandon\\Documents\\Personal_Projects\\vid_m_comp_big_data\\current_data\\downloaded_clips\\post_0004.mp4"
    title="auto_test_upload2"
    description="AUTO_upload_TEST"
    keywords='"Memes, GTA"'
    category="22"
    privacy_status="private"
    thumbnail_pic_path='"C:\\Users\\Brandon\\Downloads\\Untitled Design (1).png"'
    youtube_upload(vid_file_path, title, description, keywords, category, privacy_status, thumbnail_pic_path)
    
    
#     print(get_video_id_from_output(b"Uploading file...\r\nVideo id 'HdZi9zGZrMQ' was successfully uploaded.\r\n"))
    
    
    
