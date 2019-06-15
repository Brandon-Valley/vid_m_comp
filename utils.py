# self.duration: 72 --> '1:12'
def sec_to_min_str(total_sec):
    minutes = int(total_sec / 60)
    seconds = int(total_sec % 60)
    sec_str = str(seconds)
    if len(sec_str) < 2:
        sec_str = '0' + sec_str
    return str(minutes) + ':' + sec_str
    
    
    
def get_cur_row_num(row_dl):
        for row_num, row_d in enumerate(row_dl):
            if row_d['current'] == '1':
                return row_num
        return 1