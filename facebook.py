#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018.03.09
Finished on 
@author: Wang Yuntao
"""

import re
import time
import utils
from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver

"""
    function:
        __init__(self, _user_name=None, _password=None, _browser_type="Chrome", 
                            is_headless=False)          __init__
        log_in(self)                                    Facebook登录
        make_post(self)                                 发布状态
        page_refresh(self, _refresh_times=0)            页面下拉刷新
        enter_homepage_self(self)                       进入当前账户的个人主页 (方便对用户好友和照片的获取)
        get_user_id(self, _user_homepage_url)           获取用户id
        get_friends_list(self, _friends_number=None)    获取当前账户的好友列表 (列表存储各好友的user_name, user_id, homepage_url)
        search_users(self, _keyword, user_number)       获取当前搜索条件下的用户列表 (列表存储各用户的user_name, homepage_url, location, user_id)
        get_photos_list(self)                           获取照片的href，方便对原图的链接，发表时间等进行获取
        get_photo_info(self, _photo_href)               获取照片的链接，发布时间，发布位置，尺寸与对应的文字说明
        get_photos_info_list(self, _photos_href_list)   批量获取照片的链接，发布时间，发布位置，尺寸与对应的文字说明
        download_photos_one(self, _homepage_url)        下载单个用户的图片
        download_photos_batch(self, _homepage_url_list) 批量下载多个用户的图片
"""


class Facebook:
    def __init__(self, _user_name=None, _password=None, _browser_type="Chrome", _is_headless=False):
        """
        构造函数
        :param _user_name: Facebook登录所需邮箱
        :param _password: Facebook登录对应的密码
        :param _browser_type: 浏览器类型 (Chrome | Firefox)
        :param _is_headless: 是否适用无头浏览器
        """
        # the variables which are fixed
        self.url = "https://www.facebook.com/"                      # facebook页面url
        self.user_name = _user_name                                 # 帐户名
        self.password = _password                                   # 密码
        self.browser_state = None                                   # 浏览器选择状态
        self.login_state = None                                     # 登录状态
        self.homepage_url = None                                    # 当前登录账号的主页url

        # some parameters of webdriver
        self.cookie = None                                          # 当前登录账号的cookie
        self.session_id = None                                      # 会话id，方便在当前打开窗口继续运行
        self.executor_url = None                                    # 会话的命令执行器连接
        self.cookies = None                                         # 用户cookies

        # the initialization of list
        self.user_info_friends = list()                             # 好友信息列表 (user_name, user_id, homepage_url)
        self.user_info_search = list()                              # 通过搜索得到的用户信息列表 (user_name, homepage_url)

        # the variables which are variant regularly
        self.id_class_name = "clearfix sideNavItem stat_elem"       # 从www.facebook.com页面获取用户id所需class name
        self.post_class_name = "_3jk"                               # 状态发布所需class name
        self.friends_class_name = "clearfix _1_ca"                  # 好友列表获取所需class name

        # 用户搜索所需class name
        self.user_item_class_name = "_4p2o"
        self.user_info_class_name = "_32mo"
        self.location_class_name = "_pac"
        self.id_class_name = "_3u1 _gli _uvb"

        # the selection of browser
        if _browser_type == "Chrome":
            try:
                options = webdriver.ChromeOptions()
                if _is_headless is True:
                    options.set_headless()
                    options.add_argument("--disable - gpu")
                self.driver = webdriver.Chrome(options=options)
                self.browser_state = 1
            except AttributeError:
                self.browser_state = 0

        if _browser_type == "Firefox":
            try:
                options = webdriver.FirefoxOptions()
                if _is_headless is True:
                    options.set_headless()
                    options.add_argument("--disable - gpu")
                self.driver = webdriver.Firefox(options=options)
                self.browser_state = 1
            except AttributeError:
                self.browser_state = 0

    def log_in(self):
        """
        facebook log in via webdriver
        :return: a status code —— True: Success, False: False
        Note:
            如果facebook账号登录成功，则当前页面的url为:https://www.facebook.com
            如果facebook账号登录失败，则当前页面的url为:https://www.facebook.com/login.php?login_attempt=1&lwv=100
        """
        timeout = randint(1, 4)
        self.driver.get(self.url)

        # username
        email_element = self.driver.find_element_by_id('email')
        email_element.clear()
        email_element.send_keys(self.user_name)
        time.sleep(timeout)

        # password
        password_element = self.driver.find_element_by_id('pass')
        password_element.clear()
        password_element.send_keys(self.password)
        time.sleep(timeout)

        # click
        login = self.driver.find_element_by_id('loginbutton')
        login.click()

        self.cookies = self.driver.get_cookies()

        # status judgement
        current_page_url = self.driver.current_url
        if current_page_url != self.url:
            self.login_state = 0
        else:
            self.login_state = 1

    def make_post(self):
        self.enter_homepage_self()
        post_element = self.driver.find_element_by_class_name(self.post_class_name)
        post_element.click()

    def page_refresh(self, _refresh_times=0):
        timeout = randint(2, 8)
        for i in range(_refresh_times):
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(timeout)

    def enter_homepage_self(self):
        """
        进入个人主页，facebook登录后页面仍停留在https://www.facebook.com，需要进一步跳转到个人主页，获取到主页url，
        方便对好友列表，照片的获取
        :return:
        """
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        li = soup.find(class_=self.id_class_name)
        user_id = li.get("data-nav-item-id")
        self.homepage_url = utils.url_concatenate(self.url, user_id)
        self.driver.get(self.homepage_url)

    def get_user_id(self, _user_homepage_url):
        if utils.url_type_judge(_user_homepage_url) == 1:
            self.driver.get(_user_homepage_url)
            page = self.driver.page_source
            soup = BeautifulSoup(page, "html.parser")
            href = soup.find(class_="photoContainer")
            _user_id = href.a.get("href").split("id=")[-1]
        else:
            _user_id = _user_homepage_url.split("id=")[-1]

        return _user_id

    def get_friends_list(self, _friends_number=None):
        friends_page_url = utils.get_jump_url(self.homepage_url, "friends")
        self.driver.get(friends_page_url)
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # 获取好友数量
        friends_table = soup.find(class_=self.friends_class_name)              # class name可能会变
        content = friends_table.a.text
        pattern = re.compile(r"\d+\.?\d*")
        friends_number = int(pattern.findall(content)[0])

        # 根据好友数量进行页面刷新
        refresh_times = friends_number // 20
        self.page_refresh(refresh_times)

        # 重新对刷新后的页面进行解析
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # 获取好友url列表
        contents = soup.find_all(class_="uiProfileBlockContent")
        for content in contents:
            homepage_url = content.a.get("href")
            if utils.url_type_judge(homepage_url) == 1:
                homepage_url = homepage_url.replace("?fref=pb&hc_location=friends_tab", "")
            if utils.url_type_judge(homepage_url) == 2:
                homepage_url = homepage_url.replace("&fref=pb&hc_location=friends_tab", "")
            user_name = content.a.text
            pattern = re.compile(r"id=\d+")
            user_id = pattern.findall(content.a.get("data-hovercard"))[0].split("id=")[-1]
            self.user_info_friends.append([user_name, user_id, homepage_url])

    def search_users(self, _keyword, user_number):
        search_url = "https://www.facebook.com/search/str/" + _keyword + "keywords_users"
        self.driver.get(search_url)
        refresh_times = user_number // 5
        self.page_refresh(refresh_times)
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # 获取user homepage列表
        contents = soup.find_all(class_=self.user_item_class_name)
        for content in contents:
            user_url_name = content.find(class_=self.user_info_class_name)
            homepage_url = user_url_name.get("href")
            if utils.url_type_judge(homepage_url) == 1:
                homepage_url = homepage_url.replace("?ref=br_rs", "")
            if utils.url_type_judge(homepage_url) == 2:
                homepage_url = homepage_url.replace("&ref=br_rs", "")

            user_name = user_url_name.text
            location = content.find(class_=self.location_class_name).text
            user_info_dict = content.find(class_=self.id_class_name).get("data-bt")
            pattern = re.compile(r"\"id\":\d+")
            user_id = pattern.findall(user_info_dict)[0].split("\"id\":")[-1]

            self.user_info_search.append([user_name, user_id, location, homepage_url])

    def get_photos_list(self, _homepage_url):
        photos_url = utils.get_jump_url(_homepage_url, "photos")
        self.driver.get(photos_url)
        page = self.driver.page_source
        soup = BeautifulSoup(page, "html.parser")
        bottom_flag = soup.find_all(class_="uiHeaderTitle")

        timeout = randint(2, 5)
        photos_href_list = list()
        while "更多" not in bottom_flag[-1].string or "More about" not in bottom_flag[-1].string:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(timeout)

            page = self.driver.page_source
            soup = BeautifulSoup(page, "html.parser")
            bottom_flag = soup.find_all(class_="uiHeaderTitle")
            if "更多" in bottom_flag[-1].string or "More about" in bottom_flag[-1].string:
                break

        for data in soup.find_all(class_="uiMediaThumb _6i9 uiMediaThumbMedium"):
            photos_href_list.append(data.get("href"))

        return photos_href_list

    def get_photo_info(self, _photo_href):
        self.driver.get(_photo_href)
        page = self.driver.page_source
        soup = BeautifulSoup(page, "html.parser")

        publish_time = soup.find("span", {"id": "fbPhotoSnowliftTimestamp"})
        _date = publish_time.a.abbr.get("data-utime")                           # 图片发表的时间 (Unix时间戳)
        location_object = soup.find(class_="fbPhotosImplicitLocLink")           # 图片发表的位置信息
        if location_object is not None:
            _location = location_object.text
        else:
            _location = []

        text_object = soup.find("span", {"class": "hasCaption"})                # 图片发表时对应的文字说明
        if text_object is not None:
            _text = text_object.text
        else:
            _text = []

        # 进入全屏状态
        full_screen_element = self.driver.find_element_by_id("fbPhotoSnowliftFullScreenSwitch")
        full_screen_element.click()
        page = self.driver.page_source
        soup = BeautifulSoup(page, "html.parser")

        spotlight = soup.find(class_="spotlight")
        _link = spotlight.get("src")                                            # 图片链接
        style = spotlight.get("style")                                          # 图片尺寸字符串
        _width, _height = utils.get_size(style)                                 # 获取图像的宽和高

        return _link, _date, _location, _text, _width, _height

    def get_photos_info_list(self, _photos_href_list):
        timeout = randint(2, 8)
        _photos_info_list = list()
        for photo_href in _photos_href_list:
            link, date, location, text, width, height = self.get_photo_info(photo_href)
            _photos_info_list.append([link, date, location, text, width, height])
            time.sleep(timeout)

        return _photos_info_list

    def download_photos_one(self, _homepage_url, start_date=None, end_date=None, _folder_name="./"):
        photos_href_list = self.get_photos_list(_homepage_url)
        photos_info_list = self.get_photos_info_list(photos_href_list)

        if start_date is None and end_date is None:
            for photo_info in photos_info_list:
                utils.download_photos(photo_info[0], _folder_name)
        else:
            start_date_unix = utils.get_unix_stamp(start_date)
            end_date_unix = utils.get_unix_stamp(end_date)
            for photo_info in photos_info_list:
                unix_time = photo_info[1]
                if start_date_unix < unix_time < end_date_unix:
                    utils.download_photos(photo_info[0], _folder_name)
                else:
                    pass

    def download_photos_batch(self, _homepage_url_list, start_date=None, end_date=None):
        for _homepage_url in _homepage_url_list:
            folder_name = _homepage_url.split("/")[-1]
            self.download_photos_one(_homepage_url, start_date, end_date, folder_name)


if __name__ == "__main__":
    email = "2432659496@qq.com"
    password = "qianxuewu"
    fb = Facebook(email, password, "Chrome", False)
    if fb.browser_state == 1:
        fb.log_in()
        fb.enter_homepage_self()
        fb.make_post()
        cookies = fb.cookies

    else:
        print("Initialization failed.")
