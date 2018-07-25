# coding utf-8
import time
import sys
import shutil
import pytesseract
import re
import os
from PIL import Image
from imp import reload
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
reload(sys)
from test import *
from get_data import *

def main():
    # login(15625125392, 348673210)
    # for year_0 in range(2010,2017):
    #     get_data(year_0)
    #     with open("./movie/" + str(year_0) + "_data.txt","r") as r:
    #         lines = r.readlines()
    #         for line in lines:
    #             line = line.replace('\n','')
    #             movie_name = line.split(' ')[0]
    #             movie_id = line.split(' ')[1]
    #             year = line.split(' ')[2]
    #             month = line.split(' ')[3]
    #             day = line.split(' ')[4]
    # data = deal("复仇者联盟3",2018,4,7)
    # print(type(data))
    # print(data)
    # os.mkdir("./Test")
    shutil.rmtree("./Test")

if __name__ == '__main__':
    main()