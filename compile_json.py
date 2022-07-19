import json, os
temp_list=[]
def update_main_json(fpath, temp, count):
    with open(fpath, 'r') as a:
        json_data = json.load(a)        #loading the current json file into a temp dict
    for x in json_data.values():
        if(x not in temp_list):
            temp.update({count:x})
            count+=1
            temp_list.append(x)          #appending the new product info dicts to the temp dict
    return temp, count
    
def compile_json(filename):
    folder='C:\Python\\relu-test'
    temp={}
    count=0
    files_path = [os.path.basename(x) for x in os.listdir(folder)]      #storing names of all the files in current folder
    for x in files_path:
        if('filenumber' in x):      #checking if the current file is one of the temp json files
            print(x)
            temp, count=update_main_json(folder+'\\'+x, temp, count)        #updating temp recursively
            os.remove(f'{folder}\\{x}')

    with open(f'C:\Python\\relu-test\\{filename}.json', 'w') as f:
        f.write(json.dumps(temp, indent=4))             #dumping all the product info dicts into a single file