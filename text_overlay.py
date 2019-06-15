# from PIL import Image
#  
# img = Image.new('RGB', (2000, 2000), color = (0,255,0))
# img.save('green.png')



# import moviepy.editor as mp
import cv2
from PIL import Image
import os

import meme_caption

BACKGROUND_COLOR = (0,255,0)

def make_background_transparent_img(in_img_path, out_img_path, bgnd_clr):
    img = Image.open(in_img_path)
    img = img.convert("RGBA")
    datas = img.getdata()
    
    newData = []
    for item in datas:
        if item[0] == bgnd_clr[0] and item[1] == bgnd_clr[1] and item[2] == bgnd_clr[2]:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    
    img.putdata(newData)
    img.save(out_img_path, "PNG")


def make_solid_color_img(dims, color, out_file_path):
    img = Image.new('RGB', dims, color)
    img.save(out_file_path)

def make_transparent_text_img(top_text, bottom_text, dims, output_file_path):
    make_solid_color_img(dims, BACKGROUND_COLOR, 't.png')
    make_background_transparent_img('t.png','t2.png', BACKGROUND_COLOR)

    meme_caption.add_caption('t2.png', output_file_path, top_text, bottom_text)
#     make_background_transparent_img('t2.png', output_file_path, BACKGROUND_COLOR)
    os.remove('t.png')
    os.remove('t2.png')


def get_int_vid_dims(vid_file_path):
    vid = cv2.VideoCapture(vid_file_path)
    vid_w_float, vid_h_float = vid.get(cv2.CAP_PROP_FRAME_WIDTH), vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    return(int(vid_w_float), int(vid_h_float))


def text_overlay(top_text, bottom_text, vid_file_path, output_vid_file_path):
    import moviepy.editor as mp # this here so long load and print dosnt happen when open gui
    vid_dims = get_int_vid_dims(vid_file_path)
    
#     print('vid_dims:  ', vid_dims)
    
    # make img with text that will be overlayed on video -- same dims as video
    make_transparent_text_img(top_text, bottom_text, vid_dims, 'text.png')
#     text_img = Image.open('text.png')
    
    video = mp.VideoFileClip(vid_file_path)
    og_vid_duration = video.duration

    text_img_overlay = (mp.ImageClip('text.png')
                          .set_duration(video.duration)
                #           .resize(height=0) # if you need to resize...
                          .margin(right=0, top=0, opacity=0) # (optional) logo-border padding
                        .set_pos(("center","center")))
    
    final = mp.CompositeVideoClip([video, text_img_overlay])
    final.write_videofile(output_vid_file_path)
    
    video.reader.close()
    video.audio.reader.close_proc()

# meme_caption.add_caption('green.png', 't.png', 'THIS is SomE TexT', 'bopoooooooottom')
# text_overlay('tooooooooop teeeeeeext', 'booooooottommmm tesssssssefsfdf', 'i.mp4', 'o.mp4')
# vid_h =