from tkinter import END
from tkinter import filedialog

import GUI #only need for testing




DIGITS = '0123456789.-'


class Tab():
    def __init__(self, master):
        self.master = master
        self.tabs = None
        
        self.digits_only = (self.master.register(self.validate), DIGITS, '%P')
         
    def validate(self, allowed_chars, value_if_allowed):
        #need this to make delete work
        if (value_if_allowed == ''):
            return True
    
        for char in value_if_allowed:
            if char not in allowed_chars:
                return False
        return True
    
    #bind keys to widget such that func gets called any time the contents of the widget change
    def bind_to_edit(self, widget, func):
        widget.bind("<KeyRelease>", func)
        widget.bind("<KeyRelease-BackSpace>", func)
        widget.bind("<KeyRelease-Delete>", func)
        widget.bind("<KeyRelease-space>", func)
        
    def bind_to_click(self, widget, func):
        widget.bind("<ButtonRelease>", func)
        widget.bind("<Enter>", func)
        
    # returns length of longest str in a list,
    # useful for making combo boxes match length of contents
    # if useing for a combo box, will need to add + 1 so V part
    # of box doesnt cover end of longest str
    def max_str_len_in_l(self, str_list):
        len_max = 0
        for m in str_list:
            if len(m) > len_max:
                len_max = len(m)
        return len_max + 1

    # fills list box widget from list of strings in order
    def fill_list_box(self, list_box_widget, str_list):
        if str_list != None:
            for str in str_list:
                list_box_widget.insert(END, str)
    
    def path_tb_browse_btn_clk(self, path_txt_box_widget, browse_for, file_type = None):
        #get file path and place it in text box
        
        if browse_for == 'file':
            if file_type == None:
                file_system_item = filedialog.askopenfilename()

            else:
                file_system_item = filedialog.askopenfilename(filetypes = (("Images", "*" + file_type), ("All files", "*")))#filetypes = (("Images", '*.png|*.jpg'), ("All files", "*")))#"*" + file_types   #,("Template files", '*.jpg'), 
        elif browse_for == 'dir':
            file_system_item = filedialog.askdirectory()
        else:
            raise Exception('ERROR:  In Tab.py, in path_tb_browse_btn_clk, invalid value for browse_for: ', browse_for)
        path_txt_box_widget.delete(0, "end")
        path_txt_box_widget.insert(END, file_system_item)
        
#         output_path_text_box_updated()
        
        
        
        
        
        
        
        
        
        
        
if __name__ == '__main__':
    GUI.main()