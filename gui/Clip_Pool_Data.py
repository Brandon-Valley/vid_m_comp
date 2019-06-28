

# to be able to import from parent dir
import sys
parent_dir_path = ''
for dir in sys.path[0].split('\\')[0:-1]:
    parent_dir_path += dir + '\\'
sys.path.append(parent_dir_path[0:-1])

# from parent dir
import utils

HIGHEST_RATING = 10


class Clip_Pool_Data():
    def __init__(self, row_dl):
        self.row_dl = row_dl
        self.total_time_str         = self.get_total_time_str(row_dl)
        self.clip_num_str           = self.get_clip_num_str(row_dl)
        self.num_accepted_clips     = self.get_num_status_clips(row_dl, 'accepted')
        self.num_declined_clips     = self.get_num_status_clips(row_dl, 'declined')
        self.num_pruned_clips       = self.get_num_status_clips(row_dl, 'pruned')
        self.ratings_occ_l          = self.build_ratings_occ_l(row_dl)
        self.ratings_occ_str_dl     = self.build_ratings_occ_str_dl()
        self.percent_below_avg_str  = self.get_percent_below_average_str()
        self.percent_above_avg_str  = self.get_percent_above_average_str()
        
        
 
        
        
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
#             print("in clip pool data, total sec: ", utils.sec_to_min_str(total_sec))#``````````````````````````````````````````
#             print("int(prune_order_dl[0]['duration']: ", int(prune_order_dl[0]['duration']))#`1`````````````````````````````````````````
            sec_needed = prune_time() - (total_sec - int(prune_order_dl[0]['duration']))
#             print("in clip pool data, sec_needed: ", utils.sec_to_min_str(sec_needed))#``````````````````````````````````````````

            return utils.sec_to_min_str(sec_needed)

                       
        
        prune_info_d = {'info_str'     : None,
                        'prune_row_dl': []}
     
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
        
        
        
        
        
    def build_ratings_occ_l(self, row_dl):
        ratings_occ_l = []
        for x in range(HIGHEST_RATING + 1):
            ratings_occ_l.append(0)
        
        for row_d in row_dl:
            rating = row_d['rating']
            if rating != '':
                ratings_occ_l[int(rating)] += 1
                
        return ratings_occ_l
            
    
    def build_ratings_occ_str_dl(self):
        def _equal_space_str(in_str, out_len):
            while(len(in_str) < out_len):
                in_str = ' ' + in_str
            return in_str

        total_ratings = 0
        for num_occ in self.ratings_occ_l:
            total_ratings += num_occ
            
        ratings_occ_str_dl = []
        for rating, num_occ in enumerate(self.ratings_occ_l):
            # build rating_str
            rating_str = _equal_space_str(str(rating), 2)
            # if len(rating_str) == 1:
                # rating_str = ' ' + rating_str
            occ_str = _equal_space_str(str(num_occ), 2)

            occ_percent = int(( num_occ / total_ratings ) * 100)
            occ_percent_str = _equal_space_str(str(occ_percent), 3)
            
            ratings_occ_str_dl.append({'rating'     : rating_str + ':',
                                       'num_occ'    : occ_str,
                                       'occ_percent': occ_percent_str + ' %'})
            
            # ratings_occ_str_l.append(rating_str + ':   ' + occ_str + '   ' + occ_percent_str + ' %')        
        return reversed(ratings_occ_str_dl)
        
        
    def most_common_rating(self):
        most_common_rating = 0
        for r_num, num_occ in enumerate(self.ratings_occ_l):
            if num_occ > self.ratings_occ_l[most_common_rating]:
                most_common_rating = r_num
        return most_common_rating
        
    def sum_list(self, list):
        sum = 0
        for num in list:
            sum += num
        return sum
    
    
    def get_percent_below_average_str(self):
        avg_rating = self.most_common_rating()
        total_ratings = self.sum_list(self.ratings_occ_l)
        num_ratings_below_avg = self.sum_list(self.ratings_occ_l[0:avg_rating])
        return str( int((num_ratings_below_avg / total_ratings) * 100) )
           
    def get_percent_above_average_str(self):
        avg_rating = self.most_common_rating()
        total_ratings = self.sum_list(self.ratings_occ_l)
        num_ratings_above_avg = self.sum_list(self.ratings_occ_l[avg_rating + 1:HIGHEST_RATING + 1])
        return str( int((num_ratings_above_avg / total_ratings) * 100) )
        
        
        
        
        
        
        
        
if __name__ == '__main__':
    import GUI  
    GUI.main()
        