
#
# vid -> frames imgs

import cv2
vidcap = cv2.VideoCapture("C:\\Users\\Brandon\\Documents\\Personal_Projects\\vid_m_comp_big_data\\vids\\post_0011.mp4")
success,image = vidcap.read()
count = 0
while success:
  cv2.imwrite("C:\\Users\\Brandon\\Documents\\Personal_Projects\\vid_m_comp_big_data\\vids\\frame_test\\frame%d.png" % count, image)     # save frame as JPEG file      
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1




# frame img -> widget


from tkinter import *      

import file_system_utils



II = 0

root = Tk()      
canvas = Canvas(root, width = 1400, height = 400)      


pic_path_l = file_system_utils.get_relative_path_of_files_in_dir("C:\\Users\\Brandon\\Documents\\Personal_Projects\\vid_m_comp_big_data\\vids\\frame_test", '.png')
print(pic_path_l)

photo_image_l = []
for pic_path in pic_path_l:
    print(pic_path)
    photo_image_l.append(PhotoImage(file=pic_path))



canvas.pack()      
img2 = PhotoImage(file="pics/green.png")
img = PhotoImage(file="pics/test_thumb.png")            
canvas.create_image(100,100, anchor=NW, image=img)  


def img_scroll(event):
    count = slider.get()
    # respond to Linux or Windows wheel event
    if event.num == 5 or event.delta == -120:
        count -= 1
    if event.num == 4 or event.delta == 120:
        count += 1
    print(count)
    slider.set(count)

 
canvas.bind("<MouseWheel>", img_scroll)


def next_img(event=None):
    canvas.create_image(20,20, anchor=NW, image=photo_image_l[0])
 
    

replay_btn = Button(root, text="Replay Clip", command = next_img)
replay_btn.pack()


def print_pos(event=None):
#     print(slider.get())
    canvas.create_image(20,20, anchor=NW, image=photo_image_l[slider.get()])

slider = Scale(root, from_=0, to=len(photo_image_l)-1, orient = "horizontal", command=print_pos)
slider.pack()



mainloop()

print('here')