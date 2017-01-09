import urllib, http.cookiejar, socket
import random
import codecs
import time
from subprocess import check_call
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json


def getKeyword():
    key_list = []
    #f = codecs.open("C:\\Users\\t_yamamoto\\Documents\\workspace\\RakutenSearch\\src\\keywordlist3.dat", 'r', 'utf-8')
    f = codecs.open('keywordlist.dat','r','utf-8')
    lines = f.readlines()
    f.close()
    for i in range(6):
        r = random.randint(0, len(lines)-1)
        key_list.append(lines[r].rstrip("\r\n"))
    return key_list

def main():
    keyword_list = getKeyword()
    print(keyword_list)

    # ファイルを読み込みモードでオープン
    with open('pex_data.json', 'r') as f:
     # ファイルから読み込み
        obj = json.load(f)
        #print(obj)
        #print("---")
        #print(json.dumps(obj, sort_keys = True, indent = 2))

    driver = webdriver.Firefox()
    driver.implicitly_wait(1)
    wait = WebDriverWait(driver, 10)


    driver.get('https://pex.jp/login')
    assert 'ログイン | ポイント交換のPeX' in driver.title

    elem = driver.find_element(By.NAME,'pex_user_login[email]')
    elem.send_keys(obj['Credential'][0]['Email'])

    elem = driver.find_element(By.NAME, 'pex_user_login[password]')
    elem.send_keys(obj['Credential'][0]['Password'] + Keys.RETURN)


    for each in keyword_list:
        print(each)
        wait.until(EC.presence_of_element_located((By.ID,'keyword')))
        elem = driver.find_element_by_id('keyword')
        elem.send_keys(each + Keys.RETURN)

        for j in range(30):
            print('*', end='', flush='ture')
            time.sleep(9+random.randint(1, 4))


    print("End of Script")


if __name__ == '__main__':
    main()
