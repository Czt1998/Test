# coding utf-8
from test import *
from get_data import *

def main():
    login(13612339624, 348673210)
    for year_0 in range(2010,2017):
        get_data(year_0)
        with open("./movie/" + str(year_0) + "_data.txt","r") as r:
            lines = r.readlines()
            for line in lines:
                line = line.replace('\n','')
                movie_name = line.split(' ')[0]
                movie_id = line.split(' ')[1]
                year = line.split(' ')[2]
                month = line.split(' ')[3]
                day = line.split(' ')[4]
                data = deal(movie_name,year,month,day)
                print(type(data))
                print(data)

if __name__ == '__main__':
    main()