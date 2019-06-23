import datetime
import os
import ntpath


import file_system_utils
import project_vars_handler
import logger
import json_logger

HISTORICAL_DATA_DIR_PATH = 'historical_data'
EVALUATED_POST_IDS_JSON_PATH = HISTORICAL_DATA_DIR_PATH + '/evaluated_post_ids.json'
CURRENT_DATA_DIR_PATH = project_vars_handler.get_var('current_data_dir_path')

# should be right next to current_data
BIG_HISTORICAL_DATA_DIR_PATH = os.path.abspath(os.path.join(CURRENT_DATA_DIR_PATH, os.pardir)) + '/big_historical_data'
NON_EVAL_CLIPS_DATA_CSV_PATH = BIG_HISTORICAL_DATA_DIR_PATH + '/non_eval_clips_data.csv'
NON_EVAL_CLIPS_DIR_PATH      = BIG_HISTORICAL_DATA_DIR_PATH + '/non_eval_clips'

NON_EVAL_CLIPS_DATA_CSV_HEADER_LIST = ['postId', 'clip_path']

MAX_NON_EVAL_CLIPS_DIR_SIZE = 300 * 1000000 # 300 MB

# go back through and rename everything so that in the csv it shows up as non_eval_0, 1, 2,...
# need this so you dont get stuff overwritten next time
def rename_clips_for_order(non_eval_clips_row_dl):
    for row_num, row_d in enumerate(non_eval_clips_row_dl):
        proper_clip_path = NON_EVAL_CLIPS_DIR_PATH + '/non_eval_' + str(row_num) + '.mp4'
        if row_d['clip_path'] != proper_clip_path:
            os.rename(row_d['clip_path'], proper_clip_path)
            row_d['clip_path'] = proper_clip_path
    logger.logList(non_eval_clips_row_dl, NON_EVAL_CLIPS_DATA_CSV_PATH, False, NON_EVAL_CLIPS_DATA_CSV_HEADER_LIST, 'overwrite')


def get_evaluated_post_id_l():
    try:
        evaluated_post_id_l = json_logger.read(EVALUATED_POST_IDS_JSON_PATH)
    except FileNotFoundError:
        evaluated_post_id_l = []
    return evaluated_post_id_l

def log_and_delete_current_data(delete = True):
    def _log_small_historical_data():
        file_system_utils.make_dir_if_not_exist(HISTORICAL_DATA_DIR_PATH)
        
        # make new log dir path
        now = datetime.datetime.now()
        date_time_str = now.strftime("%Y-%m-%d__%H_%M")
        new_log_dir_path = HISTORICAL_DATA_DIR_PATH + '/log__' + date_time_str
        
        # add new dir, delete old if exists
        file_system_utils.delete_if_exists(new_log_dir_path)
        os.mkdir(new_log_dir_path)
        
        # copy data from current_data to new dir in historical_data
        copy_path_l = [CURRENT_DATA_DIR_PATH + '/download_log.csv',
                       CURRENT_DATA_DIR_PATH + '/pool_clips_data.csv',
                       CURRENT_DATA_DIR_PATH + '/LOG_FILES']
        file_system_utils.copy_objects_to_dest(copy_path_l, new_log_dir_path)
        
        # get list of evaluated postIds
        pool_evaluated_post_id_l = []
        pool_clips_data_row_dl = logger.readCSV(CURRENT_DATA_DIR_PATH + '/pool_clips_data.csv')    
        for row_d in pool_clips_data_row_dl:
            if row_d['status'] != '':
                pool_evaluated_post_id_l.append(row_d['postId'])
                
#         print(pool_evaluated_post_id_l)#``````````````````````````````````````````````````````````````````````````
                
        # add pool_evaluated_post_id_l to existing list of evaluated post ids
        evaluated_post_id_l = get_evaluated_post_id_l()
#         print(evaluated_post_id_l)#`````````````````````````````````````````````````````````````````````````
        json_logger.write(pool_evaluated_post_id_l + evaluated_post_id_l, EVALUATED_POST_IDS_JSON_PATH)
        
          
        
    def _log_non_eval_clips():
        def __make_og_non_eval_post_id_clip_path_dl():
            new_row_dl = []
            pool_row_dl = logger.readCSV(CURRENT_DATA_DIR_PATH + '/pool_clips_data.csv')
            
            for pool_row_d in pool_row_dl:
                if pool_row_d['status'] == '':
                    new_row_dl.append({'postId'    : pool_row_d['postId'],
                                       'clip_path' : pool_row_d['clip_path']})
            return new_row_dl
        
        def __get_post_id_l(non_eval_clips_row_dl):
            post_id_l = []
            for row_dl in non_eval_clips_row_dl:
                post_id_l.append(row_dl['postId'])
            return post_id_l
              
            
            
        file_system_utils.make_dir_if_not_exist(NON_EVAL_CLIPS_DIR_PATH)
        try:
            non_eval_clips_row_dl = logger.readCSV(NON_EVAL_CLIPS_DATA_CSV_PATH)
        except FileNotFoundError:
            non_eval_clips_row_dl = []
        
        # make row_dl of postIDs and original clip paths
        og_non_eval_post_id_clip_path_dl = __make_og_non_eval_post_id_clip_path_dl()
        
        # build final_non_eval_post_id_clip_path_dl - contains postId and new clip path that clip is about to be saved to
        # also will not include any postIds that are already logged
        final_non_eval_post_id_clip_path_dl = []
        existing_post_id_l = __get_post_id_l(non_eval_clips_row_dl)
        
        clips_added = 0
        for d in og_non_eval_post_id_clip_path_dl:
            if d['postId'] not in existing_post_id_l:
                new_save_name = 'non_eval_' + str(len(non_eval_clips_row_dl) + clips_added) + '.mp4'
                final_non_eval_post_id_clip_path_dl.append({'postId'    : d['postId'],
                                                            'clip_path' : NON_EVAL_CLIPS_DIR_PATH + '/' + new_save_name})
                clips_added += 1

        # copy all non-evaluated clips to thier new home in non_eval_clips
        # could just rename, but this is nicer for testing
        og_pos = 0
        for d in final_non_eval_post_id_clip_path_dl:
            while(d['postId'] != og_non_eval_post_id_clip_path_dl[og_pos]['postId']):
                og_pos += 1
            og_clip_path = og_non_eval_post_id_clip_path_dl[og_pos]['clip_path']
            file_system_utils.copy_files_to_dest([og_clip_path], NON_EVAL_CLIPS_DIR_PATH)
            just_copied_clip_path = NON_EVAL_CLIPS_DIR_PATH + '/' + ntpath.basename(og_clip_path)
            os.rename(just_copied_clip_path, d['clip_path'])

        
        # add info from final_non_eval_post_id_clip_path_dl to non_eval_clips_row_dl
        for row_d in final_non_eval_post_id_clip_path_dl:
            non_eval_clips_row_dl.append(row_d)
            

            
        logger.logList(non_eval_clips_row_dl, NON_EVAL_CLIPS_DATA_CSV_PATH, False, NON_EVAL_CLIPS_DATA_CSV_HEADER_LIST, 'overwrite')
       
       
    def _prune_non_eval_clips():
#         print(NON_EVAL_CLIPS_DIR_PATH)#````````````````````````````````````````````````````````````````````````````````````````````

        # remove clips until under max dir size
        age_sorted_non_eval_clip_path_l = file_system_utils.get_file_paths_in_dir_by_age(NON_EVAL_CLIPS_DIR_PATH)
#         print(age_sorted_non_eval_clip_path_l)#``````````````````````````````````````````````````````````````````````````````````
        deleted_clip_path_l = []
        while(file_system_utils.get_size(NON_EVAL_CLIPS_DIR_PATH) > MAX_NON_EVAL_CLIPS_DIR_SIZE):
            pos = len(deleted_clip_path_l)
            os.remove(age_sorted_non_eval_clip_path_l[pos])
            deleted_clip_path_l.append(os.path.abspath(age_sorted_non_eval_clip_path_l[pos]))
            
            
            
        # remove rows that go to the paths of the clips that were just deleted
        non_eval_clips_row_dl = logger.readCSV(NON_EVAL_CLIPS_DATA_CSV_PATH)
        
        del_row_d_l = []
        for row_d_num, row_d in enumerate(non_eval_clips_row_dl):
            if os.path.abspath(row_d['clip_path']) in deleted_clip_path_l:
                del_row_d_l.append(row_d)
                
        for row_d in del_row_d_l:
            non_eval_clips_row_dl.remove(row_d)
         
        # go back through and rename everything so that in the csv it shows up as non_eval_0, 1, 2,...
        # need this so you don't get stuff overwritten next time       
        rename_clips_for_order(non_eval_clips_row_dl)


        
        
    _log_small_historical_data()
    _log_non_eval_clips()
    _prune_non_eval_clips()
    if delete:
        try:
            file_system_utils.delete_if_exists(CURRENT_DATA_DIR_PATH) # I know it exists
        except PermissionError as e:
            print('ERROR  got permission error, make sure you dont have stuff open in visual studio, error: ', str(e))

    
def get_non_eval_clip_data_d():
    non_eval_clips_row_dl = logger.readCSV(NON_EVAL_CLIPS_DATA_CSV_PATH)
    
    non_eval_clip_data_d = {}
    for row_d in non_eval_clips_row_dl:
        non_eval_clip_data_d[row_d['postId']] = row_d['clip_path']
    return non_eval_clip_data_d


def pull_clip(clip_path, dest_path):
    os.rename(clip_path, dest_path)
    
    non_eval_clips_row_dl = logger.readCSV(NON_EVAL_CLIPS_DATA_CSV_PATH)

    # find and remove row in csv for the clip that was just renamed
    for row_d in non_eval_clips_row_dl:
        if row_d['clip_path'] == clip_path:
            non_eval_clips_row_dl.remove(row_d)
            break
    
    rename_clips_for_order(non_eval_clips_row_dl)
    
    
    
if __name__ == '__main__':
#     pull_clip('C:\\Users\\Brandon\\Documents\\Personal_Projects\\vid_m_comp_big_data/big_historical_data/non_eval_clips/non_eval_0.mp4', 'test.mp4')
    
    
    log_and_delete_current_data(delete = False)
#     print(get_non_eval_clip_data_d())

    print('done')