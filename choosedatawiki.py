import json 
import pandas as pd 
import csv
import requests
import os


def fetch(name):
    res = requests.get("https://xeno-canto.org/api/2/recordings?query={}".format(name))
    return json.loads(res.content.decode())


def main(start_index=0):
    df = pd.read_csv('./bird_names.csv')

    for i, bird_name in enumerate(df['name'][start_index:], start=start_index):
        res = fetch(bird_name)
        filenames = "bird_count_sound.csv"
        dataname = [bird_name, res['numRecordings']]
        print(bird_name, res['numRecordings'])

        with open(filenames, mode='a') as file:
            writer = csv.writer(file)
            writer.writerow(dataname)
        save_checkpoint(i + 1)

def load_checkpoint():
    checkpoint_file = "checkpointname.txt"
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, "r") as f:
            return int(f.read())
    else:
        return 0

def save_checkpoint(index):
    checkpoint_file = "checkpointname.txt"
    with open(checkpoint_file, "w") as f:
        f.write(str(index))

if __name__ == '__main__':
    start_index = load_checkpoint()
    print(f"Resuming from index: {start_index}")
    main(start_index)
