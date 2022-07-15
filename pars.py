import re
import time

import requests
import os
from bs4 import BeautifulSoup
import sqlite3
import random
import threading
import pyshorteners
from webbot import Browser

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

threading.TIMEOUT_MAX = 60 * 10.0

database = 'data.db'


class proxy():

    def update(self):
        while True:
            data = ''
            urls = ["https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&ssl=yes",
                    "https://www.proxy-list.download/api/v1/get?type=https&anon=elite"]
            for url in urls:
                data += requests.get(url).text

            self.splited += data.split("\r\n")  # scraping and splitting proxies
            time.sleep(600)

    def get_proxy(self):
        random1 = random.choice(self.splited)  # choose a random proxie
        return random1

    def FormatProxy(self):
        proxyOutput = {'https': 'https://' + self.get_proxy()}
        return proxyOutput

    def __init__(self):
        self.splited = []
        threading.Thread(target=self.update).start()
        time.sleep(3)


proxy1 = proxy() #proxies=proxy1.FormatProxy())

def get_url():
    conector = sqlite3.connect(database)
    cursor = conector.cursor()
    cursor.execute('SELECT url FROM urls')
    id_f = cursor.fetchall()
    urls = []
    for i in id_f:
        urls.append(i[0])
    return (urls)


def pars(log=False, url='http://anime.reactor.cc/new'):
    r = requests.get(url, timeout=200)
    if log:
        print(f"[log] Requests status: {r.status_code}")
    soup = BeautifulSoup(r.text, features="lxml")
    r.close()
    item = soup.find_all('a', {'class': 'prettyPhotoLink'})
    item2 = soup.find_all('a', {'class': 'video_gif_source'})
    item[len(item):] = item2

    links = []

    for i in item:
        lnk = str(i.get('href')).replace('full/', '')
        links.append(lnk)
        if log:
            print(f"[log] Link {lnk}")
    try:
        links.pop(0)
    except:
        pass
    return (links)


def web_dw(link, log=False):
    web = Browser(showWindow=False)

    options = webdriver.FirefoxOptions()
    options.add_argument("-profile")
    options.add_argument("bot_profile")
    firefox_capabilities = DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True

    options.headless = True

    driver = webdriver.Firefox(capabilities=firefox_capabilities, options=options)

    driver.get(link)
    time.sleep(4)

    htm = driver.page_source

    soup = BeautifulSoup(htm, features="lxml")
    item = soup.find_all('a', {'class': 'prettyPhotoLink'})
    item2 = soup.find_all('a', {'class': 'video_gif_source'})
    item[len(item):] = item2
    #print(item)
    links = []
    for i in item:
        lnk = str(i.get('href')).replace('full/', '')
        links.append(lnk)
    for i in links:
        #s = str(i[(i.rfind('-') + 1):])
        #r = requests.get(i, allow_redirects=True)
        thread = threading.Thread(target=dw, args=[i, log])
        thread.start()

    driver.close()
    del driver
    # web.go_to('http://joyreactor.cc/login')
    # web.type('diadern', id='signin_username')
    # web.type('n9z2s7NDkXq348H', id='signin_password')  # specific selection
    # time.sleep(5)
    # web.click('Войти')  # you are logged in ^_^
    # time.sleep(5)
    # web.new_tab(link)
    # #htm = web.find_elements()
    # #print(tabs)
    # web.switch_to_tab(2)
    # web.new_tab(link)
    # web.switch_to_tab(3)
    # htm = web.get_page_source()
    # #print(htm)
    # soup = BeautifulSoup(htm, features="lxml")
    # item = soup.find_all('a', {'class': 'prettyPhotoLink'})
    # item2 = soup.find_all('a', {'class': 'video_gif_source'})
    # item[len(item):] = item2
    # #print(item)
    # links = []
    # for i in item:
    #     lnk = str(i.get('href')).replace('full/', '')
    #     links.append(lnk)
    # for i in links:
    #     #s = str(i[(i.rfind('-') + 1):])
    #     #r = requests.get(i, allow_redirects=True)
    #     thread = threading.Thread(target=dw, args=[i, log])
    #     thread.start()
    # web.driver.quit()
    # del web


def dw(i, log=False):
    img_c = sqlite3.connect(database)
    cursor_i = img_c.cursor()
    if not 'http' in i:
        i = i.replace('//', 'http://')
    try:
        cursor_i.execute(f'INSERT INTO pic VALUES (?, ?)', (i, 'False'))
        img_c.commit()
        if log:
            print(f"{i} added!")
    except:
        if log:
            print(f"{i} was added last!")


def downloader(log=False, urls=[]):
    # global urls
    links = []
    if len(urls):
        urls_ = urls
    else:
        urls_ = get_url()
    for i in urls_:
        if 'joyreactor' in i:
            try:
                thread = threading.Thread(target=web_dw, args=[i, log])
                thread.start()
            except:
                pass
        else:
            try:
                links_ = smart_dw(log=log, link=i)#pars(log=log, url=i)
            except:
                links_ = []
            for i in links_:
                links.append(i)
    for i in links:
        # s = str(i[(i.rfind('-') + 1):])
        # r = requests.get(i, allow_redirects=True)
        thread = threading.Thread(target=dw, args=[i, log])
        thread.start()


def shrter(link):
    s = pyshorteners.Shortener()
    slnk = s.tinyurl.short(link)
    return (slnk)


def smart_dw(link, log = False, test = True):
    s2 = []
    #print(link)
    if 'yande.re' in link:
        r = requests.get(link)
        ht = r.text
        r.close()
        soup = BeautifulSoup(ht, features="lxml")
        item = soup.find_all('a', {"class": "thumb"})
        for i in item:
            # print(str(i.get("href")))
            r = requests.get(f'http://yande.re{str(i.get("href"))}')
            ht2 = BeautifulSoup(r.text, features="lxml")
            r.close()
            s2.append(str(ht2.find("img", {"id": "image"}).get('src')))

    elif 'rule34.xxx' in link:
        #print('rule!!!!!!')
        if link.startswith('http'):
            r = requests.get(link)
        else:
            r = requests.get(f'http://{link}')
        ht = r.text
        r.close()
        #print(ht)
        soup = BeautifulSoup(ht, features="lxml")
        item = soup.find_all('span', {"class": "thumb"})
        #print(item[5])
        for i in item:
            #print(str(i.get("href")))
            try:
                r = requests.get(f'https://rule34.xxx/{str(i.find("a").get("href"))}')
                ht2 = BeautifulSoup(r.text, features="lxml")
                r.close()
                s2.append(str(ht2.find("img", {"id": "image"}).get('src')))
            except:
                pass

    elif 'reactor' in link:
        s2 = pars(log=log, url=link)

    else:
        r = requests.get(link, timeout=200)
        ht = r.text
        r.close()

        patt = r'((http(s|)?:\/\/)?([\/\w-]{1,200}\.[\/\w-]{1,200})*[jpg|png|jpeg])'

        # print(ht)

        f = re.findall(patt, ht)
        s1 = list(set(f))
        for j in s1:
            # print(j)
            for i in j:
                lnk = str(i.get('href'))
                if lnk.startswith('http') and (lnk.endswith('jpg')
                                               or lnk.endswith('png')
                                               or lnk.endswith('jpeg')
                                               or lnk.endswith('webm')
                                               or lnk.endswith('gif')):
                    s2.append(lnk)
                lnk = str(i.get('src'))
                if lnk.startswith('http') and (lnk.endswith('jpg')
                                               or lnk.endswith('png')
                                               or lnk.endswith('jpeg')
                                               or lnk.endswith('webm')
                                               or lnk.endswith('gif')):
                    s2.append(lnk)
    s2 = list(set(s2))
    if log:
        print(s2)
    if test:
        return s2
    else:
        for i in s2:
            #print(i)
            thread = threading.Thread(target=dw, args=[i, log])
            thread.start()


#downloader(log=True, urls=['https://rule34.xxx/index.php?page=post&s=list&tags=meru_%28merunyaa%29+',])

# print(downloader(log=True))
#print(pars(log=True, url='http://anime.reactor.cc/tag/Anime+Ero+Pussy'))
#web_dw(log=True, link='http://fapreactor.com/tag/Demonstration+Хентай/new')
