
from typing import List
from bs4 import BeautifulSoup
import requests
import csv

def fetchBirds( url : str ) -> List[str] :
    res = requests.get( url )
    soup = BeautifulSoup( res.content, "html.parser" )
    tables = soup.find_all( 'table' )

    birdNames = []

    for table in tables:
        elements = table.find_all( 'i' )
        for element in elements:
            birdNames.append( element.text )

    return birdNames


def main():
    birdNames = fetchBirds( 'https://th.wikipedia.org/wiki/%E0%B8%A3%E0%B8%B2%E0%B8%A2%E0%B8%8A%E0%B8%B7%E0%B9%88%E0%B8%AD%E0%B8%99%E0%B8%81%E0%B8%97%E0%B8%B5%E0%B9%88%E0%B8%9E%E0%B8%9A%E0%B9%83%E0%B8%99%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B9%80%E0%B8%97%E0%B8%A8%E0%B9%84%E0%B8%97%E0%B8%A2' )
    fields = [ 'id', 'name' ] 
    filename = "bird_names.csv"

    with open( filename, 'w' ) as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()


if __name__ == "__main__":
    main()