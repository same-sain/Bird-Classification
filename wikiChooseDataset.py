import requests
import pandas as pd
import json
from threading import Thread
import time
import csv

class FetchNum( Thread ) :
    def __init__(self, name ):
        Thread.__init__(self)
        self.name = name

    def fetch(self) : 
        try :
            res = requests.get("https://xeno-canto.org/api/2/recordings?query={}".format(self.name))
            return [ self.name, json.loads(res.content.decode())["numRecordings"] ]
        except :
            return "Error"
    
    def run(self) :
        result = self.fetch()
        if result != "Error" :
            print( self.name )
            with open('bird_data.csv', mode='a') as file:
                writer = csv.writer(file)
                writer.writerow(result)
    
def main() :
    fetchQueue = []
    df = pd.read_csv('./bird_names.csv')
    
    for name in df["name"] :
        fetchQueue.append( FetchNum(name) )
        
    for fetch in fetchQueue :
        fetch.start()
    
    for fetch in fetchQueue :
        fetch.join()
    
if __name__ == "__main__" :
    main()