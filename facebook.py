#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018.03.09
Finished on 
@author: Wang Yuntao
"""

from crawl import *
import re


if __name__ == "__main__":
    agent_file_path = "E:/Myself/1.source_code/crawler/user_agents.txt"
    url = "https://www.facebook.com"
    headers = get_agent(agent_file_path)
    html = get_html_text(url, headers)
