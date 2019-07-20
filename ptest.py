

def add(a,b,c):
    return a+b +c

def fancy_print(s):
    print('{{{ ', s,'}}}')
    
def do_math_and_print(math_func, args):
    result = str(math_func(100, *args))
    fancy_print(result)
    
do_math_and_print(add, [2,3])
