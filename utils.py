#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018.03.09
Finished on 2018.04.13
@author: Wang Yuntao
"""

import re
import os
import pip
import csv
import time
import json
import shutil
import requests
from random import randint
from subprocess import call

"""
    function:
        is_exist(var)                               确定当前变量是否存在
        get_account(_account_file, number=None)     从本地文件读取用于登录Facebook的账号和密码 (用于防止账号泄露和多账号管理)
        get_packages()                              获取当前运行的机器上的python库
        package_check(packages=None)                检查当前运行的机器上是否有程序运行依赖的库
        get_timeout(_speed_mode)                    根据设定的系统运行模式设定相应的时间延迟，降低被封号的风险
        folder_make(_folder_name="./")              创建文件夹，用于存储某个用户的照片
        get_time(_unix_time_stamp)                  unix时间戳 -> "%Y-%m-%d %H:%M:%S"格式的时间
        get_unix_stamp(_time_string)                "%Y-%m-%d %H:%M:%S"格式的时间 -> unix时间戳
        get_size(_style_string)                     对html源码解析得到的字符串进行分析，得到照片的尺寸
        url_type_judge(_url)                        对facebook的homepage url进行类型判断，方便url处理
        url_concatenate(base_url, join_url)         ulr拼接，类似于urlparse中的urljoin
        get_jump_url(_main_page_url, _key)          根据facebook的url规则进行处理，得到相应的跳转链接
        download_photos(_link, _folder_name="./",
         _name=None)                                根据图像的url对其进行下载
        str2dict(string)                            将网页中原本为字典变量的字符串重新转换为字典类型
"""


def is_exist(var):
    """
    判断当前变量是否存在
    :param var: 待检测变量值 (需为字符串类型)
    :return: exist - True, not exist - False
    """
    try:
        type(eval(var))
    except BaseException:
        return False
    else:
        return True


def get_account(_account_file, number=None):
    """
    从本地读取Facebook账户密码
    :param _account_file: 账户文件列表
    :param number: 用户编号, 若不设定则为随机数
    :return:
        account: Facebook account
        password: Facebook password
    """
    if not os.path.exists(_account_file):
        print("The current file is not existed.")
        account, password = None, None
    else:
        account_list = list()
        account_total_number = 0
        with open(_account_file, "r") as file:
            contents = csv.reader(file)
            for content in contents:
                account_list.append(content)
                account_total_number += 1

        if number is None:
            number = randint(0, account_total_number - 1)
        if number > account_total_number - 1:
            number = account_total_number - 1

        account, password = account_list[number][0], account_list[number][1]

    return account, password


def get_packages():
    """
    获取当前运行的机器上安装的python库
    :return:
        _packages: python库目录
    """
    _packages = list()
    for distribution in pip.get_installed_distributions():
        package_name = distribution.project_name
        _packages.append(package_name)

    return _packages


def package_check(packages=None):
    """
    判断当前项目需要运行的库是否安装
    :param packages: 待检测的python库
    :return: NULL
    """
    system_packages = get_packages()
    if packages is None:
        packages = ["selenium", "beautifulsoup4", "requests"]
    if isinstance(packages, list) is False:
        packages = [packages]
    for package in packages:
        if package not in system_packages:
            val = call("pip install " + package, shell=True)
            if val == 0:
                print("%s is installed successfully." % package)
            elif val == 1:
                print("%s is not existed." % package)
            else:
                pass
        else:
            pass
    print("Packages check completed.")


def get_timeout(_speed_mode):
    """
    根据运行模式获取时间延迟
    :param _speed_mode: 运行模式 (Extreme | Fast | Normal | Slow | Other)
    :return:
        timeout: 时间延迟
    """
    if _speed_mode == "Extreme":
        timeout = 0
    elif _speed_mode == "Fast":
        timeout = randint(1, 3)
    elif _speed_mode == "Normal":
        timeout = randint(2, 5)
    elif _speed_mode == "Slow":
        timeout = randint(3, 8)
    else:
        timeout = 1

    return timeout


def folder_make(_folder_name="./"):
    """
    创建文件目录
    :param _folder_name: 目录名
    :return: NULL
    """
    if _folder_name == "./":
        pass
    else:
        if not os.path.exists(_folder_name):
            os.mkdir(_folder_name)


def get_time(_unix_time_stamp=None):
    """
    unix时间戳 -> "%Y-%m-%d %H:%M:%S"格式的时间
    e.g. 1522048036 -> 2018-03-26 15:07:16
    :param _unix_time_stamp: unix时间戳
    :return:
        "%Y-%m-%d %H:%M:%S"格式的时间
    """
    _format = "%Y-%m-%d %H:%M:%S"
    if _unix_time_stamp is None:
        value = time.localtime()
    else:
        value = time.localtime(_unix_time_stamp)
    _time_string = time.strftime(_format, value)

    return _time_string


def get_unix_stamp(_time_string="1970-01-01 08:01:51"):
    """
    "%Y-%m-%d %H:%M:%S"格式的时间 -> unix时间戳
    :param _time_string: "%Y-%m-%d %H:%M:%S"格式的时间
    :return: unix时间戳
    """
    _format = "%Y-%m-%d %H:%M:%S"
    _unix_time_stamp = time.mktime(time.strptime(_time_string, _format))

    return int(_unix_time_stamp)


def get_size(_style_string):
    """
    根据解析得到的html字符串进行格式分析
    :param _style_string: "width: ***px; height: ***px;"格式的字符串
    :return:
        width: 图片的宽度
        height: 图片的高度
    """
    pattern = re.compile(r"\d+\.?\d*")
    content = pattern.findall(_style_string)
    _width, _height = content[0], content[1]

    return _width, _height


def url_type_judge(_url):
    """
    facebook的url分为两种：
        1. https://www.facebook.com/erlyn.jumawan.7
        2. https://www.facebook.com/profile.php?id=100025029671192
    两种url的处理方式是不同的，因此需要先对其进行类型判断
    :param _url: url
    :return:
        _url_type: 1 or 2 (user_name | ID)
    """
    url_root = "https://www.facebook.com/"
    url_new = _url.replace(url_root, "")
    url_cut = url_new.split("?")
    if url_cut[0] == "profile.php":
        _url_type = 2
    else:
        _url_type = 1

    return _url_type


def get_homepage_url(original_homepage_url):
    """
    对获取的url进行处理，去除尾标

        https://www.facebook.com/profile.php?id=100000031380685&ref=br_rs ->
            https://www.facebook.com/profile.php?id=100000031380685

        https://www.facebook.com/nihaomexico?ref=br_rs ->
            https://www.facebook.com/nihaomexico

    :param original_homepage_url: 原始homepage url
    :return:
    """
    url_type = url_type_judge(original_homepage_url)
    if url_type == 1:
        homepage_url = original_homepage_url.split("?")[0]
    else:
        homepage_url = original_homepage_url.split("&")[0]

    return homepage_url


def url_concatenate(base_url, join_url):
    """
    链接字串合并
    :param base_url: 主链接
    :param join_url: 待合并字串
    :return:
        new_url: 合并后的url
    """
    if base_url[-1] == "/":
        new_url = base_url + join_url
    else:
        new_url = base_url + "/" + join_url

    return new_url


def get_jump_url(_main_page_url, _key):
    """
    获得Facebook跳转链接
    :param _main_page_url:
    :param _key: 关键字
    :return:
        _url: 生成的跳转链接
    e.g.
        _main_page_url: https://www.facebook.com/erlyn.jumawan.7
        _key: friends
        output: https://www.facebook.com/erlyn.jumawan.7/friends

        _main_page_url: https://www.facebook.com/profile.php?id=100025029671192
        _key: photos
        output: https://www.facebook.com/profile.php?id=100025029671192&sk=photos
    """
    keys = ["about", "photos", "friends", "videos", "music", "movies", "books", "tv"]
    if _key not in keys:
        _url = None
    else:
        if url_type_judge(_main_page_url) == 1:
            _url = url_concatenate(_main_page_url, _key)

        elif url_type_judge(_main_page_url) == 2:
            bunch = "&sk=" + _key
            _url = url_concatenate(_main_page_url, bunch)

        else:
            _url = ""

    return _url


def user_search_xpath(_index):
    """
    生成用于用户查询的xpath
    :param _index: 用户序号
    :return:
        xpath_str: 指定序号用户的xpath
    """
    count = _index + 1
    if count <= 5:
        xpath_str = "//*[@id=\"BrowseResultsContainer\"]/div[" + str(count) + "]/div"
    elif 5 < count <= 11:
        xpath_str = "//*[@id=\"u_ps_fetchstream_0_3_0_browse_result_below_fold\"]/div/div[" + str(count - 5) + "]/div"
    else:
        pager = (count - 12) // 6
        number = (count - 12) % 6 + 1

        xpath_str = "//*[@id=\"fbBrowseScrollingPagerContainer" + str(pager) + "\"]/div/div[" + str(number) + "]/div"

    return xpath_str


def str2dict(string):
    """
    将字符串转为字典变量，从网页源代码解析出的部分字典类型的变量以字符串形式存储，因此需要先对其进行转换，再取出对应元素
    :param string: 带转换的字典形式的字符串
    :return:
        result_dict: 转换后的字典变量
    """
    result_dict = json.loads(string, encoding='UTF-8')

    return result_dict


def download_photos(_link, _folder_name="./", _name=None):
    """
    图像下载
    :param _link: 图像链接
    :param _folder_name: 用于保存图像的文件路径
    :param _name: 下载后的图像名
    :return: NULL
    """
    if _name is None:
        _name = ((_link.split("/")[-1]).split("?")[0]).split(".")[0]
    response = requests.get(_link, stream=True)
    if response.status_code == 200:
        photo_file_name = os.path.join(_folder_name, _name + ".jpg")
        with open(photo_file_name, "wb") as file:
            shutil.copyfileobj(response.raw, file)
            print("image %s is saved successfully." % (_name + ".jpg"))
    else:
        pass


if __name__ == "__main__":
    d = get_unix_stamp()
    print(d)
    s = get_time(1332888820)
    print(s)
    width, height = get_size("width: 547px; height: 972px;")
    print(width, type(width))
    print(height, type(height))
    print(get_jump_url("https://www.facebook.com/erlyn.jumawan.7", "videos"))
    print(get_jump_url("https://www.facebook.com/profile.php?id=100025029671192", "photos"))
