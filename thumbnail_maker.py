from PIL import Image


def make_solid_color_img(dims, color, out_file_path):
    img = Image.new('RGB', dims, color)
    img.save(out_file_path)
    
    
    
    
img = Image.new('RGB', (2048, 1152), 'white')
img.save('pics/blank_thumb.png')