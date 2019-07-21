import logger
import utils # this file in currently in gui, no clue why i am allowed to import like this but im to lazy to investigate right now\
import project_vars_handler
 
# status	title	duration	rating	use_text_overlay	top_text	bottom_text	clip_path	current

POOL_CLIPS_DATA_CSV_PATH = project_vars_handler.get_var('current_data_dir_path') + "/pool_clips_data.csv"
HEADER_LIST = ["current", "priority_next", "status", "title", "duration", "rating", "use_text_overlay", "top_text", "bottom_text", "use_trimmed_clip", "start_trim_time", "end_trim_time", "clip_path", "txt_overlay_clip_path", "trimmed_clip_path", "postId", "postTitle", "postSubmitter", "postType", "postURL", "postSubreddit"]#['status', 'postTitle', 'duration', 'rating', 'use_text_overlay', 'top_text', 'bottom_text', 'clip_path', 'current']

def get_csv_row_dl():
    return logger.readCSV(POOL_CLIPS_DATA_CSV_PATH)

            
# def get_current_row_dl():
#     row_dl = logger.readCSV(POOL_CLIPS_DATA_CSV_PATH)
# 
#     for row_d in row_dl:
#         if row_d['current'] == '1':
#             return Clip_Data.Clip_Data(row_d)
        

    
# move amount usually + or - 1
def move_current(move_amount):
    row_dl = logger.readCSV(POOL_CLIPS_DATA_CSV_PATH)

    # get row num of original current clip and set current 'current' = ''
    og_current_row_num = utils.get_cur_row_num(row_dl)
    row_dl[og_current_row_num]['current'] = ''

    #print(og_current_row_num)
    new_cur_row_num = og_current_row_num + move_amount
    if new_cur_row_num not in range(len(row_dl)):
        if move_amount > 0:
            new_cur_row_num = 0
        else:
            new_cur_row_num = len(row_dl) - 1

    row_dl[new_cur_row_num]['current'] = '1'

    logger.logList(row_dl, POOL_CLIPS_DATA_CSV_PATH, False, HEADER_LIST, 'overwrite')
    
    
def write_to_current(header, value):
    row_dl = logger.readCSV(POOL_CLIPS_DATA_CSV_PATH)
    cur_row_num = utils.get_cur_row_num(row_dl)
    row_dl[cur_row_num][header] = value

    logger.logList(row_dl, POOL_CLIPS_DATA_CSV_PATH, False, HEADER_LIST, 'overwrite')
    
    
def read_from_current(header):
    row_dl = get_csv_row_dl()

    for row_d in row_dl:
        if row_d['current'] == '1':
            return row_d[header]


    
def get_accepted_clip_path_list():
    row_dl = get_csv_row_dl()
    
    accepted_clip_path_list = []
    
    for row_d in row_dl:
        if row_d['status'] == 'accepted':
            accepted_clip_path_list.append(row_d['clip_path'])
    return accepted_clip_path_list






# used by dl_utils
def add_to_clip_pool(row_d):
    logger.logSingle(row_d, POOL_CLIPS_DATA_CSV_PATH, False, HEADER_LIST, 'append')



def init_current_if_needed():
    row_dl = get_csv_row_dl()
    for row_d in row_dl:
        if row_d['current'] == '1':
            return
    row_dl[0]['current'] = '1'
    logger.logList(row_dl, POOL_CLIPS_DATA_CSV_PATH, False, HEADER_LIST, 'overwrite')

    
    
def non_eval_clips_exist():
    row_dl = get_csv_row_dl()
    for row_d in row_dl:
        if row_d['status'] == '':
            return True
    return False


    
    
def prune_by_row_dl(prune_row_dl):
    row_dl = get_csv_row_dl()
    
    prune_id_l = []
    for prune_row_d in prune_row_dl:
        prune_id_l.append(prune_row_d['postId'])
        
    for row_d in row_dl:
        if row_d['postId'] in prune_id_l:
            row_d['status'] = 'pruned'
    logger.logList(row_dl, POOL_CLIPS_DATA_CSV_PATH, False, HEADER_LIST, 'overwrite')
    
  
  
def get_cur_row_num():
    row_dl = get_csv_row_dl()
    return utils.get_cur_row_num(row_dl)


def write_to_row_num(row_num, header, value):
    row_dl = get_csv_row_dl()
    row_dl[row_num][header] = value
 
    logger.logList(row_dl, POOL_CLIPS_DATA_CSV_PATH, False, HEADER_LIST, 'overwrite')
    
    
# if there are no rows markd as priority_next, returns False
def get_next_priority_row_num():
    row_dl = get_csv_row_dl()
    for row_d_num, row_d in enumerate(row_dl):
        if row_d['priority_next'] == '1':
            return row_d_num
    return False


def move_current_to_row_num(row_num):
    row_dl = get_csv_row_dl()
    cur_row_num = utils.get_cur_row_num(row_dl)
    row_dl[cur_row_num]['current'] = ''
    row_dl[row_num]['current'] = '1'
    logger.logList(row_dl, POOL_CLIPS_DATA_CSV_PATH, False, HEADER_LIST, 'overwrite')


def get_main_clip_path_from_row_d(row_d):
    if row_d['use_text_overlay'] == '1' and row_d['txt_overlay_clip_path'] != '':
        return row_d['txt_overlay_clip_path']
    if row_d['use_trimmed_clip'] == '1' and row_d['use_trimmed_clip'] != '':
        print('in pool_clips_data_handler, returning row_d["trimmed_clip_path"]: ', row_d['trimmed_clip_path'])#``````````````````````
        return row_d['trimmed_clip_path']
    else:
        return row_d['clip_path']
    
    
def get_current_main_clip_path():
    row_dl = get_csv_row_dl()
    cur_row_num = utils.get_cur_row_num(row_dl)
    return get_main_clip_path_from_row_d(row_dl[cur_row_num])


def get_rated_clip_path_dl():
    row_dl = get_csv_row_dl()
    
    rated_clip_path_dl = []
    accepted_clip_path_list = []
    
    for row_d in row_dl:
        if row_d['status'] == 'accepted':
            rated_clip_path_dl.append( {'rating'    : int(row_d['rating']),
                                        'clip_path' : get_main_clip_path_from_row_d(row_d) } )
    return rated_clip_path_dl




# def delete_csv():
#     os.remove(POOL_CLIPS_DATA_CSV_PATH)



# logger.logSingle({'a':1, 'b': 2}, POOL_CLIPS_DATA_CSV_PATH, False, ['a', 'b', 'c'], 'append')













if __name__ == '__main__':
    from gui import GUI
    GUI.main()




#move_current(1)
