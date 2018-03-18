#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 
Finished on 
@author: Wang Yuntao
"""

from crawl import *
import bs4
from bs4 import BeautifulSoup

"""
    function:
        get_ip_belong(ip, headers=None, timeout=3)                      获取IP归属地
"""


def get_ip_belong(ip, _headers=None, timeout=3):
    """
    get the ip belonging
    :param ip: ip address
    :param _headers: user agent
    :param timeout: timeout (s)
    :return: belonging
    """
    _url = "http://www.ip138.com/ips138.asp?ip="
    url = _url + ip + "&action=2"
    _html = get_html_text(url, _headers=_headers, timeout=timeout)
    soup = BeautifulSoup(_html, "html.parser")
    for tr in soup.find_all("table"):
        if isinstance(tr, bs4.element.Tag):
            print(tr)
    # table = soup.find_all("table")

    # print(table)
    # for tr in soup.find("tbody").children:
    #     print(tr)


if __name__ == "__main__":
    # get user agent info
    agent_file_path = "E:/Myself/1.source_code/crawler/user_agents.txt"
    headers = get_agent(agent_file_path)
    ip = "222.24.56.12"

    get_ip_belong(ip, _headers=headers, timeout=10)
