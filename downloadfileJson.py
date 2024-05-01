import requests
import pandas as pd
import json
from urllib.request import urlretrieve
import os

def fetch(name , page = 1)  :
    res = requests.get("https://xeno-canto.org/api/2/recordings?query={}&page={}".format(name,page))
    return json.loads(res.content.decode())


def main():
    with open( './bird.json' ) as birds_json:
        birdNames = json.load( birds_json )
    for bird in birdNames:
        sciName = bird['sci']
        try:
            results = fetch( sciName )
            recordings = results.get("recordings", [ ] )
            numPages = int( results.get("numPages", "1" ) )
            if ( numPages >= 2 ): 
                recordings.extend( fetch( sciName, 2 )["recordings"] )
            print( recordings )
            filename = f"./birdJson/{sciName}.json"
            with open( filename, "w" ) as f_json:
                json.dump( recordings, f_json )
        except requests.exceptions.RequestException as e:
            print( f"Error fetching recordings for { sciName } : { e }")
    
    # for i in data :
    #     nameSci = i['sci']
    #     res1 = fetch(nameSci,1)
    #     if res1['numPages'] >= 2 :
    #         res2 = fetch(nameSci,2)
    #         print(res2)
    #         json_str1 = json.dumps(res2)
    #         with open('./birdJson/{}2.json'.format(nameSci), 'w') as f:
    #             f.write(json_str1)
            
    #     json_str = json.dumps(res1)
    #     with open('./birdJson/{}.json'.format(nameSci), 'w') as f:
    #         f.write(json_str)
        


        

'''

    for i in data :
        birdjson = open('./birdJson/{}'.format(i))
        datajson = json.load(birdjson)
        # for m in range(int(datajson['numRecordings'])) :
        if int(datajson['numRecordings']) != len(datajson['recordings']) :
            print(datajson['numRecordings'],len(datajson['recordings']),datajson['numPages'])

        birdjson.close()
'''



if __name__ == "__main__" :
    main()

