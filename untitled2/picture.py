# codeing utf-8
import time
import sys
import pytesseract
from PIL import Image
from imp import reload
from selenium import webdriver
reload(sys)
reload(Image)
img = Image.open('./pic.png')
rangle = (934,470,1026,512)
jpg = img.crop(rangle)
jpg.show()