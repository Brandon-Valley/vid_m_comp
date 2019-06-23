import datetime


import json_logger

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
            
            if self.am_pm == 'AM':
                hour += 0
            else: 
                hour += 12
            return (hour, min, 0)
            
        time = _make_time_tup()
        return datetime.datetime(self.dl_date.year, self.dl_date.month, self.dl_date.day, time[0], time[1], time[2])
        








# 
# 
# def get_next_dl_event_data_d():
#     def _make_dl_event_data_d(dl_schedule_d):
#          pass
#          
#          
#          
#     dl_schedule_dl = json_logger.read(DL_SCHEDULE_JSON_PATH)
#     print(dl_schedule_dl)
#      
#     dl_event_data_dl = []
#     for dl_schedule_d in dl_schedule_dl:
#         dl_event_data_dl.append(_make_dl_event_data_d(dl_schedule_d))
#          
#     print(dl_event_data_dl)



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


def main():
    dl_schedule_dl = json_logger.read(DL_SCHEDULE_JSON_PATH)
    dl_event_l = build_dl_event_l(dl_schedule_dl)
#     for dl_event in dl_event_l:
#         print(dl_event.event_name, dl_event.dl_date, dl_event.dl_datetime)
        
    scheduled_dl_event_l = get_scheduled_dl_event_l(dl_event_l)
    for dl_event in scheduled_dl_event_l:
        print(dl_event.event_name, dl_event.dl_date, dl_event.dl_datetime)


if __name__ == '__main__':
    main()
#     next_dl_event_data_d = get_next_dl_event_data_d()
#     print(next_dl_event_data_d)
