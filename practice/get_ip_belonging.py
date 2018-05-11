#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 
Finished on 
@author: Wang Yuntao
"""

from crawl import *
from bs4 import BeautifulSoup

"""
    function:
        get_ip_belong(ip, headers=None, timeout=3)                      获取IP归属地
"""


def get_ip_belong(_ip, _timeout=3):
    """
    get the ip belonging
    :param _ip: ip address
    :param _timeout: timeout (s)
    :return: belonging
    """
    _url = "http://www.ip138.com/ips138.asp?ip="
    ip_url = _url + _ip
    _html = get_html_text(ip_url, _timeout=_timeout)
    soup = BeautifulSoup(_html, "html.parser")
    data = soup.find("li")
    data_content = data.string
    _belonging = data_content.split("：")[1]

    return _belonging


if __name__ == "__main__":
    ip = "222.23.56.12"
    belonging = get_ip_belong(ip)
    print("ip归属地：%s" % belonging)
