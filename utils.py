#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 
Finished on 
@author: Wang Yuntao
"""

import time

"""
    function:
        get_time(_unix_time_stamp)                  unix时间戳 -> "%Y-%m-%d %H:%M:%S"格式的时间
        get_unix_stamp(_time_string)                "%Y-%m-%d %H:%M:%S"格式的时间 -> unix时间戳
"""


def get_time(_unix_time_stamp):
    """
    unix时间戳 -> "%Y-%m-%d %H:%M:%S"格式的时间
    e.g. 1522048036 -> 2018-03-26 15:07:16
    :param _unix_time_stamp: unix时间戳
    :return: "%Y-%m-%d %H:%M:%S"格式的时间
    """
    _format = "%Y-%m-%d %H:%M:%S"
    value = time.localtime(_unix_time_stamp)
    _time_string = time.strftime(_format, value)

    return _time_string


def get_unix_stamp(_time_string):
    """
    "%Y-%m-%d %H:%M:%S"格式的时间 -> unix时间戳
    :param _time_string: "%Y-%m-%d %H:%M:%S"格式的时间
    :return: unix时间戳
    """
    _format = "%Y-%m-%d %H:%M:%S"
    time.strptime(_time_string, _format)
    _unix_time_stamp = time.mktime(time.strptime(_time_string, _format))

    return int(_unix_time_stamp)


if __name__ == "__main__":
    d = get_unix_stamp('2012-03-28 06:53:40')
    print(d)
    s = get_time(1332888820)
    print(s)
