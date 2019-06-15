import pool_clips_data_handler
from gui import clip_order

def main():
    rated_clip_path_dl = pool_clips_data_handler.get_rated_clip_path_dl()
    ordered_clip_path_l = clip_order.order_rated_clip_paths(rated_clip_path_dl, 'balanced_with_padding')



