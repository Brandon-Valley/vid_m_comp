# https://dzone.com/articles/python-gui-examples-tkinter-tutorial-like-geeks

from tkinter.ttk import *
from tkinter import *

#from GUI_tools import Tab

#import build_image
#import GUI_utils

#Tabs
#import Edit_Tab
#import Advanced_Tab
import Build_Tab
import Compile_Tab
import Download_Tab
import Upload_Tab


 
def main(msg = None): 
    root = Tk()
    
    root.title("Text Image Maker")

    tab_control = Notebook(root)
    tab_control.grid(row=1, column=0, sticky='NESW')
    
    
    tab_tup_l = [#('Build'   , 'build'   , Build_Tab.Build_Tab),
                 ('Compile' , 'compile' , Compile_Tab.Compile_Tab),
                 ('Upload'  , 'upload'  , Upload_Tab.Upload_Tab),
                 ('Download', 'download', Download_Tab.Download_Tab)]
    tab_list = []
    tab_dict = {}
    for tab_tup in tab_tup_l:
        tab = Frame(tab_control)
        tab_control.add(tab, text=tab_tup[0])
        tab_dict[tab_tup[1]] = tab_tup[2](tab, tab_control)
        tab_list.append(tab)
    
#     tab1 = Frame(tab_control)
#     tab2 = Frame(tab_control)
#     tab3 = Frame(tab_control)
#     tab4 = Frame(tab_control)
#     tab5 = Frame(tab_control)
#     tab_control.add(tab1, text='Download')
#     tab_control.add(tab2, text='Build')
#     tab_control.add(tab4, text='Compile')
#     tab_control.add(tab5, text='Edit')
#     tab_control.add(tab3, text='Advanced Edit')
#     
# 
# 
     # tab_dict = {'download': tab_tup_l[0][2](tab1, tab_control),# Download_Tab.Download_Tab(tab1, tab_control),
                 # 'build': Build_Tab.Build_Tab(tab2, tab_control),
                 # 'compile': Compile_Tab.Compile_Tab(tab4, tab_control),
                 # 'edit': Edit_Tab.Edit_Tab(tab5),
                 # 'advanced': Advanced_Tab.Advanced_Tab(tab3),
                 # }

    #print('in gui, tab dict: ', tab_dict)#``````````````````````````````

    #let all the tabs use each other's member variables
    for tab_name, tab in tab_dict.items():
        tab.tabs = tab_dict

    # run functions where one tab needs to use another tab's
    # members after all tabs have been loaded,
    # but before any user input
    
    tab_dict['compile'].update_compile_upload_log_btn_state()
#     tab_dict['upload'].update_upload_ability()

    print('starting gui...')
    root.mainloop()
 
if __name__ == '__main__':
    print('in gui main')
    main()
    
    
    
    
    
    
    
    
    
