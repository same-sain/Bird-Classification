import requests
import pandas as pd
import json
from urllib.request import urlretrieve
import os
import threading
import time

def main():
    last_processed_index = load_checkpoint()
    dir = os.listdir('./birdJson')

    for i in range(len(dir)):
        name = dir[i]
        data = open('./birdJson/{}'.format(name))
        datajson = json.load(data)
        path1 = './datasets/{}'.format(name[:-5])

        if not os.path.exists(path1):
            os.mkdir(path1)
    
        threads = []
        for j in range(last_processed_index, len(datajson)):   
            if datajson[j]['file'] == '':
                continue
            t = threading.Thread(target=download_file_with_retry, args=(dir[i][:-5], datajson[j]))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

def download_file_with_retry(bird_name, file_data):
    retry_interval = 10  # Retry interval in seconds
    while True:
        try:
            download_file(bird_name, file_data)
            break  # Break the loop if download is successful
        except Exception as e:
            print(f"Failed to download file, retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)

def download_file(bird_name, file_data):
    filesound = file_data['file']
    path = './datasets/{}/{}'.format(bird_name, file_data['file-name'])
    urlretrieve(filesound, path)
    save_checkpoint(file_data['index'] + 1)

def load_checkpoint():
    checkpoint_file = "checkpoint.txt"
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, "r") as f:
            return int(f.read())
    else:
        return 0

def save_checkpoint(index):
    checkpoint_file = "checkpoint.txt"
    with open(checkpoint_file, "w") as f:
        f.write(str(index))

if __name__ == "__main__":
    main()
