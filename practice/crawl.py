#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 
Finished on 
@author: Wang Yuntao
"""

import os
import random
import requests
import win_unicode_console

win_unicode_console.enable()


"""
    Function list:    
        load_user_agent(_agent_file_path)                               从本地加载User Agent文件
        get_agent(_agent_file_path)                                     从本地加载User Agent文件，并随机获取一个User Agent
        download_media(_url, _file_dir, _file_name=None, _timeout=10)   给定媒体链接，并对其进行下载
        get_html_text(_url, timeout=10)                                 获取网页的html文本内容
        html_write(_html, _file_path)                                   将html文本内容写入本地文件
"""


def load_user_agent(_agent_file_path="user_agents.txt"):
    """
    load agent from disk
    :param _agent_file_path: the agent file path
    :return: _agents_list
    """
    _agents_list = []
    with open(_agent_file_path, "r") as file:
        for line in file.readlines():
            if line is not None:
                _agents_list.append(line.strip()[1:-1 - 1])
    random.shuffle(_agents_list)

    return _agents_list


def get_agent(_agent_file_path="user_agents.txt"):
    """
    get an user agent randomly
    :param _agent_file_path: the agent file path
    :return: _headers
    """
    _agents = load_user_agent(_agent_file_path)
    _agent = random.choice(_agents)
    _headers = {"User-Agent": _agent}

    return _headers


def download_media(_url, _file_dir, _file_name=None, _timeout=10):
    """
    download image, video, audio from the internet
    :param _url: url
    :param _file_dir: the folder used for multimedia save
    :param _file_name: file name
    :param _timeout: timeout (s)
    :return: NULL
    """
    if _file_name is None:
        file_name = _url.split("/")[-1]
        file_path = os.path.join(_file_dir, file_name)
    else:
        file_path = os.path.join(_file_dir, _file_name)
    try:
        if not os.path.exists(_file_dir):
            os.mkdir(_file_dir)
        if not os.path.exists(file_path):
            with requests.Session() as sess:
                response = sess.get(url=_url, timeout=_timeout, stream=True)
                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                    print("The file is saved successfully.")
        else:
            print("The file has already existed.")
    except NotImplementedError:
        print("Fail.")


def get_html_text(_url, _timeout=10):
    """
    get the html content from the page
    :param _url: the url of the page
    :param _timeout: timeout (s)
    :return:
    """
    try:
        with requests.Session() as sess:
            _headers = get_agent()
            response = sess.get(_url, headers=_headers, timeout=_timeout)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            text = response.text
    except NotImplementedError:
        text = ""

    return text


def html_write(_html, _file_path):
    """
    write a html file into a file
    :param _html: html content
    :param _file_path: the file path
    :return:
    """
    try:
        with open(_file_path, "w") as file:
            file.write(_html)
        print("The html file is saved successfully.")
    except NotImplementedError:
        print("The html file is not saved successfully.")


def html_read(_file_path):
    with open(_file_path, "r") as file:
        _html = file.read()

    return _html


if __name__ == "__main__":
    # download multimedia
    print(__doc__)
    # url = "http://f2.topitme.com/2/b9/71/112660598401871b92l.jpg"
    # file_dir = "E:/Myself/1.source_code/crawler/image"
    # download_media(_url=url, _file_dir=file_dir)

    # download html content
    # html = get_html_text("http://www.zuihaodaxue.cn/zuihaodaxuepaiming2016.html")
    # html_write(html, "E:/Myself/1.source_code/crawler/text.txt")
