import random

# just for testing VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV


def rcp_d_print_str(rcp_d):
    try:
        save_name = rcp_d['clip_path'].split('\\')[-1]
        return '  {' + str(rcp_d['rating']) + ' : ' + save_name + '}'
    except KeyError:
        return '  {}'
        
    
def print_rcp_d(rcp_d):
    print(rcp_d_print_str(rcp_d))
    
def print_rcp_dl(rcp_dl):
    print ('[')
    for rcp_d in rcp_dl:
        print_rcp_d(rcp_d)
    print (']')

    
# just for testing ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



def order_rated_clip_paths___random(rated_clip_path_dl):    
    ordered_clip_path_l = []
    
    while(len(rated_clip_path_dl) > 0):
        l_pos = random.randint(0, len(rated_clip_path_dl) - 1)
        ordered_clip_path_l.append(rated_clip_path_dl[l_pos]['clip_path'])
        rated_clip_path_dl.pop(l_pos)
    return ordered_clip_path_l


# puts beginning_high_rated_pad # highest rated clips at front and end_high_rated_pad # next highest clips at end,
# evenly distributes high and low rated clips in between
def order_rated_clip_paths___balanced_with_padding(rated_clip_path_dl, beginning_high_rated_pad, end_high_rated_pad):
    def _most_common_rating():
        rating_freq_d = {}
        for rcp_d in rated_clip_path_dl:
            if  rcp_d['rating'] in rating_freq_d.keys():
                rating_freq_d[rcp_d['rating']] = rating_freq_d[rcp_d['rating']] + 1
            else:
                rating_freq_d[rcp_d['rating']] = 1
        
        #find most common
        most_common_rating = random.choice(list(rating_freq_d))
        for rating, num_occur in rating_freq_d.items():
            if rating_freq_d[most_common_rating] < num_occur:
                most_common_rating = rating
        return most_common_rating
        
    def _break_up_by_rating(most_common_rating):
        high_rcp_dl = []
        low_rcp_dl  = []
        avg_rcp_dl  = []
        
        for rcp_d in rated_clip_path_dl:
            if   rcp_d['rating'] == most_common_rating:
                avg_rcp_dl.append(rcp_d)
            elif rcp_d['rating'] < most_common_rating:
                low_rcp_dl.append(rcp_d)
            elif rcp_d['rating'] > most_common_rating:
                high_rcp_dl.append(rcp_d)
        return high_rcp_dl, low_rcp_dl, avg_rcp_dl
        
        
    def _order_rcp_dl(rcp_dl):
        def __highest_rated_pos(rcp_dl):
            highest_rated_pos = 0
            for rcp_d_num, rcp_d in enumerate(rcp_dl):
                if rcp_d['rating'] > rcp_dl[highest_rated_pos]['rating']:
                    highest_rated_pos = rcp_d_num
            return highest_rated_pos
        
        ordered_rcp_dl = []
        
        while(len(rcp_dl) > 0):
            highest_rated_pos = __highest_rated_pos(rcp_dl)
            ordered_rcp_dl.append(rcp_dl[highest_rated_pos])
            rcp_dl.pop(highest_rated_pos)
        return ordered_rcp_dl
        
    def _make_empty_dl(num_elements):
        dl = []
        for x in range(num_elements):
            dl.append({})
        return dl
        
    def _sort_highest_on_ends(o_rcp_dl):
        highest_on_ends_rcp_dl = _make_empty_dl(len(o_rcp_dl))
       
        pos = 0       
        cnt = 0
        while(len(o_rcp_dl) > 0):
            if pos == 0:
                highest_on_ends_rcp_dl[pos + cnt] = o_rcp_dl[0]
                pos = -1
            else:
                highest_on_ends_rcp_dl[pos - cnt] = o_rcp_dl[0]
                cnt += 1
                pos = 0
            o_rcp_dl.pop(0)
        return highest_on_ends_rcp_dl
        
    def _random_empty_pos(rcp_dl):
        pos_l = []
        for rcp_d_num, rcp_d in enumerate(rcp_dl):
            if rcp_d == {}:
                pos_l.append(rcp_d_num)
        return random.choice(pos_l)
        

    
    
    
    
    # break rated_clip_path_dl into high, low, and avg rated_clip_path_dls
    most_common_rating = _most_common_rating()
    #print(most_common_rating)
    
    # get un-ordered dls
    uo_high_rcp_dl, uo_low_rcp_dl, uo_avg_rcp_dl = _break_up_by_rating(most_common_rating)
    
    # put un-ordered dls in order from highest to lowest
    o_high_rcp_dl = _order_rcp_dl(uo_high_rcp_dl)
    o_low_rcp_dl  = _order_rcp_dl(uo_low_rcp_dl)
    #o_avg_rcp_dl  = uo_avg_rcp_dl
    
#     print('high: ')
#     print_rcp_dl(o_high_rcp_dl)
#     print('low: ')
#     print_rcp_dl(o_low_rcp_dl)
#     print('avg: ')
#     print_rcp_dl(uo_avg_rcp_dl)
   
    # make empty rcp_dl with enough space for all the rcp_ds
    output_rcp_dl = _make_empty_dl(len(rated_clip_path_dl))
    #print(output_rcp_dl)
    
    # add beginning padding
    
    for pos in range( beginning_high_rated_pad ):
        if len(o_high_rcp_dl) > 0:
            if len( output_rcp_dl ) - 1 > pos:
#                 print(pos)#`````````````````````````````````````````````````````````````````````````
                output_rcp_dl[pos] = o_high_rcp_dl[0]
            o_high_rcp_dl.pop(0)
        
    # add end padding
    for pos in range( end_high_rated_pad ):
        if len(o_high_rcp_dl) > 0:
            if len( output_rcp_dl ) - 1 > pos:
#                 print(pos)#`````````````````````````````````````````````````````````````````````````
                output_rcp_dl[-1-pos] = o_high_rcp_dl[0]
            o_high_rcp_dl.pop(0)
    #print_rcp_dl(output_rcp_dl)

    # add the rest of the high rated, spaced out evenly with the highest rated towards the beginning and end,
    # if cant space out evenly, assign the remainder randomly
    if len(o_high_rcp_dl) > 0:
        high_rated_spacing = int( ( output_rcp_dl.count({}) / len( o_high_rcp_dl ) + 1 ) )
    else:
        low_rated_spacing = 0
   
    highest_on_ends_high_rcp_dl = _sort_highest_on_ends(o_high_rcp_dl)
    
    for rcp_d_num, rcp_d in enumerate( highest_on_ends_high_rcp_dl ):
        try:
            output_rcp_dl[beginning_high_rated_pad + (rcp_d_num * high_rated_spacing)] = highest_on_ends_high_rcp_dl[rcp_d_num]
        except IndexError:
            pos = _random_empty_pos(output_rcp_dl)
            output_rcp_dl[pos] = highest_on_ends_high_rcp_dl[rcp_d_num]
    #print_rcp_dl(output_rcp_dl)
       
    # add the low rated, spaced out evenly but then moved forward so that a low rated clip is always followed by a high rated clip
    # if possable, put the highest rated bad clips on the ends with the worst in the middle
    if len(o_low_rcp_dl) > 0:
        low_rated_spacing = int( ( (len(rated_clip_path_dl) - beginning_high_rated_pad - end_high_rated_pad) / len( o_low_rcp_dl ) + 1 ) )
    else:
        low_rated_spacing = 0
        
    #print(low_rated_spacing)
    
    highest_on_ends_low_rcp_dl = _sort_highest_on_ends(o_low_rcp_dl)
    #print_rcp_dl(highest_on_ends_low_rcp_dl)
    
    for rcp_d_num, rcp_d in enumerate( highest_on_ends_low_rcp_dl ):
        pos = rcp_d_num * low_rated_spacing
        while(True):
#             print(len(output_rcp_dl))#````````````````````````````````````````````````````````````````````````
#             print(pos)#````````````````````````````````````````````````````````````````````````````````````````````
#             print(len(output_rcp_dl) > (pos + 1))#``````````````````````````````````````````````````````````````````
            if pos > len(output_rcp_dl) - 1:
                pos = _random_empty_pos(output_rcp_dl)
                break
            elif output_rcp_dl[pos] == {} and len(output_rcp_dl) > (pos + 1) and output_rcp_dl[pos + 1] != {} and output_rcp_dl[pos + 1]['rating'] > most_common_rating:
                break

            pos += 1
        output_rcp_dl[pos] = highest_on_ends_low_rcp_dl[rcp_d_num]
        
    #print_rcp_dl(output_rcp_dl)
    
    
    # fill the rest randomly with the average clips
    
    for rcp_d in uo_avg_rcp_dl:
        pos = _random_empty_pos(output_rcp_dl)
        output_rcp_dl[pos] = rcp_d
        
        
    #print_rcp_dl(output_rcp_dl)
    
    
    # get rid of the ratings and just return a list of clip paths
    output_clip_path_list = []
    for rcp_d in output_rcp_dl:
        if rcp_d != {}: # no clue why there is  an empty d at the end one tim, but it fixes an error
#             print(rcp_d)#```````````````````````````````````````````````````````````````````````````````````````
            output_clip_path_list.append(rcp_d['clip_path'])
        
    #print(output_clip_path_list)
        
        
    return output_clip_path_list
    
    
    

def order_rated_clip_paths(rated_clip_path_dl, order_type, beginning_high_rated_pad = 2, end_high_rated_pad = 2):
    if order_type == 'random':
        return order_rated_clip_paths___random(rated_clip_path_dl)
    elif order_type == 'balanced_with_padding':
        return order_rated_clip_paths___balanced_with_padding(rated_clip_path_dl, beginning_high_rated_pad, end_high_rated_pad)
    
    
    
    
    
    
    
if __name__ == '__main__':
    # to be able to import from parent dir
    import sys
    parent_dir_path = ''
    for dir in sys.path[0].split('\\')[0:-1]:
        parent_dir_path += dir + '\\'
    sys.path.append(parent_dir_path[0:-1])

    # from parent dir
#     import ptest3
#     ptest3.main() 
    
    
    import pool_clips_data_handler
    #from gui import clip_order


    rated_clip_path_dl = pool_clips_data_handler.get_rated_clip_path_dl()
    ordered_clip_path_l = order_rated_clip_paths(rated_clip_path_dl, 'balanced_with_padding')
    
    