import cv2
vidcap = cv2.VideoCapture("C:\\Users\\Brandon\\Documents\\Personal_Projects\\vid_m_comp_big_data\\vids\\post_0011.mp4")
success,image = vidcap.read()
count = 0
while success:
  cv2.imwrite("C:\\Users\\Brandon\\Documents\\Personal_Projects\\vid_m_comp_big_data\\vids\\frame_test\\frame%d.png" % count, image)     # save frame as JPEG file      
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1
  
  
  
  
  
  
# import cv2
# print(cv2.__version__)
# vidcap = cv2.VideoCapture('big_buck_bunny_720p_5mb.mp4')
# success,image = vidcap.read()
# count = 0
# success = True
# while success:
#   cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
#   success,image = vidcap.read()
#   print 'Read a new frame: ', success
#   count += 1