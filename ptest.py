from moviepy.video.io.VideoFileClip import VideoFileClip


in_vid_path = "C:\\Users\\Brandon\\Documents\\Personal_Projects\\vid_m_comp_big_data\\current_data\\downloaded_clips\\post_0010.mp4"
out_vid_path = "C:\\Users\\Brandon\\Documents\\Personal_Projects\\vid_m_comp_big_data\\vids\\post_0010__trimmed.mp4"
# time_tup = (10,17)



# input_video_path = 'myPath/vid1.mp4'
# output_video_path = 'myPath/output/vid1.mp4'

with VideoFileClip(in_vid_path) as video:
    new = video.subclip(10,17)
    new.write_videofile(out_vid_path, audio_codec='aac')
    
    
    
    
    

#     trim_vid(in_vid_path, out_vid_path, time_tup)