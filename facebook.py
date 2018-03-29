#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018.03.09
Finished on 
@author: Wang Yuntao
"""

import time
from random import randint
from crawl import *
from bs4 import BeautifulSoup
from selenium import webdriver

try:
    import facepy
except ImportError as e:
    print("pip install facepy please")
    print(e)

"""
    function:
        log_in(_email="", _password="")                                                         Facebook登录
        page_refresh(_browser, 
            _url="https://www.facebook.com/groups/frontbird/photos/", _number=10)               页面下拉刷新
            
        
"""

token = "EAACEdEose0cBAPRnHwpIR4lG3JZCsiZAKrL9vTanJ1OsFJ7gcnu5ki3QH9639OHproIdZCQ8Bo0DNZAqbcbe" \
        "TnoRBF6ZCqKIoEfR24BMyxZC6JenZC8gLrtZAlXWZATMu5BG3k4dwNZCHNaQZAdJ1rqM7GoawbFqzmHbZBJ7c43" \
        "i6gSSGFq4GGPNNCkOZARCb6nm6q32JsKUgZAcSvnZC8xwTWsdpjRtm9B2RZBfJgQZD"


def make_request(_id="me"):
    _request = _id + " "

    return _request


def get_response_from_facebook(_request):
    url_root = "http://graph.facebook.com/v2.12/"
    _url = url_root + _request
    response = requests.get(_url, {"access_token": token})

    return response


def log_in(_email="", _password=""):
    """
    facebook log in via webdriver
    :param _email: the email for logging
    :param _password: password
    :return: a browser object
    """
    _url = "https://www.facebook.com/"
    timeout = randint(1, 4)
    _browser = webdriver.Chrome()
    _browser.get(_url)
    email_element = _browser.find_element_by_id('email')
    email_element.send_keys(_email)
    time.sleep(timeout)
    password_element = _browser.find_element_by_id('pass')
    password_element.send_keys(_password)
    time.sleep(timeout)
    login = _browser.find_element_by_id('loginbutton')
    login.click()

    return _browser


def page_refresh(_browser, _url="https://www.facebook.com/groups/frontbird/photos/", _number=1):
    """
    dynamic refresh of pages
    :param _browser: browser object
    :param _url: url
    :param _number: the number of downward slide
    :return:
    """
    _browser.get(_url)
    _photos_link = list()
    timeout = randint(2, 8)
    for i in range(_number):
        _browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(timeout)
    source = _browser.page_source
    soup = BeautifulSoup(source, "html.parser")
    # for data in soup.find_all(class_="uiMediaThumb uiScrollableThumb uiMediaThumbLarge"):
    for data in soup.find_all(class_="uiMediaThumb _6i9 uiMediaThumbMedium"):
        _photos_link.append(data.get("href"))

    return _photos_link


def get_picture_info(_browser, _link):
    _browser.get(_link)
    _source = _browser.page_source
    soup = BeautifulSoup(_source, "html.parser")
    images_info = dict()
    # 获取当前图片的url链接，尺寸，发布时间，对应的文字
    pictures = soup.find_all("img", {"class": "spotlight"})
    for picture in pictures:
        size = picture.get("style")
        if size is not None:
            href = picture.get("src")
            publish_time = soup.find("span", {"id": "fbPhotoSnowliftTimestamp"})
            date = publish_time.a.abbr.get("data-utime")
            text_object = soup.find("span", {"class": "hasCaption"})
            if text_object is not None:
                text = text_object.text
            else:
                text = []

            print("href:", href)
            print("size:", size)
            print("data:", date)
            print("text:", text)

            images_info.update({"href": href})
            images_info.update({"size": size})
            images_info.update({"date": date})
            images_info.update({"text": text})
        else:
            continue

    return images_info


def image_download(_browser, _photo_link):
    pass


def images_download(_browser, _photos_link, images_folder="/images"):
    if os.path.exists(images_folder):
        os.mkdir(images_folder)
    for i in range(0, len(_photos_link)):
        if i == 10:
            time.sleep(randint(2, 10))

        picture_link = get_picture_info(_browser, _photos_link[i])
        print(type(picture_link), picture_link)
        try:
            _url = picture_link[0]
            print(_url, type(_url))
            response = requests.get(_url)
            image_file_path = os.path.join(images_folder, str(i), ".jpg")
            with open(image_file_path, "wb") as out_file:
                out_file.write(response.content)
        except:
            print("image %s can't be saved." % str(i))


def get_friends_link(_browser, _url):
    _browser.get(_url)
    _photos_link = list()
    timeout = randint(2, 8)
    source = _browser.page_source
    soup = BeautifulSoup(source, "html.parser")
    # for data in soup.find_all(class_="uiMediaThumb uiScrollableThumb uiMediaThumbLarge"):
    for data in soup.find_all(class_="uiMediaThumb _6i9 uiMediaThumbMedium"):
        _photos_link.append(data.get("href"))
        time.sleep(timeout)

    return _photos_link


if __name__ == "__main__":
    # agent_file_path = "E:/Myself/1.source_code/crawler/user_agents.txt"
    email = "2432659496@qq.com"
    password = "qianxuewu"
    browser = log_in(email, password)
    photos_link = page_refresh(browser, "https://www.facebook.com/100025148614740/photos")
    images_download(browser, photos_link)
    # print(photos_link)
    # graph = facepy.GraphAPI(token)
    # user_info = graph.get('me?fields=friendlists')
    # print(user_info)
    # print('id: ', user_info['id'])
    # print('name: ', user_info['name'])

