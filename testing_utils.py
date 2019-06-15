

def print_str_wo_error(str):
    output = ''
    
    for char in str:
        try:
            print(char, end = '')
        except:
            print('[' + format(ord(char), "x") + ']', end = '')
            
    print('')
    
