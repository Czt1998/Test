# codeing utf-8
import time
import sys
import pytesseract
import re
import os
import shutil
import random
import numpy as np
from PIL import Image
from imp import reload
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
reload(sys)
driver = webdriver.Chrome()

path=os.getcwd()

def login(name, passwd):
    url = 'http://index.baidu.com/?from=pinzhuan#/'
    # 这里可以用Chrome、Phantomjs等，如果没有加入环境变量，需要指定具体的位置
    driver.maximize_window()
    driver.get(url)
    print('开始登录')
    time.sleep(3)
    login_tag = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div[1]/div[4]/span/span")
    login_tag.click()
    time.sleep(3)
    name_field = driver.find_element_by_xpath("//*[@id='TANGRAM__PSP_4__userName']")
    name_field.send_keys(name)
    time.sleep(3)
    passwd_field = driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_4__password"]')
    passwd_field.send_keys(passwd)
    # yanzheng = driver.find_element_by_xpath("//*[@id='TANGRAM__PSP_4__verifyCodeImg']")
    # pic = yanzheng.get_attribute("src")
    # print(pic)
    # driver1.get(pic)
    time.sleep(10)
    # driver.save_screenshot('./pic.png')
    # rangle = (934, 470, 1026, 512)
    # img = Image.open('./pic.png')
    # jpg = img.crop(rangle)
    # jpg.save('./picc.png')
    # im = Image.open('./picc.png')
    # text = pytesseract.image_to_string(im)
    # print(text)
    # yanzheng = driver.find_element_by_xpath("//*[@id='TANGRAM__PSP_4__verifyCode']")
    # yanzheng.send_keys(text)
    login_button = driver.find_element_by_id('TANGRAM__PSP_4__submit')
    login_button.click()
    time.sleep(3)
def deal(name,year,month,day):
    try:
        driver.find_element_by_xpath("//*[@id='search-input-form']/input[3]").clear()
        driver.find_element_by_xpath("//*[@id='search-input-form']/input[3]").send_keys(name)
        driver.find_element_by_xpath("//*[@id='home']/div[2]/div[2]/div/div[1]/div/div[2]/div/span/span").click()
    except:
        driver.find_element_by_xpath("//*[@id='schword']").clear()
        driver.find_element_by_xpath("//*[@id='schword']").send_keys(name)
        driver.find_element_by_xpath("//*[@id='schsubmit']").click()
    time.sleep(5)
    fyear,fmonth,ayear,amonth=CalculateDate(year,month)
    # 点击网页上的开始日期
    driver.maximize_window()
    driver.find_elements_by_xpath("//div[@class='box-toolbar']/a")[6].click()
    driver.find_elements_by_xpath("//span[@class='selectA yearA']")[0].click()
    driver.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#" + str(fyear) + "']").click()
    driver.find_elements_by_xpath("//span[@class='selectA monthA']")[0].click()
    driver.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#" + str(fmonth) + "']").click()
    # 选择网页上的截止日期
    driver.find_elements_by_xpath("//span[@class='selectA yearA']")[1].click()
    driver.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#" + str(ayear) + "']").click()
    driver.find_elements_by_xpath("//span[@class='selectA monthA']")[1].click()
    driver.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#" + str(amonth) + "']").click()
    driver.find_element_by_xpath("//input[@value='确定']").click()
    time.sleep(2)
    # 月份-日字典
    Monthdict = {'01': 31, '02': 28, '03': 31, '04': 30, '05': 31, '06': 30, '07': 31, '08': 31, '09': 30, '10': 31,
            '11': 30, '12': 31, '1': 31, '2': 28, '3': 31, '4': 30, '5': 31, '6': 30, '7': 31, '8': 31, '9': 30}
    # 闰年处理
    if int(year) == 2012 or int(year) == 2016:
        Monthdict['02'] = 29
    return CollectIndex(Monthdict,fyear,fmonth,day,name)

def CalculateDate(year, month):
        if year == '2010':
            fyear = 2011
            fmonth = '01'
        else:
            fyear = year
            if int(month) == 1:
                fmonth = '12'
                fyear = str(int(year) - 1)
            else:
                fmonth = str(int(month) - 1)
        if len(fmonth) < 2:
            fmonth = '0' + fmonth
        if year == '2010':
            ayear = 2011
            amonth = '03'
        else:
            ayear = year
            if int(month) + 1 == 13:
                amonth = '01'
                ayear = str(int(year) + 1)
            else:
                amonth = str(int(month) + 1)
        if len(amonth) < 2:
            amonth = '0' + amonth
        return fyear, fmonth, ayear, amonth

def CollectIndex(Monthdict, fyear, fmonth, day, name):
        # 初始化输出String
        OutputString = str(name.encode("utf-8")) + '\n'
        x_0 = 1
        y_0 = 1
        # 根据起始具体日子计算鼠标的初始位置
        # 一日=13.51 例如,上映日期为7.20日 则x起始坐标为1+13.51*19
        if str(fyear) != '2011':
            ran = Monthdict[fmonth] + int(day) - 32
            if ran < 0:
                ran = 0.5
            x_0 = x_0 + 13.51 * ran
        else:
            day = 1
        xoyelement = driver.find_elements_by_css_selector("#trend rect")[2]
        ActionChains(driver).move_to_element_with_offset(xoyelement, x_0, y_0).perform()
        for i in range(61):
            # 计算当前得到指数的时间
            if int(fmonth) < 10:
                fmonth = '0' + str(int(fmonth))
            if int(day) >= Monthdict[str(fmonth)] + 1:
                day = 1
                fmonth = int(fmonth) + 1
                if fmonth == 13:
                    fyear = int(fyear) + 1
                    fmonth = 1
            day = int(day) + 1
            time.sleep(0.5)
            # 获取Code
            code = GetTheCode(fyear, fmonth, day, name, path, xoyelement, x_0, y_0)
            # ViewBox不出现的循环
            cot = 0
            jud = True
            # print code
            while (code == None):
                cot += 1
                code = GetTheCode(fyear, fmonth, day, name, path, xoyelement, x_0, y_0)
                if cot >= 6:
                    jud = False
                    break
            if jud:
                anwserCode = code.group()
                print(anwserCode)
            else:
                anwserCode = str(-1)
                if int(day) < 10:
                    day = '0' + str(int(day))
                if int(fmonth) < 10:
                    fmonth = '0' + str(int(fmonth))
            OutputString += str(fyear) + '-' + str(fmonth) + '-' + str(int(day) - 1) + ':' + str(anwserCode) + ','
            x_0 = x_0 + 13.51
        OutputString += ']\n'
        print(OutputString)
        return OutputString

def GetTheCode(fyear,fmonth,day,name,path,xoyelement,x_0, y_0):
    ActionChains(driver).move_to_element_with_offset(xoyelement, x_0, y_0).perform()
    #鼠标重复操作直到ViewBox出现
    cot1=0
    while (ExistBox(driver)==False):
        cot1+=1
        ActionChains(driver).move_to_element_with_offset(xoyelement, x_0, y_0).perform()
        if ExistBox(driver)==True:
            break
        if cot1>=6:
            return None
    time.sleep(1)
    Create_folder()
    imgelement = driver.find_element_by_xpath('//div[@id="viewbox"]')
    locations = imgelement.location
    printString = str(fyear) + "-" + str(fmonth) + "-" + str(day)
    # 找到图片位置
    l = len(name)
    if l > 8:
        l = 8
    rangle = (int(int(locations['x'])) + l * 10 + 38, int(int(locations['y'])) + 28,
              int(int(locations['x'])) + l * 10 + 38 + 75,
              int(int(locations['y'])) + 56)
    #保存截图
    driver.save_screenshot(str(path) + "/raw/" + printString + ".png")
    img = Image.open(str(path) + "/raw/" + printString + ".png")
    if locations['x'] != 0.0:
         #按Rangle截取图片
        jpg = img.crop(rangle)
        imgpath = str(path) + "/crop/" + printString + ".jpg"
        jpg.save(imgpath)
        jpgzoom = Image.open(str(imgpath))
        #放大图片
        (x, y) = jpgzoom.size
        x_s = 60 * 10
        y_s = 20 * 10
        out = jpgzoom.resize((x_s, y_s), Image.ANTIALIAS)
        out.save(path + "/zoom/" + printString, 'jpeg', quality=95)
        image = Image.open(path + "/zoom/" + printString )
        #识别图片
        code = pytesseract.image_to_string(image)
        regex = "\d+"
        pattern = re.compile(regex)
        dealcode = code.replace("S", '5').replace(" ", "").replace(",", "").replace("E", "8").replace(".", ""). \
            replace("'", "").replace(u"‘", "").replace("B", "8").replace("\"", "").replace("I", "1").replace(
            "i", "").replace("-", ""). \
            replace("$", "8").replace(u"’", "").strip()
        match = pattern.search(dealcode)
        Delete_folder()
        return match
    else:
        Delete_folder()
        return None

def ExistBox(browser):
    try:
        browser.find_element_by_xpath('//div[@id="viewbox"]')
        return True
    except:
        return False

def Create_folder():
    os.mkdir("./crop")
    os.mkdir("./raw")
    os.mkdir("./zoom")

def Delete_folder():
    shutil.rmtree("./crop")
    shutil.rmtree("./raw")
    shutil.rmtree("./zoom")
