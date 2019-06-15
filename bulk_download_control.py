import subprocess

exe_path = "C:/Users/Brandon/Documents/Personal_Projects/reddit_comp/bulk_downloader_for_reddit-1.6.5-windows/bulk-downloader-for-reddit.exe "

# save_path = "C:/Users/Brandon/Documents/Personal_Projects/reddit_comp/vids_to_compile"

args = {'--directory' : "C:/Users/Brandon/Documents/Personal_Projects/reddit_comp/vids_to_compile"}


arg_str = ''
for key, val in args.items():
    arg_str += ' ' + key + ' ' + val




cmd = exe_path + arg_str + ' --NoDownload'
subprocess.call(cmd, shell=True)