import json
import os.path


# changes values of headers already in the file, and appends lines with new headers to the end, or creates new file if dosn't already exist
def log_vars(log_dict, json_file_path):
    if os.path.isfile(json_file_path): 
        json_data = read(json_file_path)
    else:
        json_data = {}

    for log_header, log_val in log_dict.items():
        json_data[log_header] = log_val

    write(json_data, json_file_path)
                
    
    
def write(data, output_file_path, indent = 4):
    with open(output_file_path, 'w') as outfile:  
        json.dump(data, outfile, indent = indent)


def read(json_file_path):
    with open(json_file_path, "r") as read_file:
        data = json.load(read_file)
    return data
    
    
    
# data = {}  
# data['people'] = []  
# data['people'].append({  
#     'name': 'Scott',
#     'website': 'stackabuse.com',
#     'from': 'Nebraska'
# })
# data['people'].append({  
#     'name': 'Larry',
#     'website': 'google.com',
#     'from': 'Michigan'
# })
# data['people'].append({  
#     'name': 'Tim',
#     'website': [1,2,3,4],
#     'from': 'Alabama'
# })
# 
#     
# write(data,'json_test.json')
# print(read('json_test.json'))
# print(read('project_vars.json'))


var_data = {'a': 5,
            'b': 6}

#log_vars(var_data, 'test.json')
log_vars({'c': 11}, 'test.json')
