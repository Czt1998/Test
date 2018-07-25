# coding utf-8
import sys
import time
import urllib
from selenium import webdriver
from imp import reload
reload(sys)

driver1 = webdriver.PhantomJS(executable_path="./phantomjs")

def get_data(year):
    with open("./movie/" + str(year) + ".txt","r") as r:
        lines = r.readlines()
        for line in lines:
            line = line.replace('\n','')
            movie_name = line.split('')[0]
            movie_id = line.split('')[1]

            # 通过时光网url的特征，利用quoto将电影名拼接得到目标url
            pre_url = 'http://search.mtime.com/search/?q=' + urllib.request.quote(movie_name)
            print(pre_url)
            driver1.get(pre_url)
            time.sleep(1)
            # 利用xpath得到带有电影编号的链接
            urls = driver1.find_elements_by_xpath("//div[@class='main']/ul/li/h3/a")
            time.sleep(1)
            print(urls)
            print(len(urls))
            ff = 0
            # 如果找不到，则多找几次
            while len(urls) == 0:
                urls = driver1.find_elements_by_xpath("//div[@class='main']/ul/li/h3/a")  # 利用xpath得到带有电影编号的链接
                time.sleep(1)
                # ff为计数器，当重复次数超过11次则认为该电影不存在，写入文件手动判断是否为电影名错误
                ff += 1
                if (ff > 11):
                    with open("./movie_null.txt", "a+") as w:
                        w.writelines(movie_name + ' ' + movie_id)
                    break
            all_urls = [i.get_attribute("href") for i in urls]
            time.sleep(1)
            # 判断电影是否存在，若不存在则为名字不正确或者年份不正确
            count = 0
            for urls in all_urls:
                # 获得电影名与年份
                print(urls)
                driver1.get(urls)
                time.sleep(1)
                name = driver1.find_element_by_xpath("//div[@class='clearfix']/h1").text
                year_0 = driver1.find_element_by_xpath("//div[@class='clearfix']/p[@class='db_year']/a").text
                print(name)
                print(year)
                if name == movie_name and int(year_0) == int(year):
                    count = 1

                    try:
                        data = driver1.find_element_by_xpath("/html/body/div[3]/div[2]/div[3]/div/div[1]/div[2]/div/div[2]/a[3]").text
                        print(data)
                        movie_year = str(data).split("年")[0]
                        movie_month = str(data).split("年")[1].split("月")[0]
                        movie_day = str(data).split("年")[1].split("月")[1].split("日")[0]
                        with open("./movie/" + year_0 + "_data.txt","a+") as w:
                            w.writelines(movie_name + ' ' + movie_id + ' ' + movie_year + ' ' + movie_month + ' ' + movie_day + '\n')
                    except:
                        try:
                            data = driver1.find_element_by_xpath("/html/body/div[3]/div[2]/div[3]/div/div[1]/div[2]/div/div[2]/a[4]").text
                            print(data)
                            movie_year = str(data).split("年")[0]
                            movie_month = str(data).split("年")[1].split("月")[0]
                            movie_day = str(data).split("年")[1].split("月")[1].split("日")[0]
                            with open("./movie/" + year_0 + "_data.txt","a+") as w:
                                w.writelines(movie_name + ' ' + movie_id + ' ' + movie_year + ' ' + movie_month + ' ' + movie_day + '\n')
                        except:
                            data = driver1.find_element_by_xpath("/html/body/div[3]/div[2]/div[3]/div/div[1]/div[2]/div/div[2]/a[2]").text
                            print(data)
                            movie_year = str(data).split("年")[0]
                            movie_month = str(data).split("年")[1].split("月")[0]
                            movie_day = str(data).split("年")[1].split("月")[1].split("日")[0]
                            with open("./movie/" + year_0 + "_data.txt","a+") as w:
                                w.writelines(movie_name + ' ' + movie_id + ' ' + movie_year + ' ' + movie_month + ' ' + movie_day + '\n')
                    break
                else:
                    pass
            if count == 0:
                with open('./movie_failed_' + str(year) + '.txt', "a+")as w:
                    w.writelines("Fail in name" + movie_name)
                    w.write('\n')