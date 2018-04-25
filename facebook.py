#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018.03.09
Finished on 2018.04.13
@author: Wang Yuntao
"""

import re
import os
import json
import time
import utils
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""
    function:
        __init__(self, _user_name=None, _password=None, _browser_type="Chrome", 
                            is_headless=False)          __init__
        sign_in(self)                                   Facebook登录
        make_post(self)                                 发布状态
        page_refresh(self, _refresh_times=0)            页面下拉刷新
        get_myself_info(self)                           获取当前登录账户的信息 user_name, user_id, homepage_url
        enter_homepage_self(self)                       进入当前账户的个人主页 (方便对用户好友和照片的获取)
        get_user_id(self, _user_homepage_url)           获取用户id
        get_friends_number(self)                        获取当前账户的好友个数
        get_friends_list(self, _friends_number=None)    获取当前账户的好友列表 (列表存储各好友的user_name, user_id, homepage_url)
        search_users(self, _keyword, user_number)       获取当前搜索条件下的用户列表 (列表存储各用户的user_name, homepage_url, location, user_id)
        
        get_photos_list(self)                           获取照片的href，方便对原图的链接，发表时间等进行获取
        get_photo_info(self, _photo_href)               获取照片的链接，发布时间，发布位置，尺寸与对应的文字说明
        get_photos_info_list(self, _photos_href_list)   批量获取照片的链接，发布时间，发布位置，尺寸与对应的文字说明
        download_photos_one(self, _homepage_url)        下载单个用户的图片
        download_photos_batch(self, _homepage_url_list) 批量下载多个用户的图片
        params_modify(self, post_class_name, 
            bottom_xpath_search, bottom_xpath_other, 
            main_container_class_name, 
            myself_id_class_name)                       用于对可变参数进行修改
         
    Note:
        实际使用中还需要根据Facebook当前的页面架构进行相应调整
"""


class Facebook:
    def __init__(self, _email=None, _password=None, _browser_type="Chrome", _is_headless=False, _speed_mode="Normal"):
        """
        构造函数
        :param _email: Facebook登录所需邮箱
        :param _password: Facebook登录对应的密码
        :param _browser_type: 浏览器类型 (Chrome | Firefox)
        :param _is_headless: 是否适用无头浏览器
        :param _speed_mode: 运行速度模式选择 (Extreme | Fast | Normal | Slow)
        Return:
            browser_state:
                0 - init fail
                1 - init success
        """
        # the variables which are fixed
        self.url = "https://www.facebook.com/"                              # facebook页面url
        self.email = _email                                                 # 帐户邮箱
        self.password = _password                                           # 账户密码
        self.soup_type = "html.parser"                                      # beautifulsoup解析类型

        # some identifier
        self.browser_state = None                                           # 浏览器选择状态
        self.login_state = None                                             # 登录状态

        # the variable about the current login account
        self.user_name = None                                               # 当前登录账号的用户昵称
        self.user_id = None                                                 # 当前登录账号的用户ID
        self.homepage_url = None                                            # 当前登录账号的主页url
        self.friends_number = 0                                             # 当前登录账号的好友数量

        # some parameters of webdriver
        self.cookie = None                                                  # 当前登录账号的cookie
        self.session_id = None                                              # 会话id，方便在当前打开窗口继续运行
        self.executor_url = None                                            # 会话的命令执行器连接
        self.cookies_path = "./cookies/cookies(" + _email + ").json"        # 用于保存用户cookies的文件

        # the initialization of list
        self.user_info_friends = list()                                     # 好友信息列表 (user_name, user_id, homepage_url)
        self.user_info_search = list()                                      # 通过搜索得到的用户信息列表 (user_name, homepage_url)

        # the variables which are static
        self.clearfix_flag = "clearfix"                                     # 网页消除浮动标识
        self.user_cover_class_name = "cover"                                # 用户封面对应的class name
        self.bottom_class_name = "uiHeaderTitle"                            # 用于确定图片、视频下载时有无下拉到最底的class name
        self.bottom_xpath_search = \
            "//*[@id=\"browse_end_of_results_footer\"]/div/div"             # 用户搜索时对应的bottom标识
        self.bottom_xpath_other = \
            "//*[@id=\"timeline-medley\"]/div/div[2]/div[1]/div/div"        # 照片好友信息遍历时的bottom标识
        self.full_screen_id = "fbPhotoSnowliftFullScreenSwitch"             # 全屏操作对应的id
        self.main_container_class_name = "homeSideNav"                      # 用户获取当前登录账户信息的class name
        self.myself_id_class_name = "data-nav-item-id"                      # 用户id对应的字段名
        self.friends_list_class_name = "uiProfileBlockContent"
        self.friends_number_id_name = "pagelet_timeline_medley_friends"     # 用于获取好友数量的id name
        self.browse_results_container = "//*[@id=\"BrowseResultsContainer\"]/div[1]"

        # the variables which may be variant regularly
        self.post_class_name = "_3jk"                                       # 状态发布所需class name

        # 用户搜索所需class name
        self.user_search_class_name = None
        self.user_name_class_name = None

        # the selection of browser
        if _browser_type == "Chrome":
            try:
                options = webdriver.ChromeOptions()
                if _is_headless is True:
                    options.set_headless()
                    options.add_argument("--disable - gpu")
                else:
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
                else:
                    self.driver = webdriver.Firefox(options=options)
                    self.browser_state = 1
            except AttributeError:
                self.browser_state = 0

        # the run speed mode selection
        self.timeout = utils.get_timeout(_speed_mode)

    def params_modify(self, cookies_path, post_class_name, bottom_xpath_search, bottom_xpath_other, main_container_class_name,
                      myself_id_class_name):
        self.cookies_path = cookies_path
        self.post_class_name = post_class_name
        self.bottom_xpath_search = bottom_xpath_search
        self.bottom_xpath_other = bottom_xpath_other
        self.main_container_class_name = main_container_class_name
        self.myself_id_class_name = myself_id_class_name

    def get(self, url):
        """
        页面跳转，为避免多余跳转，先对当前页面的url进行判断，若url相同则不再跳转
        :param url: 待跳转的url
        :return: NULL
        """
        current_url = self.driver.current_url
        if url == current_url:
            pass
        else:
            self.driver.get(url)

    def login_with_account(self):
        """
        facebook login with username and password
        :return: a status code —— True: Success, False: False
        Note:
            如果facebook账号登录成功，则当前页面的url为:https://www.facebook.com
            如果facebook账号登录失败，则当前页面的url为:https://www.facebook.com/login.php?login_attempt=1&lwv=100
        """
        self.get(self.url)
        try:
            # username
            email_element = WebDriverWait(self.driver, timeout=5).until(
                    EC.presence_of_element_located((By.ID, "email")))
            email_element.clear()
            email_element.send_keys(self.email)
            self.driver.implicitly_wait(1)

            # password
            password_element = WebDriverWait(self.driver, timeout=5).until(
                    EC.presence_of_element_located((By.ID, "pass")))
            password_element.clear()
            password_element.send_keys(self.password)
            self.driver.implicitly_wait(1)

            # click
            login_element = WebDriverWait(self.driver, timeout=5).until(
                    EC.presence_of_element_located((By.ID, "loginbutton")))
            login_element.click()
        except:
            pass

    def login_with_cookies(self):
        """
        facebook login with cookies
        :return: a status code —— True: Success, False: False
        Note:
            如果facebook账号登录成功，则当前页面的url为:https://www.facebook.com
            如果facebook账号登录失败，则当前页面的url为:https://www.facebook.com/login.php?login_attempt=1&lwv=100
        """
        if os.path.exists(self.cookies_path):
            with open(self.cookies_path, 'r', encoding='utf-8') as file:
                list_cookies = json.loads(file.read())
            if len(list_cookies) != 0:
                self.driver.get(self.url)
                for cookie in list_cookies:
                    try:
                        self.driver.add_cookie({
                            "domain": cookie["domain"],
                            "name": cookie["name"],
                            "value": cookie["value"],
                            "path": cookie["path"],
                            "expiry": cookie["expiry"]
                        })
                    except KeyError:
                        pass

                self.driver.get(self.url)

    def is_login_success(self):
        """
        判断当前账户是否登录成功
        :return:
            login_status: False - Fail, True - Success
        """
        page = self.driver.page_source
        soup = BeautifulSoup(page, self.soup_type)
        flag = soup.find(id="sideNav")
        if flag is not None:
            login_status = True
        else:
            login_status = False

        return login_status

    def sign_in(self):
        """
        facebook login via webdriver, cookies login first, if no cookies, login with account and save the cookies
        :return: a status code —— True: Success, False: False
        Note:
            如果facebook账号登录成功，则当前页面的url为:https://www.facebook.com
            如果facebook账号登录失败，则当前页面的url为:https://www.facebook.com/login.php?login_attempt=1&lwv=100
        """
        if os.path.exists(self.cookies_path):
            self.login_with_cookies()
        else:
            self.login_with_account()

        # status judgement
        if self.is_login_success():
            self.save_cookie()

    def save_cookie(self):
        if not os.path.exists("cookies"):
            os.mkdir("cookies")
        # 获取cookie并通过json模块将dict转化成str
        dict_cookies = self.driver.get_cookies()
        json_cookies = json.dumps(dict_cookies)
        # 登录完成后，将cookie保存到本地文件
        if os.path.exists(os.path.join("./cookies", self.cookies_path)):
            pass
        else:
            with open(self.cookies_path, "w") as file:
                file.write(json_cookies)

    def make_post(self):
        current_url = self.driver.current_url
        if current_url != self.url:
            self.enter_homepage_self()
        else:
            pass
        post_element = self.driver.find_element_by_class_name(self.post_class_name)
        post_element.click()

    def page_refresh_to_bottom(self, item, timeout=3, poll_frequency=0.5):
        """
        页面刷新
        :param item: 下拉页类型，分为用户搜索和照片搜索两类
        :param timeout: 模拟下拉的时间延迟
        :param poll_frequency: 模拟下拉的时间频率
        :return: NULL
        """
        if item == "users":
            xpath = self.bottom_xpath_search
        else:
            xpath = self.bottom_xpath_other

        while True:
            try:
                WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll_frequency).until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
                break
            except:
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

    def page_refresh(self, _refresh_times=0):
        """
        页面刷新
        :param _refresh_times: 刷新次数
        :return: NULL
        """
        for i in range(_refresh_times):
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            try:
                bottom_element = WebDriverWait(self.driver, timeout=3).until(
                    EC.presence_of_element_located((By.XPATH, self.bottom_xpath_search)))
            except:
                try:
                    bottom_element = WebDriverWait(self.driver, timeout=3).until(
                        EC.presence_of_element_located((By.XPATH, self.bottom_xpath_other)))
                except:
                    bottom_element = None

            if bottom_element is not None:
                break

    def get_myself_info(self):
        """
        获取当前登录账户的信息
        :return:
            user_name: 用户名
            user_id: 用户id
            homepage_url: 用户主页
        """
        self.get(self.url)
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, self.soup_type)

        main_container = soup.find(class_=self.main_container_class_name)
        id_class = main_container.li
        user_id = id_class.get(self.myself_id_class_name)
        user_info_class = main_container.find_all("a")
        user_name = user_info_class[1].get("title")
        homepage_url = user_info_class[1].get("href")
        homepage_url = utils.get_homepage_url(homepage_url)

        self.user_name, self.user_id, self.homepage_url = user_name, user_id, homepage_url

    def enter_homepage_self(self):
        """
        进入个人主页，facebook登录后页面仍停留在https://www.facebook.com，需要进一步跳转到个人主页，获取到主页url，
        方便对好友列表，照片的获取
        :return:
        """
        if self.user_id is None:
            self.get_myself_info()

        self.get(self.homepage_url)

    def get_user_id(self, user_homepage_url):
        """
        根据用户的主页url获取其user id
        :param user_homepage_url: 用户的主页url
        :return: user id
        """
        if utils.url_type_judge(user_homepage_url) == 1:
            self.driver.get(user_homepage_url)
            page = self.driver.page_source
            soup = BeautifulSoup(page, self.soup_type)
            cover = soup.find(class_=self.user_cover_class_name)
            user_id = cover.a.get("data-referrerid")
        else:
            user_id = user_homepage_url.split("id=")[-1]

        return user_id

    def get_friends_number(self):
        """
        获取当前登录账户的好友数量
        :return:
            self.friends_number: 当前登录账户的好友数量
        """
        if self.homepage_url is None:
            self.get_myself_info()
        friends_page_url = utils.get_jump_url(self.homepage_url, "friends")
        self.get(friends_page_url)
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, self.soup_type)

        friends_table = self.driver.find_element_by_id(self.friends_number_id_name)
        friends_table_class_name = friends_table.get_attribute("class")

        block = soup.find(class_=friends_table_class_name)
        content = block.find_all("div")
        content_text = content[5].a.text
        pattern = re.compile(r"\d+\.?\d*")

        self.friends_number = int(pattern.findall(content_text)[0])

    def get_friends_list(self, friends_number=None):
        """
        获取当前登录账户的好友列表
        :param friends_number: 待检索的好友数量
        :return:
            self.user_info_friends: 好友用户信息 [user_name, user_id, homepage_url]
        """
        self.get_friends_number()
        self.user_info_friends = list()

        if friends_number is None or friends_number > self.friends_number:
            self.page_refresh_to_bottom("friends")
        else:
            refresh_times = friends_number // 20
            self.page_refresh(refresh_times)
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, self.soup_type)

        # 获取好友url列表
        items = soup.find_all(class_=self.friends_list_class_name)

        if friends_number is None or friends_number > self.friends_number:
            for item in items:
                friend_info = self.get_friend_info(item)
                self.user_info_friends.append(friend_info)
        else:
            index = 0
            while index < friends_number:
                friend_info = self.get_friend_info(items[index])
                self.user_info_friends.append(friend_info)
                index += 1

    @staticmethod
    def get_friend_info(item):
        homepage_url = item.a.get("href")
        homepage_url = utils.get_homepage_url(homepage_url)
        user_name = item.a.text
        pattern = re.compile(r"id=\d+")
        user_id = pattern.findall(item.a.get("data-hovercard"))[0].split("id=")[-1]

        return [user_name, user_id, homepage_url]

    def get_user_info(self, item):
        data_be_str = item.div.get("data-bt")
        user_id = str(utils.str2dict(data_be_str)["id"])

        # 获取user homepage url
        user_info = item.find(class_=self.clearfix_flag)
        user_homepage_url = user_info.a.get("href")
        user_homepage_url = utils.get_homepage_url(user_homepage_url)

        user_name_block = user_info.div.find(class_=self.clearfix_flag).find_all("div")
        # user_name_class_name = user_name_block[-1].a.get("class")[0]
        user_name = user_name_block[-1].a.text

        about_items = user_info.find_all("div")
        about_class = about_items[11].find_all("div")

        try:
            about = about_class[5].text
        except:
            about = ""

        return [user_name, user_id, user_homepage_url, about]

    def get_class_name_for_search(self):
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, self.soup_type)

        element = self.driver.find_element_by_xpath(self.browse_results_container)
        user_search_class_name = element.get_attribute("class")
        item = soup.find(class_=user_search_class_name)
        user_info = item.find(class_=self.clearfix_flag)
        user_name_block = user_info.div.find(class_=self.clearfix_flag).find_all("div")
        user_name_class_name = user_name_block[-1].a.get("class")[0]

        self.user_search_class_name = user_search_class_name
        self.user_name_class_name = user_name_class_name

    def search_users(self, user_name="wahaha", user_number=None):
        """
        根据关键字进行用户搜索
        :param user_name: 待检索关键字
        :param user_number: 需要检索的用户数量
        :return:
            self.user_info_search: 用户信息列表 [user_name, user_id, location, homepage_url]
        """
        user_info_search = list()
        search_url = "https://www.facebook.com/search/str/" + user_name + "/keywords_users"
        self.get(search_url)
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, self.soup_type)
        empty_flag = soup.find(id="empty_result_error")
        if empty_flag is None:
            # 页面刷新
            if user_number is None:
                self.page_refresh_to_bottom("users")
            else:
                refresh_times = user_number // 5
                self.page_refresh(refresh_times)

            # 页面解析
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, self.soup_type)

            if self.user_search_class_name is None:
                self.get_class_name_for_search()

            items = soup.find_all(class_=self.user_search_class_name)
            total_user_number = len(items)

            # 列表填充
            if user_number is None or user_number > total_user_number:
                for item in items:
                    user_info_search.append(self.get_user_info(item))
            else:
                index = 0
                while index < user_number:
                    user_info_search.append(self.get_user_info(items[index]))
                    index += 1
        else:
            pass

        return user_info_search

    def get_photos_href_list(self, _homepage_url):
        """
        获取照片
        :param _homepage_url: 待访问的用户主页链接
        :return:
            photos_href_list: 图像链接列表
        """
        photos_url = utils.get_jump_url(_homepage_url, "photos")
        self.get(photos_url)
        page = self.driver.page_source
        soup = BeautifulSoup(page, self.soup_type)
        photos_href_list = list()

        if soup.find(text="No photos to show") is not None:
            return photos_href_list
        else:
            try:
                bottom_element = self.driver.find_element_by_xpath(self.bottom_xpath_other)
            except:
                bottom_element = None

            while bottom_element is None:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                page = self.driver.page_source
                soup = BeautifulSoup(page, self.soup_type)
                try:
                    bottom_element = self.driver.find_element_by_xpath(self.bottom_xpath_other)
                except:
                    bottom_element = None

                if bottom_element is not None:
                    break

            for data in soup.find_all(class_="uiMediaThumb"):
                photos_href_list.append(data.get("href"))

            return photos_href_list

    def get_photo_info(self, _photo_href):
        """
        根据图像的链接对其信息进行获取
        :param _photo_href: 图像链接
        :return:
            link: 原始图像对应的链接
            date: 图像发布对应的时间
            location: 图像发布对应的位置
            text: 图像发布对应的文本内容
            width: 图像的实际宽度
            height: 图像的实际高度
        """
        self.get(_photo_href)
        page = self.driver.page_source
        soup = BeautifulSoup(page, self.soup_type)

        date = self.get_photo_publish_date(soup)
        location = self.get_photo_publish_location(soup)
        text = self.get_photo_publish_text(soup)

        try:
            full_screen_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, self.full_screen_id)))
            full_screen_element.click()
        except:
            pass
        page = self.driver.page_source
        soup = BeautifulSoup(page, self.soup_type)

        link = self.get_photo_link(soup)
        width, height = self.get_photo_size(soup)

        return link, date, location, text, width, height

    def get_photos_info_list(self, _photos_href_list):
        """
        获取图片信息
        :param _photos_href_list:
        :return:
        """
        photos_info_list = list()
        if len(_photos_href_list) == 0:
            pass
        else:
            for photo_href in _photos_href_list:
                link, date, location, text, width, height = self.get_photo_info(photo_href)
                photos_info_list.append([link, date, location, text, width, height])

        return photos_info_list

    def download_photos_one(self, homepage_url, folder_name="./",
                            start_date=None, end_date=None, keyword="",
                            width_left=0, width_right=5000, height_left=0, height_right=5000):
        """
        单个用户的照片下载
        :param homepage_url: 用户主页
        :param folder_name: 待保存文件夹路径

        以下为筛选条件
        :param start_date: 待下载图片的起始日期 (default: None)
        :param end_date: 待下载图片的终止日期 (default: None)
        :param keyword: 待下载图片对应的文字中包含的关键字 (default: "")
        :param width_left: 图片宽度下界 (default: 0)
        :param width_right: 图片宽度上界 (default: 5000)
        :param height_left: 图片高度下界 (default: 0)
        :param height_right: 图片高度上界 (default: 5000)
        :return: NULL
        Note:
            photo info:
                link, date, location, text, width, height
        """
        utils.folder_make(folder_name)
        photos_href_list = self.get_photos_href_list(homepage_url)
        photos_info_list = self.get_photos_info_list(photos_href_list)

        if len(photos_href_list) == 0:
            pass
        else:
            if start_date is None and end_date is None:
                for photo_info in photos_info_list:
                    utils.download_photos(photo_info[0], folder_name)
            else:
                start_date_unix = utils.get_unix_stamp(start_date)
                end_date_unix = utils.get_unix_stamp(end_date)
                for photo_info in photos_info_list:
                    unix_time = photo_info[1]
                    if start_date_unix < unix_time < end_date_unix \
                            and keyword in photo_info[3]:
                        if width_left < photo_info[4] < width_right and height_left < photo_info[5] < height_right:
                            utils.download_photos(photo_info[0], folder_name)
                        else:
                            pass
                    else:
                        pass

    def download_photos_batch(self, user_info_list,
                              start_date=1075824000, end_date=int(time.time()), keyword="",
                              width_left=0, width_right=10000, height_left=0, height_right=10000):
        """
        多个用户照片下载
        :param user_info_list: 用户信息列表
                user_name, user_id, user_homepage_url, about
        以下为筛选条件
        :param start_date: 待下载图片的起始日期 (default: 1075824000 -> 2004年2月4日，Facebook成立时间)
        :param end_date: 待下载图片的终止日期 (default: None)
        :param keyword: 待下载图片对应的文字中包含的关键字 (default: "")
        :param width_left: 图片宽度下界 (default: 0)
        :param width_right: 图片宽度上界 (default: 5000)
        :param height_left: 图片高度下界 (default: 0)
        :param height_right: 图片高度上界 (default: 5000)
        :return: NULL
        """
        for user_info in user_info_list:
            folder_name = user_info[1]
            homepage_url = user_info[2]

            self.download_photos_one(homepage_url, folder_name=folder_name,
                                     start_date=start_date, end_date=end_date, keyword=keyword,
                                     width_left=width_left, width_right=width_right,
                                     height_left=height_left, height_right=height_right)
        print("Download completed.")

    @staticmethod
    def get_photo_link(soup):
        spotlight = soup.find(class_="spotlight")
        _link = spotlight.get("src")                                            # 图片链接

        return _link

    @staticmethod
    def get_photo_size(soup):
        spotlight = soup.find(class_="spotlight")
        style = spotlight.get("style")                                          # 图片尺寸字符串
        _width, _height = utils.get_size(style)                                 # 获取图像的宽和高

        return _width, _height

    @staticmethod
    def get_photo_publish_date(soup):
        publish_time = soup.find("span", {"id": "fbPhotoSnowliftTimestamp"})
        if publish_time is None:
            _date = None
        else:
            _date = publish_time.a.abbr.get("data-utime")                       # 图片发表的时间 (Unix时间戳)

        return _date

    @staticmethod
    def get_photo_publish_location(soup):
        location_object = soup.find(class_="fbPhotosImplicitLocLink")           # 图片发表的位置信息
        if location_object is None:
            _location = None
        else:
            _location = location_object.text

        return _location

    @staticmethod
    def get_photo_publish_text(soup):
        text_object = soup.find("span", {"class": "hasCaption"})  # 图片发表时对应的文字说明
        if text_object is None:
            _text = []
        else:
            _text = text_object.text

        return _text

    # 集成
    def get_friends_photos(self, friends_number=None, start_date=None, end_date=None, keyword="",
                           width_left=0, width_right=5000, height_left=0, height_right=5000):
        """
        爬取当前登录账户好友的照片
        :param friends_number: 待爬取的好友数量

        以下为筛选条件
        :param start_date: 待下载图片的起始日期 (default: None)
        :param end_date: 待下载图片的终止日期 (default: None)
        :param keyword: 待下载图片对应的文字中包含的关键字 (default: "")
        :param width_left: 图片宽度下界 (default: 0)
        :param width_right: 图片宽度上界 (default: 5000)
        :param height_left: 图片高度下界 (default: 0)
        :param height_right: 图片高度上界 (default: 5000)
        :return: NULL
            Note: [user_name, user_id, homepage_url]
        """
        if len(self.user_info_friends) == 0:
            self.get_friends_list(friends_number)

        self.download_photos_batch(self.user_info_friends, start_date=start_date, end_date=end_date,
                                   keyword=keyword, width_left=width_left, width_right=width_right,
                                   height_left=height_left, height_right=height_right)

    def get_user_photos(self, user_name=None, user_number=None, start_date=None, end_date=None, keyword="",
                        width_left=0, width_right=5000, height_left=0, height_right=5000):
        """
        爬取当前登录账户好友的照片
        :param user_name: 待爬取用户昵称
        :param user_number: 待爬取的用户数量

        以下为筛选条件
        :param start_date: 待下载图片的起始日期 (default: None)
        :param end_date: 待下载图片的终止日期 (default: None)
        :param keyword: 待下载图片对应的文字中包含的关键字 (default: "")
        :param width_left: 图片宽度下界 (default: 0)
        :param width_right: 图片宽度上界 (default: 5000)
        :param height_left: 图片高度下界 (default: 0)
        :param height_right: 图片高度上界 (default: 5000)
        :return: NULL
            Note: [user_name, user_id, homepage_url]
        """
        if user_name is None:
            self.get_friends_photos(friends_number=user_number, start_date=start_date, end_date=end_date,
                                    keyword=keyword, width_left=width_left, width_right=width_right,
                                    height_left=height_left, height_right=height_right)
        else:
            user_info_list = self.search_users(user_name=user_name, user_number=user_number)
            self.download_photos_batch(user_info_list, start_date=start_date, end_date=end_date,
                                       keyword=keyword, width_left=width_left, width_right=width_right,
                                       height_left=height_left, height_right=height_right)


if __name__ == "__main__":
    pass
