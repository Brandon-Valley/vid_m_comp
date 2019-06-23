
import logger
import project_vars_handler



CLIP_DOWNLOAD_LOG_CSV_PATH = project_vars_handler.get_var('current_data_dir_path') + '/download_log.csv'# 'current_data/download_log.csv'

def print_dl_report():
    def _num_dl_success(row_dl):
        num_dl_success = 0
        for row_d in row_dl:
            if row_d['download_success'] == 'True':
                num_dl_success += 1
        return num_dl_success
    
    def _youtube_reddit_other_cnt(row_dl):
        def __youtube_reddit_or_other_url(url):
            if 'youtu' in url:
                return 'youtube'
            elif 'redd' in url:
                return 'reddit'
            else:
                return 'other'
#                 raise Exception('ERROR:  Unkown URL type: ', url)
    
    def _fail_reason_occ_d(row_dl):
        fail_reason_occ_d = {}
        for row_d in row_dl:
            
    
    
        yt_cnt = 0
        r_cnt = 0
        other_cnt = 0
        for row_d in row_dl:
            if(__youtube_reddit_or_other_url(row_d['postURL']) == 'youtube'):
                yt_cnt += 1
            elif (__youtube_reddit_or_other_url(row_d['postURL']) == 'reddit'):
                r_cnt += 1
            else:
                other_cnt += 1
        return yt_cnt, r_cnt, other_cnt
            
    
    row_dl = logger.readCSV(CLIP_DOWNLOAD_LOG_CSV_PATH)
    
    num_attempts = len(row_dl)
    num_dl_success = _num_dl_success(row_dl)
    dl_success_ratio = num_dl_success / num_attempts 
    
    yt_cnt, r_cnt, other_cnt = _youtube_reddit_other_cnt(row_dl)
    
    overall_fail_reason_occ_d = _fail_reason_occ_d(row_dl)
    
    print('num_attempts: ', num_attempts)
    print('num_dl_success: ', num_dl_success)
    print('dl_success_ratio: ', dl_success_ratio)
    print('num youtube videos: ', yt_cnt, '  %', (yt_cnt / num_attempts) * 100)
    print('num reddit videos:  ', r_cnt, '  %', (r_cnt / num_attempts) * 100)
    print('num other videos:   ', other_cnt, '  %', (other_cnt / num_attempts) * 100)
    
    

    
    
    
    
    
    
if __name__ == '__main__':
    print_dl_report()
    print('done')