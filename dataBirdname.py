from bs4 import BeautifulSoup
import requests
import csv


def fetchBirdName(url : str) -> list[str] :
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    tables = soup.find_all("table")

    birdName = []

    for table in tables :
        dateName = table.find_all("i")
        for name in dateName :
            birdName.append(name.text)

    return birdName


def main():
    birdName = fetchBirdName("https://th.wikipedia.org/wiki/%E0%B8%A3%E0%B8%B2%E0%B8%A2%E0%B8%8A%E0%B8%B7%E0%B9%88%E0%B8%AD%E0%B8%99%E0%B8%81%E0%B8%97%E0%B8%B5%E0%B9%88%E0%B8%9E%E0%B8%9A%E0%B9%83%E0%B8%99%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B9%80%E0%B8%97%E0%B8%A8%E0%B9%84%E0%B8%97%E0%B8%A2")
    fields = [ 'id', 'name' ] 
    filename = "bird_names.csv"
    mydict = []

    with open( filename, 'w' ) as file:
        writer = csv.DictWriter(file, fieldnames=fields,lineterminator="\n")
        writer.writeheader()
        for i in range(len(birdName)): 
            writer.writerow({"id" : i , "name": birdName[i]})  # mydict in writerow
            # mydict = [{"id" : i , "name" : v }for i ,v in enumerate(birdName)]





if __name__ == "__main__" :
    main()













