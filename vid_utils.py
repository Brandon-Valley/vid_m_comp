from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip




def trim_vid(in_vid_path, out_vid_path, time_tup):
    ffmpeg_extract_subclip(in_vid_path, time_tup[0], time_tup[1], targetname=out_vid_path)
    






if __name__ == "__main__":
    in_vid_path = "C:\\Users\\Brandon\\Documents\\Personal_Projects\\vid_m_comp_big_data\\vids\\post_0011.mp4"
    out_vid_path = "C:\\Users\\Brandon\\Documents\\Personal_Projects\\vid_m_comp_big_data\\vids\\post_0011_trimmed.mp4"
    time_tup = (1,4)
    trim_vid(in_vid_path, out_vid_path, time_tup)
