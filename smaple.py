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
    keyword_list = []
    #f = codecs.open("C:\\Users\\t_yamamoto\\Documents\\workspace\\RakutenSearch\\src\\keywordlist3.dat", 'r', 'utf-8')
    f = codecs.open('keywordlist3.dat','r','utf-8')
    lines = f.readlines()
    f.close()
    for i in range(6):
        r = random.randint(0, len(lines)-1)
        keyword_list.append(lines[r].rstrip("\r\n"))
    return keyword_list

def main():
    keywords = getKeyword()
    print(keywords)

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

    '''
    driver.get('http://www.rakuten.co.jp/')
    assert '【楽天市場】Shopping is Entertainment! ： インターネット最大級の通信販売、通販オンラインショッピングコミュニティ' in driver.title

    elem = driver.find_element(By.CLASS_NAME, 'infoseek')
    elem.click()
    wait.until(EC.presence_of_element_located((By.ID,'qt1')))

    print(driver.current_url)
    print(driver.title)

    elem = driver.find_element(By.ID, 'qt1')
    elem.send_keys(keywords[0] + Keys.RETURN)
    '''

    driver.get('https://pex.jp/login')
    assert 'ログイン | ポイント交換のPeX' in driver.title

    elem = driver.find_element(By.NAME,'pex_user_login[email]')
    elem.send_keys(obj['Credential'][0]['Email'])

    elem = driver.find_element(By.NAME, 'pex_user_login[password]')
    elem.send_keys(obj['Credential'][0]['Password'] + Keys.RETURN)

    print(driver.current_url)
    print(driver.title)

    wait.until(EC.presence_of_element_located((By.ID,'keyword')))

    print(driver.current_url)
    print(driver.title)

    elem = driver.find_element_by_id('keyword')
    elem.send_keys(keywords[0] + Keys.RETURN)

    print(driver.current_url)
    print(driver.title)

    wait.until(EC.presence_of_element_located((By.ID,'keyword')))

    print(driver.current_url)
    print(driver.title)


if __name__ == '__main__':
    main()
