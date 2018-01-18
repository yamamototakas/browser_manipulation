# -*- coding: utf-8 -*-

import codecs
import copy
import http.cookiejar
import json
import pickle
import random
import re
import socket
import sys
import time
import urllib
import pdb
import traceback
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


def getKeyword(num):
    key_list = []
    with codecs.open('keywordlist.dat', 'r', 'utf-8') as f:
        lines = f.readlines()

    for i in range(num):
        r = random.randint(0, len(lines) - 1)
        key_list.append(lines[r].rstrip("\r\n"))
    return key_list


def numToOridnal(n):
    suffixes = ("th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th")

    i = (n % 100)
    j = 0 if (i > 10 and i < 20) else (n % 10)
    return "{0}{1}".format(n, suffixes[j])


def get_progressbar_str(max_len, progress):
    status = int(max_len * progress)
    space = max_len - status
    return ('[' + '=' * status + ' ' * space + '] %.1f%%' % (progress * 100.))


def searchWord(driver, wait, keyword):
    try:
        print('Start of search')
        driver.get('http://pex.jp/search/index')
        print('    moved to "search page"')

        time.sleep(2)
        wait.until(EC.presence_of_element_located((By.ID, 'keyword')))
        elem = driver.find_element_by_id('keyword')
        elem.send_keys(keyword + Keys.RETURN)
        print('    searched by "{0}"'.format(keyword))
        print('End of search')

    except NoSuchElementException as err:
        print('Cannot find element: {0}'.format(err))
    except TimeoutException as err:
        print('Cannot find element, then timeout in waiting: {0}'.format(err))
    except Exception as err:
        print('Eception: {0}'.format(err))
        print("ERROR in [serach]: ", sys.exc_info())

    return True


def clickQuiz(driver, wait):
    try:
        print('Start of quiz')
        driver.get('http://pex.jp/point_quiz')
        print('    moved to "quiz page"')

        time.sleep(2)
        r = random.randint(1, 4)
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, '/html/body/section/article/section/ul/li[{0}]/a'.format(r))))
        elem = driver.find_element(
            By.XPATH, '/html/body/section/article/section/ul/li[{0}]/a'.format(r))
        elem.click()
        print('    clicked {0} answer in "quize page"'.format(numToOridnal(r)))

        time.sleep(3)
        alert = driver.switch_to.alert
        alert.accept()
        print('    accepted in dialogue')
        time.sleep(3)
        print('End of quiz')
    except NoSuchElementException as err:
        print('Cannot find element: {0}'.format(err))
    except TimeoutException as err:
        print('Cannot find element, then timeout in waiting: {0}'.format(err))
    except Exception as err:
        print("ERROR in [quiz]: ", sys.exc_info())
    return True


def clickPekutan(driver, wait):
    try:
        print('Start of pekutan')
        driver.get('http://pex.jp/pekutan/words/current')
        print('    moved to "pekutan page"')

        time.sleep(2)
        r = random.randint(1, 2)

        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'body > section > article > section > ul \
                                    > li:nth-child({0}) > form > input.btn'.format(r))))
        elem = driver.find_element(
            By.CSS_SELECTOR, 'body > section > article > section > ul \
                                   > li:nth-child({0}) > form > input.btn'.format(r))
        elem.click()
        print('    clicked {0} item for first word'.format(numToOridnal(r)))
        driver.get('http://pex.jp/pekutan/words/current')

        time.sleep(4)
        r = random.randint(1, 2)

        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'body > section > article > section > ul\
                                    > li:nth-child({0}) > form > input.btn'.format(r))))
        elem = driver.find_element(
            By.CSS_SELECTOR, 'body > section > article > section > ul\
                                   > li:nth-child({0}) > form > input.btn'.format(r))
        elem.click()
        print('    clicked {0} item for Second word'.format(numToOridnal(r)))
        print('End of pekutan')
    except NoSuchElementException as err:
        print('Cannot find element: {0}'.format(err))
    except TimeoutException as err:
        print('Cannot find element, then timeout in waiting: {0}'.format(err))
    except Exception as err:
        print("ERROR in [pekutan]: ", sys.exc_info())

    return True


def clickSeal(driver, wait):
    try:
        print('Start of seal')
        driver.get('http://pex.jp/seal/mekutte')
        print('    moved to "mekutte seal page"')

        time.sleep(4)
        r = random.randint(1, 4)

        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '#serve > li:nth-child({0}) > form > input.card0{0}'.format(r))))
        elem = driver.find_element(
            By.CSS_SELECTOR, '#serve > li:nth-child({0}) > form > input.card0{0}'.format(r))
        elem.click()
        print('    clicked {0} seal'.format(numToOridnal(r)))
        time.sleep(4)
        print('End of seal')
    except NoSuchElementException as err:
        print('Cannot find element: {0}'.format(err))
    except TimeoutException as err:
        print('Cannot find element, then timeout in waiting: {0}'.format(err))
    except Exception as err:
        print("ERRO in [seal]: ", sys.exc_info())

    return True


def hintCheck(words):
    mapping = {
        "無料会員登録": "http://pex.jp/point_actions/list/free_register",
        "キャンペーン応募": "http://pex.jp/point_actions/list/campaign",
        "カード発行": "http://pex.jp/point_actions/list/card",
        "口座開設": "http://pex.jp/point_actions/list/open_account",
        "資料請求": "http://pex.jp/point_actions/list/document_request",
        "査定・見積もり": "http://pex.jp/point_actions/list/assessment",
        "相談": "http://pex.jp/point_actions/list/consultation",
        "ゲーム起動": "http://pex.jp/point_actions/list/start_up_game",
        "会員登録後のアクション": "http://pex.jp/point_actions/list/register_and_action",
        "中古買取り": "http://pex.jp/point_actions/list/used_item_purchase",
        "無料その他": "http://pex.jp/point_actions/list/free_point_action_other",
        "有料会員登録": "http://pex.jp/point_actions/list/charge_register",
        "旅行": "http://pex.jp/point_actions/list/travel",
        "エステ体験": "http://pex.jp/point_actions/list/esthetic",
        "来店": "http://pex.jp/point_actions/list/visit_store",
        "成約・借り入れ": "http://pex.jp/point_actions/list/agree_contract",
        "ウォーターサーバー設置完了": "http://pex.jp/point_actions/list/water_server",
        "サービス利用その他": "http://pex.jp/point_actions/list/charge_point_action_other"
    }
    temp_words = '【獲得条件 : 有料会員登録 】の2,200Pの広告のページ'
    temp_words2 = '【獲得条件 : サービス利用その他 】の15,000Pの広告のページ'

    key = ':\s(.+)\s\D+([0-9,]+)\D+'
    r = re.compile(key)
    result = r.findall(words)
    end = {}
    try:
        if result:
            end["url"] = mapping[result[0][0]]
            end["point"] = result[0][1]
        print(end)
    except Exception as err:
        print("ERROR in [word mappings]: ", sys.exc_info())

    return end


def clickLookingforSeal(driver, wait):
    try:
        print('Start of looking for seal')
        driver.get('http://pex.jp/seal/mitsukete')
        print('    moved to "Looking for seal page"')

        # pdb.set_trace()

        time.sleep(4)
        wait.until(EC.visibility_of_element_located(
            (By.CLASS_NAME, 'h-lv2')))
        elem = driver.find_element(
            By.CLASS_NAME, 'h-lv2')
        words = elem.text
        print('    extracted text = ', words)

        if(words == "シール獲得状況"):
            print("    Already clicked today")
            print('End of looking for seal')
            return True

        info = hintCheck(words)
        driver.get(info["url"])
        print('    moved to "{0}"'.format(info["url"]))

        time.sleep(4)
        wait.until(EC.visibility_of_element_located(
            (By.CLASS_NAME, 'text_area')))
        max_text = driver.find_element(By.CLASS_NAME, 'number').text
        if(re.findall('[0-9]+', max_text)):
            max_num = re.findall('[0-9]+', max_text)[0]
        else:
            max_num = 1
        page = int(max_num) // 20 + 1
        print('    # of pages:', page, ', # of items:', max_num)
        isFound = False
        isClicked = False

        for i in range(1, page + 1):
            currentPage = str(i)
            currentUrl = info['url'] + '?page=' + \
                         currentPage + '&sort=point_desc'
            driver.get(currentUrl)
            print("        {0} page for searching".format(numToOridnal(i)))

            time.sleep(4)
            wait.until(EC.visibility_of_element_located(
                (By.CLASS_NAME, 'text_area')))
            nelem = driver.find_elements(By.CLASS_NAME, 'up_p')
            selem = driver.find_element(
                By.CLASS_NAME, 'service_list').find_elements(By.TAG_NAME, 'a')

            url_list = []

            for j, each in enumerate(nelem):
                if (each.text == info["point"]):
                    url_list.append(selem[j].get_attribute('href'))
            if(url_list):
                print("    URLs with same point", url_list)

            for each_url in url_list:
                driver.get(each_url)
                time.sleep(6)
                hiyoko = driver.find_elements(By.CLASS_NAME, 'hiyoko')
                if (hiyoko):
                    isFound = True
                    hiyoko[0].click()
                    time.sleep(6)

                    wait.until(
                        EC.visibility_of_element_located((By.ID, 'find')))
                    hiyoko = driver.find_element(By.ID, 'find')
                    # ActionChains(driver).move_to_element(hiyoko).click(hiyoko)
                    hiyoko.click()
                    time.sleep(3)

                    wait.until(EC.visibility_of_element_located(
                        (By.CLASS_NAME, 'card01')))
                    hiyoko = driver.find_element(By.CLASS_NAME, 'card01')
                    hiyoko.click()
                    time.sleep(3)

                    isClicked = True
                    break
                else:
                    pass

            if (isFound):
                break
            else:
                time.sleep(3)

        if(isFound and isClicked):
            print('    Found and Clicked')
        elif(isFound):
            print("    Found, but couldn't clicked")
        else:
            print('    Not found')

        print('End of looking for seal')

    except NoSuchElementException as err:
        print('Cannot find element: {0}'.format(err))
    except TimeoutException as err:
        print('Cannot find element, then timeout in waiting: {0}'.format(err))
    except Exception as err:
        print("ERROR in [looking for seal]: ", sys.exc_info())
        print("-" * 60)
        traceback.print_exc(file=sys.stdout)
        print("-" * 60)

    return True


def clickAnswer(driver, wait):
    try:
        print('Start of answer')
        driver.get('http://pex.jp/minna_no_answer/questions/current')
        print('    moved to "answer page"')

        time.sleep(2)
        r = random.randint(1, 2)

        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'body > section > article > section > ul\
                                    > li:nth-child({0}) > form'.format(r))))
        elem = driver.find_element(
            By.CSS_SELECTOR, 'body > section > article > section > ul\
                                   > li:nth-child({0}) > form'.format(r))
        elem.click()
        print('    clicked {0} answer in "answer page"'.format(
            numToOridnal(r)))
        time.sleep(4)
        print('End of answer')

    except NoSuchElementException as err:
        print('Cannot find element: {0}'.format(err))
    except TimeoutException as err:
        print('Cannot find element, then timeout in waiting: {0}'.format(err))
    except Exception as err:
        print("ERROR in [answer]: ", sys.exc_info())

    return True


def clickChirashi(driver, wait):
    try:
        print('Start of chirashi')
        driver.get('http://pex.jp/chirashi')
        print('    moved to "chirashi page"')
        time.sleep(5)

        for i in range(1, 2):
            time.sleep(5)
            wait.until(EC.visibility_of_element_located(
                (By.XPATH, '/html/body/section/section[2]/ul/li[{0}]/figure/a[2]'.format(i))))
            elem = driver.find_element(
                By.XPATH, '/html/body/section/section[2]/ul/li[{0}]/figure/a[2]'.format(i))
            elem.click()
            print('    clicked {0} ad in "chirashi page"'.format(
                numToOridnal(i)))
        print('End of chirashi')
    except NoSuchElementException as err:
        print('Cannot find element: {0}'.format(err))
    except TimeoutException as err:
        print('Cannot find element, then timeout in waiting: {0}'.format(err))
    except Exception as err:
        print("ERROR in [chirashi]: ", sys.exc_info())

    return True


def clickNews(driver, wait):
    print('Start of news')

    for i in range(1, 7):
        try:
            driver.get('http://pex.jp/point_news')
            print('    moved to "news page"')

            time.sleep(2)
            wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '#news-list > li:nth-child({0}) > figure'.format(i))))
            elem = driver.find_element(
                By.CSS_SELECTOR, '#news-list > li:nth-child({0}) > figure'.format(i))
            elem.click()
            print('    clicked {0} news in "news page"'.format(
                numToOridnal(i)))

            time.sleep(5)
            wait.until(EC.visibility_of_element_located(
                (By.ID, 'submit-cool'.format(i))))
            elem = driver.find_element(
                By.ID, 'submit-cool'.format(i))
            elem.click()
            print('    clicked cool-icon "news page"')
            time.sleep(3)

        except NoSuchElementException as err:
            print('Cannot find element in {0} news: {1}'.format(
                numToOridnal(i), err))
        except TimeoutException as err:
            print('Cannot find element in {0} news, then timeout in waiting: {1}'.format(
                numToOridnal(i), err))
        except Exception as err:
            print("ERROR in [news]: ", sys.exc_info())

    print('End of news')
    return True


def main():
    key_num = 6
    keyword_list = getKeyword(key_num)
    print(keyword_list)

    with open('pex_data.json', 'r') as f:
        obj = json.load(f)

    ffprofile = webdriver.FirefoxProfile('C:/selenium/')
    driver = webdriver.Firefox(firefox_profile=ffprofile)
    # driver = webdriver.Firefox()
    driver.implicitly_wait(1)
    wait = WebDriverWait(driver, 8)

    url = 'https://pex.jp/login'
    driver.get(url)

    if(driver.current_url == url):
        print("Not logged in")
        elem = driver.find_element(By.NAME, 'pex_user_login[email]')
        elem.send_keys(obj['Credential'][0]['Email'])
        elem = driver.find_element(By.NAME, 'pex_user_login[password]')
        elem.send_keys(obj['Credential'][0]['Password'] + Keys.RETURN)
        time.sleep(5)
    else:
        print("Successfully logged in automatically")

    searchWord(driver, wait, keyword_list[0])

    clickQuiz(driver, wait)
    clickPekutan(driver, wait)
    clickSeal(driver, wait)
    clickAnswer(driver, wait)
    clickChirashi(driver, wait)
    clickNews(driver, wait)
    clickLookingforSeal(driver, wait)

    for i in range(1, key_num):
        # for j in range(20):
        #     print('*', end='', flush='ture')
        #     time.sleep(15 + random.randint(0, 5))
        print("< Waiting for next trial ({0}/{1})>".format(i + 1, key_num))
        width = 40
        for j in range(width + 1):
            progress = 1.0 * j / width
            print('\r', get_progressbar_str(width, progress), end='', flush='ture')
            time.sleep(random.randint(8, 10))
        print(" ")

        searchWord(driver, wait, keyword_list[i])
        if(i <= 6):
            clickPekutan(driver, wait)
            clickLookingforSeal(driver, wait)
        else:
            pass

    print("End of Script")
    return


def main2():
    key_num = 6
    keyword_list = getKeyword(key_num)
    print(keyword_list)

    with open('pex_data.json', 'r') as f:
        obj = json.load(f)

    driver = webdriver.Firefox()
    driver.implicitly_wait(1)
    wait = WebDriverWait(driver, 8)

    url = 'https://pex.jp/login'
    driver.get(url)

    if(driver.current_url == url):
        print("Not logged in")
        elem = driver.find_element(By.NAME, 'pex_user_login[email]')
        elem.send_keys(obj['Credential'][0]['Email'])
        elem = driver.find_element(By.NAME, 'pex_user_login[password]')
        elem.send_keys(obj['Credential'][0]['Password'] + Keys.RETURN)
        time.sleep(5)
    else:
        print("Successfully logged in automatically")

    searchWord(driver, wait, keyword_list[0])
    clickLookingforSeal(driver, wait)

    for i in range(1, key_num):
        print("< Waiting for next trial ({0}/{1})>".format(i + 1, key_num))
        width = 40
        for j in range(width + 1):
            progress = 1.0 * j / width
            print('\r', get_progressbar_str(width, progress), end='', flush='ture')
            time.sleep(random.randint(8, 10))
        print(" ")

        searchWord(driver, wait, keyword_list[i])
        if(i <= 6):
            clickLookingforSeal(driver, wait)
        else:
            pass

    print("End of Script")


if __name__ == '__main__':
    main()
