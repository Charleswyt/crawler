#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 
Finished on 
@author: Wang Yuntao
"""

import json
from crawl import *
from urllib.parse import urlencode


def get_page_index(_keyword, _offset=0):
    data = {
        "offset": _offset,
        "format": "json",
        "keyword": _keyword,
        "autoload": "true",
        "count": "20",
        "cur_tab": 1
    }
    _url = "https://www.toutiao.com/search_content/?" + urlencode(data)
    _html = get_html_text(_url)

    return _html


def parse_page_index(_html):
    data = json.loads(_html)
    if data and "data" in data.keys():
        for item in data.get("data"):
            yield item.get("article_url")


if __name__ == "__main__":
    # get user agent info
    agent_file_path = "E:/Myself/1.source_code/crawler/user_agents.txt"
    headers = get_agent(agent_file_path)

    # crawler
    keyword = "两会"
    content = get_page_index(keyword)
    for url in parse_page_index(content):
        html = get_html_text(url, )
