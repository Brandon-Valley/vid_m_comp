import pool_clips_data_handler
from gui import Clip_Pool_Data

row_dl = pool_clips_data_handler.get_csv_row_dl()
cpd = Clip_Pool_Data.Clip_Pool_Data(row_dl)
#print('in ptest, )

for r in cpd.ratings_occ_str_l:
  print(r)

print(cpd.percent_below_avg_str)
