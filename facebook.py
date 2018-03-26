#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018.03.09
Finished on 
@author: Wang Yuntao
"""

from crawl import *
import re, time, pickle, random


token = "EAACEdEose0cBACrrYenWFagOcG3CO1pCeQSfZBgnfVGSbVGtxr3EmMcu3k2ezCGy3dPeHqAMCHZBCFNZBZC36Km09RbD6kWXtkm62rtupkx453JZAGKTn6jqicRyJZBn8BeL375dy7ovX3Und40z" \
        "jZCNT3UWGoZCYUK9wZBcVjFmlnrEuI8IunZCq6q3rkP5lkGOxAh5dewuT8Q6axbSRfhnGB9hEGp95rX88ZD"


def make_request(_id="me"):
    _request = _id + " "

    return _request


def get_response_from_facebook(_request):
    url_root = "http://graph.facebook.com/v2.12/"
    _url = url_root + _request
    response = requests.get(url_root + _request, {"access_token": token})

    return response


if __name__ == "__main__":
    agent_file_path = "E:/Myself/1.source_code/crawler/user_agents.txt"
    url = "https://www.facebook.com"
    headers = get_agent(agent_file_path)
    html = get_html_text(url, headers)
