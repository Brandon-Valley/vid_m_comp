from tkinter import *     
import file_system_utils
 
from PIL import Image

im = Image.open('test_thumb.png')
w, h = im.size
 
 
print(w,h)
 
 
root = Tk()      
canvas = Canvas(root, width = w, height = h)      
canvas.pack()      
img = PhotoImage(file='test_thumb.png')   
# file_system_utils.delete_if_exists('test_thumb.png')   
canvas.create_image(0,0, anchor=NW, image=img)      
mainloop()