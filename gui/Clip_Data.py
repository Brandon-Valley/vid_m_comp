# to be able to import from parent dir
import sys
parent_dir_path = ''
for dir in sys.path[0].split('\\')[0:-1]:
    parent_dir_path += dir + '\\'
sys.path.append(parent_dir_path[0:-1])

# from parent dir
import utils

DEFAULT_RATING = 5

class Clip_Data():
    def __init__(self, row_d):
        self.status = self.get_status(row_d['status'])
        self.title = row_d['title']
        self.duration = int( row_d['duration'] )
        self.rating = self.get_rating(row_d['rating'])
        self.use_txt_overlay = self.get_use_txt_overlay(row_d['use_text_overlay'])
        self.top_txt = row_d['top_text']
        self.bottom_txt = row_d['bottom_text']
        self.clip_path = row_d['clip_path']
        self.current = True
        
        self.duration_str = utils.sec_to_min_str(int(row_d['duration']))
        self.eval_color = self.get_eval_color(row_d['status'])
        self.use_trimmed_clip = self.get_use_trimmed_clip(row_d['use_trimmed_clip'])
        
        
    def get_use_trimmed_clip(self, use_trimmed_clip):
        if use_trimmed_clip == '1':
            return True
        return False 
        
    def get_eval_color(self, status):
        def _from_rgb(rgb):
            return "#%02x%02x%02x" % rgb   
    
        if status == 'accepted':
            return _from_rgb((0, 168, 107))
        elif status == 'declined':
            return 'red'
        elif status == 'pruned':
            return 'purple'
        else:
            return None
        
        
        
    def get_status(self, csv_status):
        if csv_status == '':
            return None
        return csv_status
        
        
    def get_use_txt_overlay(self, csv_use_txt_overlay):
        if   csv_use_txt_overlay == '1':
            return True
        elif csv_use_txt_overlay == '0':
            return False
    
    
    def get_rating(self, csv_rating):
        if csv_rating == '':
            return DEFAULT_RATING
        else:
            return int(csv_rating)
        
        
        
        
        
        
        
        
        
        
import GUI  
if __name__ == '__main__':
    GUI.main()
        