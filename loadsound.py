import requests
import pandas as pd
import json
from urllib.request import urlretrieve
import os


def main() :
    last_processed_index = load_checkpoint()
    
    dir = os.listdir('./birdJson')
    
    for i in range(len(dir)) :
        name = dir[i]
        data = open('./birdJson/{}'.format(name))
        datajson = json.load(data)
        path1 = './datasets/{}'.format(name[:-5]) 

        if not os.path.exists(path1) :
            os.mkdir(path1)
        
        for j in range(last_processed_index , len(datajson)) :
            if datajson[j]['file'] == '':
                continue

            filesound = datajson[j]['file']
            path = './datasets/{}/{}'.format(dir[i][:-5] , datajson[j]['file-name'])
            urlretrieve(filesound, path)
            save_checkpoint(j + 1)  
        

def load_checkpoint():
    checkpoint_file = "checkpoint.txt"
    if  os.path.exists(checkpoint_file):
        with open(checkpoint_file, "r") as f:
            return int(f.read())
    else:
        return 0 

def save_checkpoint(index):
    checkpoint_file = "checkpoint.txt"
    with open(checkpoint_file, "w") as f:
        f.write(str(index))


if __name__ == "__main__" :
    main()
