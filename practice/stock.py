#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 
Finished on 
@author: Wang Yuntao
"""

import re
import traceback
from crawl import *
from bs4 import BeautifulSoup

"""
    function:
        get_stocks_list(_url, _timeout=3)                               获取股票列表
        get_stocks_info(_stock_list, _stock_url, _number=10)            获取股票信息
        get_stock_id(_stock_name)                                       通过股票名获取股票编号
        get_stock_info_id(_stock_id)                                    通过股票编号获取股票信息
        get_stock_info_name(_stock_name)                                通过股票名字获取股票信息
        show_stock_info(_stock_info_dict)                               显示股票信息
"""


def get_stocks_list(_url):
    """
    get the stock list
    content: <li><a target="_blank" href="http://quote.eastmoney.com/sh502007.html">国企改A(502007)</a></li>
    :param _url: url
    :return: a list of stocks
    """
    _html = get_html_text(_url=_url)
    soup = BeautifulSoup(_html, "html.parser")
    a = soup.find_all("a")
    _stocks_list = []
    for item in a:
        try:
            href = item.attrs["href"]
            pattern = re.compile(r"[s][hz]\d{6}")
            _stocks_list.append(pattern.findall(href)[0])
        except:
            continue

    return _stocks_list


def get_stocks_info(_stocks_list, _stock_info_url, _number=10, is_write=False):
    """
    get stocks info
    :param _stocks_list: stocks list
    :param _stock_info_url: the url for getting stock info
    :param _number: the number of stocks
    :param is_write: if is_write is True, the stock info is writen in a text file
    :return: stocks info list
    """
    _stocks_list = _stocks_list[:_number]
    _stocks_info_list = []
    for stock in _stocks_list:
        _url = _stock_info_url + stock + ".html"
        _html = get_html_text(_url)
        try:
            if _html == "":
                continue
            else:
                _stock_info_dict = {}
                soup = BeautifulSoup(_html, "html.parser")
                _stock_info = soup.find("div", attrs={"class": "stock-bets"})
                name = _stock_info.find_all(attrs={"class": "bets-name"})[0]
                _stock_info_dict.update({"股票名": name.text.split()[0]})

                key_list = _stock_info.find_all("dt")
                value_list = _stock_info.find_all("dd")
                if key_list is None:
                    continue
                else:
                    for index in range(len(key_list)):
                        key = key_list[index].text
                        value = value_list[index].text
                        _stock_info_dict[key] = value
                        if "跌停" in _stock_info_dict.keys():
                            _stock_info_dict["跌停"] = _stock_info_dict["跌停"].split(" ")[-1]
        except:
            traceback.print_exc()
            continue
        _stocks_info_list.append(_stock_info_dict)

    return _stocks_info_list


def get_stock_id(_stock_name):
    """
    get stock id
    :param _stock_name: stock name
    :return: stock id
    """
    _stock_list_url = "http://quote.eastmoney.com/stocklist.html"
    _html = get_html_text(_stock_list_url)
    soup = BeautifulSoup(_html, "html.parser")

    quote_body = soup.find("div", attrs={"class": "quotebody"})
    li_a = quote_body.find_all("a")
    _stock_id = []
    for item in li_a:
        if item.text.split("(")[0] == _stock_name:
            href = item.attrs["href"]
            pattern = re.compile(r"[s][hz]\d{6}")
            _stock_id = pattern.findall(href)[0]
            break

    return _stock_id


def get_stock_info_id(_stock_id):
    """
    get stock info
    :param _stock_id: the id of the stock
    :return: stock info dict
    """
    _stock_info_url = "https://gupiao.baidu.com/stock/"
    _url = _stock_info_url + _stock_id + ".html"
    _html = get_html_text(_url)
    soup = BeautifulSoup(_html, "html.parser")
    _stock_info = soup.find("div", attrs={"class": "stock-bets"})
    _stock_name = _stock_info.find_all(attrs={"class": "bets-name"})[0]
    _stock_name = _stock_name.text.split()[0]
    key_list = _stock_info.find_all("dt")
    value_list = _stock_info.find_all("dd")

    _stock_info_dict = {}
    for index in range(len(key_list)):
        key = key_list[index].text.split()[0]
        value = value_list[index].text
        _stock_info_dict[key] = value
    _stock_info_dict["跌停"] = _stock_info_dict["跌停"].split(" ")[-1]
    _stock_info_dict["股票名"] = _stock_name

    return _stock_info_dict


def get_stock_info_name(_stock_name):
    """
    get stock info
    :param _stock_name: the id of the stock
    :return: stock info dict
    """
    _stock_id = get_stock_id(_stock_name)
    _stock_info_url = "https://gupiao.baidu.com/stock/"
    _url = _stock_info_url + _stock_id + ".html"
    _html = get_html_text(_url)
    soup = BeautifulSoup(_html, "html.parser")
    _stock_info = soup.find("div", attrs={"class": "stock-bets"})
    _stock_name = _stock_info.find_all(attrs={"class": "bets-name"})[0]
    _stock_name = _stock_name.text.split()[0]
    key_list = _stock_info.find_all("dt")
    value_list = _stock_info.find_all("dd")

    _stock_info_dict = {}
    for index in range(len(key_list)):
        key = key_list[index].text.split()[0]
        value = value_list[index].text
        _stock_info_dict[key] = value
    _stock_info_dict["跌停"] = _stock_info_dict["跌停"].split(" ")[-1]
    _stock_info_dict["股票名"] = _stock_name

    return _stock_info_dict


def show_stock_info(_stock_info_dict):
    """
    show stock info
    :param _stock_info_dict: stock info dict
    :return: NULL
    """
    print("股票名: %s" % _stock_info_dict["股票名"])
    del _stock_info_dict["股票名"]

    for item in _stock_info_dict:
        print("%s: %s" % (item, _stock_info_dict[item]))


if __name__ == "__main__":
    # module 1
    # stock_name = "宏图高科"
    # stock_id = get_stock_id(stock_name)
    # stock_info = get_stock_info_id(stock_id)
    # show_stock_info(stock_info)

    # module 2
    # stock_name = "宏图高科"
    # stock_info = get_stock_info_name(stock_name)
    # show_stock_info(stock_info)

    # module 3
    stock_list_url = "http://quote.eastmoney.com/stocklist.html"
    stock_info_url = "https://gupiao.baidu.com/stock/"
    stocks_list = get_stocks_list(stock_list_url)
    stocks_info_list = get_stocks_info(stocks_list, stock_info_url, 10)
    print(stocks_info_list)
    # stocks_info_list = get_stocks_info(stocks_list)
    # print(stocks_info_list)


