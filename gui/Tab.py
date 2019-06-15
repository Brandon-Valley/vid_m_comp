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

        
    

        
        
        
        
        
        
        
        
        
        
        
if __name__ == '__main__':
    GUI.main()