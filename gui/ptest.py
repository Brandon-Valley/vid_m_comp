import os

print(os.path.abspath('../upload_video.py'))

import sys
# print(sys.path[0])


# to be able to import from parent dir
import sys
parent_dir_path = ''
for dir in sys.path[0].split('\\')[0:-1]:
    parent_dir_path += dir + '\\'
sys.path.append(parent_dir_path[0:-1])

# from parent dir
import ptest2

print('in gui ptest, ptest2 sys path: ', ptest2.PTEST2_SYS_PATH)