#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 
Finished on 
@author: Wang Yuntao
"""
from crawl import *
import re

"""
    function:
        get_goods_prince(_goods, number)                根据
        page_parser(_html)                              对爬取到的html进行解析
        print_goods_list(_goods_list)                   对商品信息进行打印
        
"""


def page_parser(_html):
    """
    page parser
    :param _html: html content
    :return: _goods_list
    """
    _goods_list = []
    pattern_price = re.compile(r'"view_price":"[\d.]*"')
    pattern_title = re.compile(r'"raw_title":".*?"')
    prices = pattern_price.findall(_html)
    titles = pattern_title.findall(_html)
    for index in range(len(prices)):
        price = eval(prices[index].split(":")[1])
        title = eval(titles[index].split(":")[1])
        _goods_list.append([price, title])

    return _goods_list


def print_goods_list(_goods_list):
    """
    print the goods list
    :param _goods_list: goods list
    :return:
    """
    tplt = "{:^5}{:^15}{:^30}"
    print(tplt.format("Index", "Price", "Goods", chr(12288)))
    count = 0
    for _goods in _goods_list:
        count = count + 1
        print(tplt.format(count, _goods[0], _goods[1], chr(12288)))


def get_goods_prince(_goods, number):
    """
    get the price of the goods according to the its name
    :param _goods: the name of the goods (str)
    :param number:
    :return:
    """
    depth = number // 44 + 1
    start_url = "http://s.taobao.com/search?q=" + _goods
    _goods_list = []

    for page in range(depth):
        try:
            _url = start_url + "&s=" + str(44 * page)
            _html = get_html_text(_url)
            _goods_list.extend(page_parser(_html))
        except NotImplementedError:
            continue

    _goods_list = _goods_list[: number]

    return _goods_list


if __name__ == "__main__":
    goods = "面包"
    goods_list = get_goods_prince(goods, 20)
    print_goods_list(goods_list)
