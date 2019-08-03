from moviepy.tools import subprocess_call
from moviepy.config import get_setting
import os

def ffmpeg_extract_subclip(filename, t1, t2, targetname=None):
    """ Makes a new video file playing video file ``filename`` between
    the times ``t1`` and ``t2``. """
    print('in ffmpeg_extract_subclip')#```````````````````````````````````````````````````````````````````
    name, ext = os.path.splitext(filename)
    if not targetname:
        T1, T2 = [int(1000*t) for t in [t1, t2]]
        targetname = "%sSUB%d_%d.%s" % (name, T1, T2, ext)

    cmd = [get_setting("FFMPEG_BINARY"),"-y",
           "-ss", "%0.2f"%t1,
           "-i", filename,
           "-t", "%0.2f"%(t2-t1),
           "-vcodec", "copy", "-acodec", "copy", targetname]
    subprocess_call(cmd)
    
    
    
    
    
def trim_vid(in_vid_path, out_vid_path, time_tup):
    ffmpeg_extract_subclip(in_vid_path, time_tup[0], time_tup[1], targetname=out_vid_path)
    






if __name__ == "__main__":
    in_vid_path = "C:\\Users\\Brandon\\Documents\\Personal_Projects\\vid_m_comp_big_data\\current_data\\downloaded_clips\\post_0010.mp4"
    out_vid_path = "C:\\Users\\Brandon\\Documents\\Personal_Projects\\vid_m_comp_big_data\\vids\\post_0010__trimmed.mp4"
    time_tup = (10,16)
    trim_vid(in_vid_path, out_vid_path, time_tup)
