import requests
import pandas as pd
import json
def fetch(name) :
    res = requests.get("https://xeno-canto.org/api/2/recordings?query={}".format(name))  
    return json.loads(res.content.decode())





def main():
    df = pd.read_csv("./bird_names.csv")

if __name__ == "__main__" :
    main()
