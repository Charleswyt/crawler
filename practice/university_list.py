#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018.03.18
Finished on  2018.03.18
@author: Wang Yuntao
"""

from crawl import *
import bs4
from bs4 import BeautifulSoup

"""
    function:
        get_html(_year=2016)                                            根据指定年份获取html内容
        get_univ_list(_html)                                            使用BeautifulSoup对html进行解析，生成大学排名列表
        print_univ_list(university_list, _number)                       对大学排名列表进行展示
        get_univ_rank(university_name, _year)                           根据大学名判断其制定年份的排名
        get_univ_location((university_name)                             根据大学名判断其所在省份
        
"""


def get_html(_year=2016):
    """
    get html content
    :param _year: year
    :return:
    """

    """url:
        2015: http://www.zuihaodaxue.cn/zuihaodaxuepaiming2015_0.html
        2016: http://www.zuihaodaxue.cn/zuihaodaxuepaiming2016.html
        2017: http://www.zuihaodaxue.cn/zuihaodaxuepaiming2017.html
        2018: http://www.zuihaodaxue.cn/zuihaodaxuepaiming2018.html
    """
    years = [2015, 2016, 2017, 2018]
    if _year in years:
        if _year == 2015:
            _url = "http://www.zuihaodaxue.cn/zuihaodaxuepaiming" + str(_year) + "_0" + ".html"
        else:
            _url = "http://www.zuihaodaxue.cn/zuihaodaxuepaiming" + str(_year) + ".html"
    else:
        _url = "http://www.zuihaodaxue.cn/zuihaodaxuepaiming" + str(_year) + ".html"

    _html = get_html_text(_url=_url)

    return _html


def get_univ_list(_html):
    """
    get university list
    :param _html: html content
    :return:
    """
    university_list = []
    soup = BeautifulSoup(_html, "html.parser")
    for tr in soup.find("tbody").children:
        if isinstance(tr, bs4.element.Tag):
            tds = tr("td")
            university_list.append([tds[0].string, tds[1].string, tds[2].string])

    return university_list


def print_univ_list(university_list, _number):
    """
    print the university list
    :param university_list: university list
    :param _number: the number of university to be showed
    :return: NULL
    """
    tplt_title = "{0:^10}{1:{3}^15}{2:^10}"
    tplt_content = "{0:^9}{1:{3}^10}{2:^10}"
    print(tplt_title.format("Index", "University", "Province", chr(12288)))
    for i in range(_number):
        u = university_list[i]
        print(tplt_content.format(u[0], u[1], u[2], chr(12288)))


def get_univ_rank(university_name, _year):
    """
    get the rank of the university in specific year
    :param university_name: the name of the university
    :param _year: year
    :return: the rank of the university, if not exist, return None
    """
    _html = get_html(_year)
    university_list = get_univ_list(_html)
    _rank = None
    for university in university_list:
        if university[1] == university_name:
            _rank = university[0]
            break
        else:
            continue

    return _rank


def get_univ_location(university_name):
    """
    get the location of the university from its name
    :param university_name: the name of the university
    :return: its location, if not exist, return None
    """
    _html = get_html(year)
    university_list = get_univ_list(_html)
    location = None
    for university in university_list:
        if university[1] == university_name:
            location = university[2]
            break
        else:
            continue

    return location


if __name__ == "__main__":
    year, number = 2016, 10
    html = get_html(year)
    univ_list = get_univ_list(html)
    print_univ_list(univ_list, number)
