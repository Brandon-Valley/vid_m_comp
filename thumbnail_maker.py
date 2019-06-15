from PIL import Image


def make_solid_color_img(dims, color, out_file_path):
    img = Image.new('RGB', dims, color)
    img.save(out_file_path)
    
    
    
    
img = Image.new('RGB', (1280, 720), 'black')
img.save('pics/blank_thumb.png')