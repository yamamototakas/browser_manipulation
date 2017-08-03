# -*- coding: utf-8 -*-

'''
Created on May 03, 2014

@author: tyama
'''
import urllib
import http.cookiejar
import socket
import random
import codecs
import time
import shlex
import sys
import psutil
import os
import signal

from subprocess import check_call
from subprocess import Popen


if __name__ == '__main__':

    keyword_list = []
    f = codecs.open("keywordlist.dat", 'r', 'utf-8')
    # f=open('keywordlist3.dat','r')
    lines = f.readlines()
    f.close()
    print("EndOfFileClose")
    for i in range(33):
        r = random.randint(0, len(lines) - 1)
        keyword_list.append(lines[r].rstrip("\r\n"))
    print(keyword_list, "Waiting before start")
    url = 'http://websearch.rakuten.co.jp/Web?col=OW&svx=101102&ref=chexti_r&qt=' \
        + urllib.parse.quote_plus("First", encoding="utf-8")

    try:
        cmd = "C:/Program Files (x86)/Mozilla Firefox/firefox.exe " + url
        proc = Popen(shlex.split(cmd))
    except Exception as err:
        print("ERROR in '", cmd, "' : ", sys.exc_info())
    time.sleep(10)

    for each in keyword_list:
        print(each)
        url = 'http://websearch.rakuten.co.jp/Web?col=OW&svx=101102&ref=chexti_r&qt=' \
            + urllib.parse.quote_plus(each, encoding="utf-8")
        print(url)

        try:
            cmd = "C:/Program Files (x86)/Mozilla Firefox/firefox.exe " + url
            proc = Popen(shlex.split(cmd))
            # check_call(
            #     ["C:/Program Files (x86)/Mozilla Firefox/firefox.exe", " http://hapitas.jp/"])
        except Exception as err:
            print("ERROR in '", cmd, "' : ", sys.exc_info())

        # check_call(["C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        #             " --disable-images", url])
        time.sleep(random.randint(5, 8) + random.randint(4, 8))

    # time.sleep(2)

    print('ENDENDEND')
    time.sleep(5)
