from tkinter import *
from PIL import Image
import io

class Window:       
    def __init__(self, master):
        master.title("Image Processing test")
        master.minsize(800, 400)

        im = Image.open("pics/thumbnail.png")
        size = 240, 240
        im.thumbnail(size)
        im.save('test_thumb.png')
#         b = io.BytesIO()
#         im.save(b, 'gif')
#         p = b.getvalue()
#         photo = BitmapImage(data=p)
#         
#         im2 = Image.open('test_thumb.png')
        img = PhotoImage(file='test_thumb.png') 
        
        
        w = Label(root, image=img, width=240, height=240).grid(row=20, column=2)
#         self.photo = photo

root = Tk()    
window = Window(root)
root.mainloop()