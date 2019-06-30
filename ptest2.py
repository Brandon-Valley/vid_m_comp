import os

# print(os.path.abspath('upload_video.py'))
import sys
# print(sys.path[0])

PTEST2_SYS_PATH = sys.path[0]
print('in ptest2, PTEST2_SYS_PATH: ', PTEST2_SYS_PATH)

import os
print('in ptest2,  os.path.dirname(os.path.abspath(__file__)): ', os.path.dirname(os.path.abspath(__file__)))

import file_system_utils
print('in ptest2,   file_system_utils.get_path_to_current_file(__file__): ', file_system_utils.get_path_to_current_file(__file__))
