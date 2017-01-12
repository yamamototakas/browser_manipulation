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


def searchWord(driver, wait, keyword):
    try :
        print('Start of search')
        driver.get('http://pex.jp/search/index')
        #wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="fixed-box"]/ul/li[6]')))
        #elem = driver.find_element(By.XPATH,'//*[@id="fixed-box"]/ul/li[6]')
        #elem.click()
        print('    moved to search page')

        time.sleep(2)
        wait.until(EC.presence_of_element_located((By.ID,'keyword')))
        elem = driver.find_element_by_id('keyword')
        elem.send_keys(keyword + Keys.RETURN)
        print('    and searched, End of search')

    except:
        print('Error in search')
    return True


def clickQuiz(driver, wait):
    try :
        print('Start of quiz')
        driver.get('http://pex.jp/point_quiz')
        #wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="fixed-box"]/ul/li[5]')))
        #elem = driver.find_element(By.XPATH,'//*[@id="fixed-box"]/ul/li[5]')
        #elem.click()
        print('    moved to search quiz page')

        time.sleep(2)
        r = random.randint(1, 4)
        wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/section/article/section/ul/li[%r]/a' % r)))
        elem = driver.find_element(By.XPATH,'/html/body/section/article/section/ul/li[%r]/a' % r)
        elem.click()
        print('    clicked %r in quiz' % r)

        time.sleep(2)
        alert = driver.switch_to.alert
        alert.accept()
        print('    and accepted in dialogue, End of quiz')

    except:
        print('Error in quiz')
    return True


def clickPekutan(driver, wait):
    try :
        print('Start of pekutan')
        driver.get('http://pex.jp/pekutan/words/current')
        #wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="fixed-box"]/ul/li[8]')))
        #elem = driver.find_element(By.XPATH,'//*[@id="fixed-box"]/ul/li[8]')
        #elem.click()
        print('    moved to pekutan page')

        time.sleep(2)
        r = random.randint(1, 2)
        wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/section/article/section/ul/li[%r]/form/input[5]' % r)))
        elem = driver.find_element(By.XPATH,'/html/body/section/article/section/ul/li[%r]/form/input[5]' % r)
        elem.click()
        print('    clicked 1st word as %r' % r)

        driver.get('http://pex.jp/pekutan/words/current')
        #wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="fixed-box"]/ul/li[8]')))
        #elem = driver.find_element(By.XPATH,'//*[@id="fixed-box"]/ul/li[8]')
        #elem.click()

        time.sleep(2)
        r = random.randint(1, 2)
        wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/section/article/section/ul/li[%r]/form/input[5]' % r)))
        elem = driver.find_element(By.XPATH,'/html/body/section/article/section/ul/li[%r]/form/input[5]' % r)
        elem.click()
        print('    clicked 2nd word as %r, End of pekutan' % r)
    except:
        print('Error in pekutan')
    return True

def clickSeal(driver, wait):
    try :
        print('Start of seal')
        driver.get('http://pex.jp/seal')
        #wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="fixed-box"]/ul/li[8]')))
        #elem = driver.find_element(By.XPATH,'//*[@id="fixed-box"]/ul/li[8]')
        #elem.click()
        print('    moved to seal page')

        time.sleep(2)
        wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="mekutte_seal"]/a')))
        elem = driver.find_element(By.XPATH,'//*[@id="mekutte_seal"]/a')
        elem.click()

        print('    moved to seal inside page')
        time.sleep(2)
        r = random.randint(1, 4)
        wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="serve"]/li[%r]/form/input[3]' % r)))
        elem = driver.find_element(By.XPATH,'//*[@id="serve"]/li[%r]/form/input[3]' % r)
        elem.click()


        print('    clicked %r seal, End of seal' % r)
    except:
        print('Error in seal')
    return True

def clickAnswer(driver, wait):
    try :
        print('Start of answer')
        driver.get('http://pex.jp/minna_no_answer/questions/current')
        #wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="fixed-box"]/ul/li[8]')))
        #elem = driver.find_element(By.XPATH,'//*[@id="fixed-box"]/ul/li[8]')
        #elem.click()
        print('    moved to answer page')

        time.sleep(2)
        r = random.randint(1, 2)
        wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/section/article/section/ul/li[%r]/form' % r)))
        elem = driver.find_element(By.XPATH,'/html/body/section/article/section/ul/li[%r]/form' % r)
        elem.click()
        print('    clicked %r answer, End of answer' % r)
    except:
        print('Error in answer')
    return True


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
    #assert 'ログイン | ポイント交換のPeX' in driver.title

    elem = driver.find_element(By.NAME,'pex_user_login[email]')
    elem.send_keys(obj['Credential'][0]['Email'])

    elem = driver.find_element(By.NAME, 'pex_user_login[password]')
    elem.send_keys(obj['Credential'][0]['Password'] + Keys.RETURN)

    time.sleep(2)

    searchWord(driver, wait, keyword_list[0])
    clickQuiz(driver, wait)
    clickPekutan(driver, wait)
    clickSeal(driver, wait)
    clickAnswer(driver, wait)



    '''
    for each in keyword_list:
        print(each)
        wait.until(EC.presence_of_element_located((By.ID,'keyword')))
        elem = driver.find_element_by_id('keyword')
        elem.send_keys(each + Keys.RETURN)

        for j in range(30):
            print('*', end='', flush='ture')
            time.sleep(9+random.randint(1, 4))
    '''


    print("End of Script")


if __name__ == '__main__':
    main()
