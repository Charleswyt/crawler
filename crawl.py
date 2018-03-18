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
        load_user_agent(file_path)                                      从本地加载User Agent文件
        get_agent(file_path)                                            从本地加载User Agent文件，并随机获取一个User Agent
        download_media(_url, _file_dir, _headers=None, timeout=3)       给定媒体链接，并对其进行下载
        get_html_text(_url, _headers=None, timeout=3)                   获取网页的html文本内容
"""


def load_user_agent(file_path):
    """
    load agent from disk
    :param file_path: the agent file path
    :return: agents_list
    """
    agents_list = []
    with open(file_path, "r") as file:
        for line in file.readlines():
            if line is not None:
                agents_list.append(line.strip()[1:-1 - 1])
    random.shuffle(agents_list)

    return agents_list


def get_agent(file_path):
    """
    get an user agent randomly
    :param file_path: the agent file path
    :return: headers
    """
    agents = load_user_agent(file_path)
    agent = random.choice(agents)
    headers = {"User-Agent": agent}

    return headers


def download_media(_url, _file_dir, _headers=None, timeout=3):
    """
    download image, video, audio from the internet
    :param _url: url
    :param _file_dir: the folder used for multimedia save
    :param _headers: user-agent
    :param timeout: timeout (s)
    :return: NULL
    """
    file_name = _url.split("/")[-1]
    file_path = os.path.join(_file_dir, file_name)
    try:
        if not os.path.exists(_file_dir):
            os.mkdir(_file_dir)
        if not os.path.exists(file_path):
            with requests.Session() as sess:
                response = sess.get(url=url, headers=headers, timeout=timeout)
                print(len(response.text))
                with open(file_path, "wb") as file:
                    file.write(response.content)
                    print("The file is saved successfully.")
        else:
            print("The file has already existed.")
    except NotImplementedError:
        print("Fail.")


def get_html_text(_url, _headers=None, timeout=3):
    """
    get the html content from the page
    :param _url: the url of the page
    :param _headers: user agent
    :param timeout: timeout (s)
    :return:
    """
    try:
        with requests.Session() as sess:
            response = sess.get(_url, headers=_headers, timeout=timeout)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            text = response.text
    except NotImplementedError:
        text = ""

    return text


def html_write(_html, file_path):
    """
    write a html file into a file
    :param _html: html content
    :param file_path: the file path
    :return:
    """
    try:
        with open(file_path, "w") as file:
            file.write(_html)
        print("The html file is saved successfully.")
        return True
    except NotImplementedError:
        print("The html file is not saved successfully.")
        return False


if __name__ == "__main__":
    # get user agent info
    agent_file_path = "E:/Myself/1.source_code/crawler/user_agents.txt"
    headers = get_agent(agent_file_path)

    # download multimedia
    url = "http://f2.topitme.com/2/b9/71/112660598401871b92l.jpg"
    file_dir = "E:/Myself/1.source_code/crawler/image"
    download_media(_url=url, _file_dir=file_dir, _headers=headers)

    # download html content
    html = get_html_text("http://www.zuihaodaxue.cn/zuihaodaxuepaiming2016.html", _headers=headers)
    html_write(html, "E:/Myself/1.source_code/crawler/text.txt")
