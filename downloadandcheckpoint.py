import requests
import pandas as pd
import json
from urllib.request import urlretrieve
import os
from threading import Thread, Lock
import time

checkpoint_lock = Lock()

class DownloadBird(Thread):
    def __init__(self, bird, data, index):
        Thread.__init__(self)
        self.bird = bird
        self.data = data
        self.index = index

    def downloadRetryWhen503(self, url, path):
        retries = 5
        while retries > 0:
            try:
                urlretrieve(url, path)
                break
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 503:
                    retries -= 1
                    print(f"HTTPError 503: Retrying... {retries} attempts left")
                    time.sleep(5)
                else:
                    print(f"HTTPError: {e}")
                    break
            except Exception as e:
                print(f"Error: {e}")
                break

    def run(self):
        for i in range(self.index, len(self.data)):
            if self.data[i]['file'] == '':
                continue

            filesound = self.data[i]['file']
            path = f'/datasets/{self.bird}/{self.data[i]["file-name"]}'
            
            self.downloadRetryWhen503(filesound, path)
            
            print(f"Downloaded {path}", end='\r')
            self.save_checkpoint(i + 1)

    def save_checkpoint(self, index):
        with checkpoint_lock:
            with open('./checkpoint/{}'.format(f"checkpoint_{self.bird}.txt"), "w") as f:
                f.write(str(index))

def load_checkpoint(bird):
    checkpoint_file = f"checkpoint_{bird}.txt"
    if os.path.exists(checkpoint_file):
        with open('./checkpoint/{}'.format(checkpoint_file), "r") as f:
            return int(f.read().strip())
    else:
        return 0

def main():
    # base_dir = '/content/Bird-Classification'
    json_dir = os.path.join( 'birdJson')#base_dir
    dataset_dir = os.path.join( 'datasets') #base_dir

    
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)

    downloadQueue = []
    for file in os.listdir(json_dir):
        bird = file[:-5]
        print(bird)
        
        bird_folder = os.path.join(dataset_dir, bird)
        if not os.path.exists(bird_folder):
            os.mkdir(bird_folder)

        with open(os.path.join(json_dir, file)) as f:
            data = json.load(f)

        last_index = load_checkpoint(bird)
        downloadQueue.append(DownloadBird(bird, data, last_index))

    for download in downloadQueue:
        download.start()

    for download in downloadQueue:
        download.join()

if __name__ == "__main__":
    main()
