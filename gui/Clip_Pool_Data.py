

# to be able to import from parent dir
import sys
parent_dir_path = ''
for dir in sys.path[0].split('\\')[0:-1]:
    parent_dir_path += dir + '\\'
sys.path.append(parent_dir_path[0:-1])

# from parent dir
import utils

class Clip_Pool_Data():
    def __init__(self, row_dl):
        self.row_dl = row_dl
        self.total_time_str     = self.get_total_time_str(row_dl)
        self.clip_num_str       = self.get_clip_num_str(row_dl)
        self.num_accepted_clips = self.get_num_status_clips(row_dl, 'accepted')
        self.num_declined_clips = self.get_num_status_clips(row_dl, 'declined')
        self.num_pruned_clips   = self.get_num_status_clips(row_dl, 'pruned')
 
        
        
    def get_num_status_clips(self, row_dl, status):
        num_status = 0
        for row_d in row_dl:
            if row_d['status'] == status:
                num_status += 1
        return str(num_status)
    
               
    
    
    def get_total_time(self, row_dl):
        total_sec = 0
        for row_d in row_dl:
            if row_d['status'] == 'accepted':
                total_sec += int(row_d['duration'])
        return total_sec
    
   
    def get_total_time_str(self, row_dl):
        total_sec = self.get_total_time(row_dl)
        return utils.sec_to_min_str(total_sec)
    
    
    def get_clip_num_str(self, row_dl):
        row_num = utils.get_cur_row_num(row_dl) + 1
        total_rows = len(row_dl)
        return str(row_num) + ' / ' + str(total_rows)

    
    
    # 3 clips ready to prune, no clips below rating
    def get_prune_info_d(self, prune_clips, prune_rating_str, prune_time_str):
        if prune_rating_str == '':
            prune_rating = 0
        else:
            prune_rating = int(prune_rating_str)
        #print('purne rating: ' , prune_rating)#`````````````````````````````````````````````````````````````````
    
        def get_prune_order_dl():
            # lowest priority is shorter clip if ratings ==
            def get_lowest_priority_row_num(prune_row_dl):
                lowest_priority_row_num = 0
                for row_num, row_d in enumerate(prune_row_dl):
                    if   int(prune_row_dl[row_num]['rating']) < int(prune_row_dl[lowest_priority_row_num]['rating']):
                        lowest_priority_row_num = row_num
                    elif prune_row_dl[row_num]['rating'] == prune_row_dl[lowest_priority_row_num]['rating']:
                        if int(prune_row_dl[row_num]['duration']) < int(prune_row_dl[lowest_priority_row_num]['duration']):
                            lowest_priority_row_num = row_num
                return lowest_priority_row_num
        
            # build prune_row_dl by removing all row_d's with rating >= prune rating and all unrated row_ds
            prune_row_dl = []
            for row_d in self.row_dl:
                if row_d['rating'] != '' and int(row_d['rating']) < prune_rating and row_d['status'] == 'accepted':
                    prune_row_dl.append(row_d)
                    
            # build final prune order dl
            prune_order_dl = []
            while(len(prune_row_dl) > 0):
                lowest_priority_row_num = get_lowest_priority_row_num(prune_row_dl)
                prune_order_dl.append(prune_row_dl[lowest_priority_row_num])
                prune_row_dl.pop(lowest_priority_row_num)
            return prune_order_dl
                   

                   
                
        def prune_time():
            split_prune_time_str_l = prune_time_str.split(':')
            min_str = split_prune_time_str_l[0]
            sec_str = split_prune_time_str_l[1]
            return int( int(min_str) * 60 ) + int(sec_str)
            
        def no_accepted_clips_below_rating():
            for row_d in self.row_dl:
                if row_d['rating'] != '' and int(row_d['rating']) < prune_rating and row_d['status'] == 'accepted':
                    return False
            return True
            
            
        def get_num_clips_ready_to_prune(prune_order_dl):
            if len(prune_order_dl) == 0:
                return 0
        
            num_clips_ready_to_prune = 0
            total_sec = self.get_total_time(self.row_dl)# - int(prune_order_dl[0]['duration'])
            
            #if total_sec > prune_time():
                #num_clips_ready_to_prune += 1
            
            while total_sec > prune_time() and num_clips_ready_to_prune < len(prune_order_dl):
                #print('in loop, total_sec: ', total_sec)
                total_sec -= int(prune_order_dl[num_clips_ready_to_prune]['duration'])
                #print("int(prune_order_dl[num_clips_ready_to_prune]['duration']: ", int(prune_order_dl[num_clips_ready_to_prune]['duration']))
                #print('new calc total_sec: ', total_sec)
                if total_sec >= prune_time():
                    num_clips_ready_to_prune += 1
                    
            return num_clips_ready_to_prune
                
                
        def get_time_needed_for_next_prune_str(prune_order_dl):
            total_sec = self.get_total_time(self.row_dl)
            sec_needed = total_sec - int(prune_order_dl[0]['duration'])
            return utils.sec_to_min_str(sec_needed)

                       
        
        prune_info_d = {'info_str'     : None,
                        'prune_rows_dl': None}
     
        if no_accepted_clips_below_rating():
            prune_info_d['info_str'] = 'No Accepted Clips Below Rating'
            return prune_info_d
            
        try:            
            prune_time_test = prune_time()
        except (ValueError, IndexError):
            prune_info_d['info_str'] = 'Invalid Prune Time'
            return prune_info_d
            #return 'Invalid Prune Time'
            
        prune_order_dl = get_prune_order_dl()
#         print(prune_order_dl)#``````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
        num_clips_ready_to_prune = get_num_clips_ready_to_prune(prune_order_dl)
        
        prune_info_d['prune_row_dl'] = prune_order_dl[0:num_clips_ready_to_prune]
        
        if num_clips_ready_to_prune == 0:
            prune_info_d['info_str'] = get_time_needed_for_next_prune_str(prune_order_dl) + ' Needed For Next Prune'
            return prune_info_d
            #return get_time_needed_for_next_prune_str(prune_order_dl) + ' Needed For Next Prune'
        
        prune_info_d['info_str'] = str(num_clips_ready_to_prune) + ' Clips Ready To Prune'
        return prune_info_d
    
        #return str(num_clips_ready_to_prune) + ' Clips Ready To Prune'
            

    def get_prune_info_str(self, prune_clips, prune_rating_str, prune_time_str):
        prune_info_d = self.get_prune_info_d(prune_clips, prune_rating_str, prune_time_str)
        return prune_info_d['info_str']
        
    def get_prune_row_dl(self, prune_clips, prune_rating_str, prune_time_str):
        prune_info_d = self.get_prune_info_d(prune_clips, prune_rating_str, prune_time_str)
        return prune_info_d['prune_row_dl']
        
        
        
        
        
        
        
        
        
        
import GUI  
if __name__ == '__main__':
    GUI.main()
        