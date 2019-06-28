import os



def is_path_creatable(pathname: str) -> bool:
    '''
    `True` if the current user has sufficient permissions to create the passed
    pathname; `False` otherwise.
    '''
    # Parent directory of the passed path. If empty, we substitute the current
    # working directory (CWD) instead.
    dirname = os.path.dirname(pathname) or os.getcwd()
    return os.access(dirname, os.W_OK)

# returns true if path could be created and ends with ext
def is_file_path_valid(path, extention = None):
    if not is_path_creatable(path):
        return False
    if extention != None and not path.endswith(extention):
        return False
    return True




print(is_file_path_valid('tryt1.m\4', 'mp4'))
