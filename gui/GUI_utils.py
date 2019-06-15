import re

from tkinter.colorchooser import *

# from PIL import Image, ImageDraw
import os



from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk

#from PIL import Image

from os import listdir
from os.path import isfile, join
 
# import fonts
#import font_tools
#import tools



OUTPUT_IMAGE_SUFFIX = '_text_art' #used????????????????????????????????????????????????????????????????????????????????

LBOX_STR_DELIM = '_'

def get_current_dir_path():
    import os 
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return dir_path#'sdfsfdfsfsd\sdffsdfsf'#"'C:\Users\Brandon\Documents\Personal Projects\white_paper_art\examples'"

# def get_defalt_text_file_path():
#     return 'default\text\file\path.txt'
#  
# def get_defalt_image_file_path():
#     return 'ddddd\aaaaa\file\bitcoin.jpg'

def get_defalt_file_path(home_dir_path, file_ext_list):
    valid_filenames = get_matching_filenames_list(home_dir_path, file_ext_list)
    
#     print('valid_filenames: ',valid_filenames)#`````````````````````````````````````````````````````````````````````````````````````
#     print(type(valid_filenames))#``````````````````````````````````````````````````````````````````````````````````````````````````
    if len(valid_filenames) != 0:
        return home_dir_path + '\\' + valid_filenames[0]
    else:
        return ''


def get_font_list():
    raw_font_filename_list = [f for f in listdir(font_tools.FONTS_PATH) if isfile(join(font_tools.FONTS_PATH, f))]
    
    font_list = []
    for raw_filename in raw_font_filename_list:
#         font_name = raw_filename.split('.')[0]
        font_name = raw_filename[0:-4]
        font_list.append(font_name)
    
    return font_list
    
    
    
def build_font_path(font_name):
    return font_tools.FONTS_PATH + '\\' + font_name + '.ttf'
    


def bool_to_state(bool_int, active_low = True):#need????????????????????????????????????????????????
    if active_low == True:
        if   bool_int == 1:
            return 'disabled'
        elif bool_int == 0:
            return 'normal'
        
    elif active_low == False:
        if   bool_int == 0:
            return 'disabled'
        elif bool_int == 1:
            return 'normal'
        
    raise Exception('ERROR    bool_str_to_state in GUI_utils received an invalid argument: ', bool_int)


def get_input_img_dims(img_path):
    img = Image.open(img_path)
    width, height = img.size
    
    img_dimensions = {'num': height,
                      'din': width}
    return img_dimensions


def strs_to_int_ratio(str1, str2):
    i1 = int(str1)
    i2 = int(str2)
    return i1 / i2
    
    
    
def get_last_path_var(f_path):
    split_f_path = re.split(r'[\\/]', f_path)
    return split_f_path[-1]

    

def valid_dir_name(dir_name):
    try:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            os.rmdir(dir_name)
        return True
    except:
        return False



def valid_img_filename(filename):
    try:
        from PIL import Image
        img = Image.new('RGB', (60, 30), color = 'red')
        img.save(filename)
        os.remove(filename)
        return True
    except:
        return False
    


    
    
    #DO NOT DELETE THIS!!!!   I HAVE NO CLUE WHY I WROTE THIS BUT I MUST HAV HAD A REASON!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def get_defalt_output_img_file_path(img_file_path):
     out_img_path = ''
     
     splt_path = re.split(r'[\\/]', img_file_path)
     
     filename = splt_path.pop()
     splt_filename = filename.split('.')
     splt_filename.insert(1, OUTPUT_IMAGE_SUFFIX)
     
     for e in splt_path:
         out_img_path += e
         
     for e in splt_filename:
         out_img_path += e
         
     return out_img_path

    
def get_matching_filenames_list(path, file_extention_list):
    filename_list = []
    for file_extention in file_extention_list:
        try:
            for file in os.listdir(path):
                if file.endswith(file_extention):
                    filename_list.append(file)
        except:
            pass
    return filename_list
    
    
    
    
    
    
    
    #advanced_tab

    
    
def round_color(color_tup):
    r, g, b = color_tup
    return (int(r), int(g), int(b))

def tk_color(clr_tuple):
    return "#%02x%02x%02x" % round_color(clr_tuple)


def apply_color_change(tup_tb, color_tb, color_tuple):
    tup_tb.configure(state = 'normal')
    
    tup_tb.delete(0, "end")
    tup_tb.insert(END, str(round_color(color_tuple)))

#     tk_rgb = "#%02x%02x%02x" % round_color(color_tuple)#(0, 0, 0)
    tk_rgb = tk_color(color_tuple)
 
    color_tb.configure(readonlybackground = tk_rgb)
    tup_tb.configure(state = 'readonly')


    
    
def change_color(tup_tb, color_tb):
    color = askcolor()
    apply_color_change(tup_tb, color_tb, color[0])


def highest_contrast_label_color(background_color):
    r, g, b = background_color
    
    for c in r,g,b:
        c = c / 255.0
        if c <= 0.03928:
            c = c/12.92 
        else:
            c = ((c+0.055)/1.055) ** 2.4
    L = 0.2126 * r + 0.7152 * g + 0.0722 * b
    
    if (255 - L) > L:
        return (255, 255, 255) #white
    else:
        return (0, 0, 0) #black
    
    
    
def str_to_tup(tup_str):
    split_tup_str = re.split(r'[(,)]', tup_str)
    r, g, b = split_tup_str[1:4]
    return(r, g, b)

def str_to_int_tup(tup_str):
    split_tup_str = re.split(r'[(,)]', tup_str)
    r, g, b = split_tup_str[1:4]
    return(int(r), int(g), int(b))




def load_colors(list_box_widget, color_list):
    for color_num in range(len(color_list)):
        color = color_list[color_num]
        list_box_widget.insert(END, str(color))
        bg_color = tk_color(color)
        font_color = tk_color( highest_contrast_label_color(color) )
        list_box_widget.itemconfig(color_num, bg=bg_color, fg = font_color)
    
    
    
    
def lbox_contents_to_str(lbox_widget):
    lbox_string = ''
    for item_num in range( lbox_widget.size() ):
        if item_num != 0:
            lbox_string += LBOX_STR_DELIM
        lbox_string += str(lbox_widget.get(item_num))
    return lbox_string
    
def lbox_str_to_tup_list(lbox_str):
    tup_list = []
    tup_str_list = lbox_str.split(LBOX_STR_DELIM)
    
    for tup_str in tup_str_list:
        tup_list.append(str_to_int_tup(tup_str))
    return tup_list
    
    


def get_color_or_none(text_box_widget):
    if(text_box_widget['state'] == 'disabled'):
        return None
    return str_to_int_tup(text_box_widget.get())
    
    
    
def font_size_or_message(txt_box_widget, msg):  
    if(txt_box_widget['state'] == 'disabled'):
        return msg
    return int(txt_box_widget.get())


# find length of longest line in chars, for use in scale_img_size
def find_final_img_char_width(kwargs):
    font_aspect_ratio = font_tools.get_aspect_ratio(kwargs['font_path'])
     
     
    #read in the text that will be colored to show a picture
#     print('reading in data text file...') 
    data = tools.read_text_file(kwargs['input_text_file_path'])
     
    #turn list of lines of data into one big string, use that to get number of chars in data, then split it into words
#     print('formatting data into word list...')
    data_str  = tools.format_data(data)
    num_chars = len(data_str)
    word_list = data_str.split(' ')
     
     
    #turn true_dimension_ratio into max number of lines and max chars per line
#     print('calculating ideal text image dimensions...')
    #find correct image dimensions by adjusting desired ratio for the difference between width and height of a char
    true_dimension_ratio = kwargs['output_image_dim_ratio'] * font_aspect_ratio
    ideal_dimentions = tools.calc_ideal_dimentions(true_dimension_ratio, num_chars)
     
    #make list of lines to be output in final image
#     print('creating text lines...')
    lines = tools.make_correct_lines(ideal_dimentions['num_lines'], ideal_dimentions['line_length'], word_list)
    
    return len(tools.find_longest_line(lines))

    
    
    
    
import GUI
if __name__ == '__main__':
#     print(str_to_tup("(222,4e,599)"))
#     change_color(3,5)
    GUI.main()