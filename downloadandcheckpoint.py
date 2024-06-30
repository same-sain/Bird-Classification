import requests
import pandas as pd
import json
from urllib.request import urlretrieve
import os
from threading import Thread
import time

class DownloadBird(Thread):
    def __init__(self, bird, data, index):
        Thread.__init__(self)
        self.bird = bird
        self.data = data
        self.index = index

    def downloadRetryWhen503(self, url, path):
        try:
            urlretrieve(url, path)
        except requests.exceptions.HTTPError as e:
            print(f"HTTPError: {e}")
            time.sleep(5)

    def run(self):
        for i in range(self.index, len(self.data)):
            if self.data[i]['file'] == '':
                continue

            filesound = self.data[i]['file']
            path = f'./datasets/{self.bird}/{self.data[i]["file-name"]}'
            self.downloadRetryWhen503(filesound, path)
            print(f"Downloaded {path}", end='\r')
            save_checkpoint( i + 1)

def save_checkpoint(index):
    with open("checkpoint.txt", "w") as f:
        f.write(str(index))

def load_checkpoint():
    if os.path.exists("checkpoint.txt"):
        with open("checkpoint.txt", "r") as f:
            return int(f.read().strip())
    else:
        return 0
    
def main():
    dirs = os.listdir('./birdJson')

    downloadQueue = []    

    for dir in dirs:
        dir = dir[:-5]
        folder = './datasets/{}'
        if not os.path.exists(folder.format(dir)):
            os.mkdir(folder.format(dir))
        data = json.load(open(f'./birdJson/{dir}.json'))
        last_index = load_checkpoint()
        downloadQueue.append(DownloadBird(dir, data, last_index))

    for download in downloadQueue:
        download.start()

    for download in downloadQueue:
        download.join()



if __name__ == "__main__":
    main()
