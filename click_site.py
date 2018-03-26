# -*- coding: utf-8 -*-
import browser_cookie3
import random
import re
import requests
import sys
import shlex
import time
import socket
import ipaddress
from subprocess import Popen


HEADERS = {
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Referer": "http://hapitas.jp/",
    "Accept-Encoding": "gzip,deflate",
    "Accept-Language": "ja,en-US,en;q=0.5"
}


URL_LIST = (
    'http://hapitas.jp/index/ajaxclickget',
    # 'http://goolge.com',
)


proxies = {
}


def get_title(html):
    return re.findall('<title>(.*?)</title>', html, flags=re.DOTALL)[0].strip()


def main():
    print(URL_LIST)
    base_url = 'http://hapitas.jp/'

    req_session = requests.session()
    # cj = browser_cookie3.load()
    cj = browser_cookie3.firefox()
    # cj = browser_cookie3.chrome()
    # print (cj)
    ip = ipaddress.ip_address(socket.gethostbyname(socket.gethostname()))
    nw = ipaddress.ip_network('10.41.192.0/18')
    print("IP address: ", ip)
    proxies = {}
    if(ip in nw):
        proxies = {
            'http': 'http://10.254.254.180:3128',
            'https': 'http://10.254.254.7:3128'
        }
    print("proxy: ", proxies)


    # check = req_session.get(base_url, headers=HEADERS, cookies=cj).text
    check = req_session.get(base_url, proxies=proxies, headers=HEADERS, cookies=cj).text

    if '会員ログイン' in check:
        print("Please login from the browser")
        print(check.find('会員ログイン'))
        return 1

    for each_url in URL_LIST:
        print(each_url)

        # page = req_session.get(each_url, headers=HEADERS, cookies=cj).text
        page = req_session.get(each_url, proxies=proxies, headers=HEADERS, cookies=cj).text

        url_list = []
        url2 = []
        key = '(clickget.recive.+top_clickget)'
        pattern = re.compile(key)
        result = pattern.findall(page)
        print("1st result", result)

        for each in result:
            url_list.append(base_url + each)
        url_list = list(set(url_list))
        print(url_list)

        for each in url_list:
            # page2 = req_session.get(each, headers=HEADERS, cookies=cj).text
            page2 = req_session.get(each, proxies=proxies, headers=HEADERS, cookies=cj).text

            print("serch for each url=", each)
            # http://hapitas.jp/condition/index/item_id/60551/apn/top_clickget/click_get/1635/fixed_point/2300/up_point/5000/point_type/0/zero_point_flg/0
            # http://hapitas.jp/condition/index/item_id/60551/apn/top_clickget/click_get/1635/fixed_point/2300/up_point/5000/point_type/0/zero_point_flg/0
            # http://hapitas.jp/item/redirect/itemid/34158/p/0/click/1633/apn/top_clickget/linkid/387
            # http://hapitas.jp/item/redirect/itemid/52128/p/0/click/1634/apn/top_clickget
            # http://hapitas.jp/item/redirect/itemid/65202/p/0/click/2566/apn/top_clickget/linkid/856

            # key2 = '(item\/|condition\/)(.+top_clickget.*)("\sclass|"\s>)'
            key2 = '(item\/)(.+top_clickget.*)("\sclass)'
            pattern2 = re.compile(key2)
            result2 = pattern2.findall(page2)
            print(result2)
            # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') # Here
            # print(page2

            if result2:
                temp_url = base_url + result2[0][0] + result2[0][1]

                if result2[0][0] == 'condition/':
                    # page3 = req_session.get(temp_url, headers=HEADERS, cookies=cj).text
                    page3 = req_session.get(temp_url, proxies=proxies, headers=HEADERS, cookies=cj).text

                    payloadkey3 = '(item\/)(.+top_clickget.*)("\sclass)'
                    pattern3 = re.compile(payloadkey3)
                    result3 = pattern3.findall(page3)

                    if result3:
                        temp_url = base_url + result3[0][0] + result3[0][1]

                url2.append(temp_url)

        url2 = list(set(url2))
        print(url2)

        for each in url2:
            print("url =", each)
            try:
                # page4 = req_session.get(each, headers=HEADERS, cookies=cj)
                page4 = req_session.get(each, proxies=proxies, headers=HEADERS, cookies=cj)
            except Exception as err:
                print("--------------------------------------------")
                print(" Error happens in sending GET to the following page")
                print(" URL = ", each)
                print("--------------------------------------------")
                print(" ERROR : ", sys.exc_info())
                # print traceback.format_exc(sys.exc_info()[2])
            finally:
                time.sleep(random.randint(1, 2) + random.randint(0, 1))

    try:
        # cmd = "C:/Program Files (x86)/Mozilla Firefox/firefox.exe -P 'selenium' " + base_url
        cmd = "C:/Program Files (x86)/Mozilla Firefox/firefox.exe " + base_url
        proc = Popen(shlex.split(cmd))
        # check_call(
        #     ["C:/Program Files (x86)/Mozilla Firefox/firefox.exe", " http://hapitas.jp/"])
    except Exception as err:
        print("ERROR in '", cmd, "' : ", sys.exc_info())

    print('ENDENDEND')
    time.sleep(5)
    return 0


if __name__ == '__main__':
    main()
