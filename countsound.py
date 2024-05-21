import pandas as pd 
import os

def main() :
    dir = os.listdir('./birdJson')
    
    for i in dir:
        dirs = open('./birdJson/{}'.format(i))
        for j in dirs :
            print(j[1])
            


if __name__ == '__main__' :
    print(main())