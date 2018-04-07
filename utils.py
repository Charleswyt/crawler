#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 
Finished on 
@author: Wang Yuntao
"""

import re
import time
import shutil
import requests

"""
    function:
        get_time(_unix_time_stamp)                  unix时间戳 -> "%Y-%m-%d %H:%M:%S"格式的时间
        get_unix_stamp(_time_string)                "%Y-%m-%d %H:%M:%S"格式的时间 -> unix时间戳
"""


def get_time(_unix_time_stamp):
    """
    unix时间戳 -> "%Y-%m-%d %H:%M:%S"格式的时间
    e.g. 1522048036 -> 2018-03-26 15:07:16
    :param _unix_time_stamp: unix时间戳
    :return: "%Y-%m-%d %H:%M:%S"格式的时间
    """
    _format = "%Y-%m-%d %H:%M:%S"
    value = time.localtime(_unix_time_stamp)
    _time_string = time.strftime(_format, value)

    return _time_string


def get_unix_stamp(_time_string):
    """
    "%Y-%m-%d %H:%M:%S"格式的时间 -> unix时间戳
    :param _time_string: "%Y-%m-%d %H:%M:%S"格式的时间
    :return: unix时间戳
    """
    _format = "%Y-%m-%d %H:%M:%S"
    time.strptime(_time_string, _format)
    _unix_time_stamp = time.mktime(time.strptime(_time_string, _format))

    return int(_unix_time_stamp)


def get_size(_style_string):
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
    :return: _url_type: 1 or 2 (user_name | ID)
    """
    url_root = "https://www.facebook.com/"
    url_new = _url.replace(url_root, "")
    url_cut = url_new.split(".")
    if url_cut[0] == "profile":
        _url_type = 2
    else:
        _url_type = 1

    return _url_type


def url_concatenate(base_url, join_url):
    """
    链接字串合并
    :param base_url: 主链接
    :param join_url: 待合并字串
    :return:
    """
    if base_url[-1] == "/":
        new_url = base_url + join_url
    else:
        new_url = base_url + "/" + join_url

    return new_url


def get_jump_url(_main_page_url, _key):
    keys = ["photos", "friends", "videos", "music", "books", "tv"]
    if _key not in keys:
        _url = None
    else:
        if url_type_judge(_main_page_url) == 1:
            _url = url_concatenate(_main_page_url, _key)

        elif url_type_judge(_main_page_url) == 2:
            bunch = "&sk=" + _key
            _url = url_concatenate(_main_page_url, bunch)

        else:
            _url = None

    return _url


def download_photos(_link, _folder_name="./", _name=None):
    if _name is None:
        _name = ((_link.split("/")[-1]).split("?")[0]).split(".")[0]
    response = requests.get(_link, stream=True)
    if response.status_code == 200:
        with open(_folder_name + _name + ".jpg", "wb") as file:
            shutil.copyfileobj(response.raw, file)
            print("image %s is saved successfully." % (_name + ".jpg"))
    else:
        pass


if __name__ == "__main__":
    d = get_unix_stamp('2012-03-28 06:53:40')
    print(d)
    s = get_time(1332888820)
    print(s)
    width, height = get_size("width: 547px; height: 972px;")
    print(width, type(width))
    print(height, type(height))
    print(get_jump_url("https://www.facebook.com/erlyn.jumawan.7", "videos"))
    print(get_jump_url("https://www.facebook.com/profile.php?id=100025029671192", "photos"))