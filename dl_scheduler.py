import datetime
import time
import os
import subprocess 



import json_logger
# import download_vids


DL_SCHEDULE_JSON_PATH = 'dl_schedule.json'

DAYS_OF_THE_WEEK_L = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saterday', 'Sunday']







class Download_Event():
    def __init__(self, dl_schedule_d):
        self.event_name     = dl_schedule_d['event_name']
        self.schedule_event = dl_schedule_d['schedule_event']
        self.subreddit_l    = dl_schedule_d['subreddit_l']
        self.day            = dl_schedule_d['day']
        self.time           = dl_schedule_d['time']
        self.am_pm          = dl_schedule_d['am_pm']
        
        self.dl_date        = self.get_dl_date()
        self.dl_datetime    = self.get_dl_datetime()
        
    def descrip_str(self):
        return self.event_name + ': at ' + self.time + ' ' + self.am_pm + ' on ' + self.day + ' with the following subreddits: ' + str(self.subreddit_l)
        
    def sec_until_dl(self):
        cur_datetime = datetime.datetime.now()
        return (self.dl_datetime - cur_datetime).seconds
        
        
    def get_dl_date(self):
        def _next_weekday(d, weekday):
            days_ahead = weekday - d.weekday()
            if days_ahead <= 0: # Target day already happened this week
                days_ahead += 7
            return d + datetime.timedelta(days_ahead)
        
        cur_date = datetime.datetime.now().date()
        day_index = DAYS_OF_THE_WEEK_L.index(self.day)
        return _next_weekday(cur_date, day_index)
    
    
    def get_dl_datetime(self):
        def _make_time_tup():
            split_time_str_l = self.time.split(':')
            hour = int(split_time_str_l[0])
            min  = int(split_time_str_l[1])
            
            
            if   self.am_pm == 'AM' and self.time.startswith('12'):
                hour -= 12
            elif self.am_pm == 'AM' or (self.am_pm == 'PM' and self.time.startswith('12')):
                hour += 0
            else: 
                hour += 12
            return (hour, min, 0)
            
        time = _make_time_tup()
        #print('in dl_sch, (self.dl_date.year, self.dl_date.month, self.dl_date.day, time[0], time[1], time[2]): ', (self.dl_date.year, self.dl_date.month, self.dl_date.day, time[0], time[1], time[2]))
        return datetime.datetime(self.dl_date.year, self.dl_date.month, self.dl_date.day, time[0], time[1], time[2])
        



def build_dl_event_l(dl_schedule_dl):
    dl_event_l = []
    for dl_schedule_d in dl_schedule_dl:
        dl_event_l.append(Download_Event(dl_schedule_d))
    return dl_event_l

def get_scheduled_dl_event_l(dl_event_l):
    scheduled_dl_event_l = []
    for dl_event in dl_event_l:
        if dl_event.schedule_event == True:
            scheduled_dl_event_l.append(dl_event)
    return scheduled_dl_event_l

def get_soonest_dl_event(scheduled_dl_event_l):
    def _sec_diff(datetime_1, datetime_2):
        return (datetime_1 - datetime_2).seconds
        
        
    cur_dt = datetime.datetime.now()
    soonest_dl_event = scheduled_dl_event_l[0]
    
    for dl_event in scheduled_dl_event_l[0:]:
        if _sec_diff(dl_event.dl_datetime, cur_dt) < _sec_diff(soonest_dl_event.dl_datetime, cur_dt):
            soonest_dl_event = dl_event
    return soonest_dl_event
        
        

    
    
        

def main():
    os.chdir('C:\\Users\\Brandon\\Documents\\Personal_Projects\\vid_m_comp') # not sure if this is needed for startup folder method
    
    dl_schedule_dl = json_logger.read(DL_SCHEDULE_JSON_PATH)
    dl_event_l = build_dl_event_l(dl_schedule_dl)
#     for dl_event in dl_event_l:
#         print(dl_event.event_name, dl_event.dl_date, dl_event.dl_datetime)
        
    scheduled_dl_event_l = get_scheduled_dl_event_l(dl_event_l)

    
    if len(scheduled_dl_event_l) == 0:
        print('no dl events scheduled')
    else:
        soonest_dl_event = get_soonest_dl_event(scheduled_dl_event_l)
        
        print('The next download event is: ', soonest_dl_event.descrip_str())
        wait_sec = soonest_dl_event.sec_until_dl()
        print('sleeping for', wait_sec, 'seconds...')
        time.sleep(wait_sec)
        import download_vids
        download_vids.download_vids(300, soonest_dl_event.subreddit_l, 'overwrite')
        main()
        
        
    

if __name__ == '__main__':
    main()
#     next_dl_event_data_d = get_next_dl_event_data_d()
#     print(next_dl_event_data_d)
