import urllib, http.cookiejar, socket
import random
import codecs
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
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


def numToOridnal(n):
    suffixes = ("th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th")

    i = (n % 100)
    j = 0 if (i > 10 and i < 20) else (n % 10)
    return "{0}{1}".format(n, suffixes[j])


def searchWord(driver, wait, keyword):
    try :
        print('Start of search')
        driver.get('http://pex.jp/search/index')
        #wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="fixed-box"]/ul/li[6]')))
        #elem = driver.find_element(By.XPATH,'//*[@id="fixed-box"]/ul/li[6]')
        #elem.click()
        print('    moved to "search page"')

        time.sleep(2)
        wait.until(EC.presence_of_element_located((By.ID,'keyword')))
        elem = driver.find_element_by_id('keyword')
        elem.send_keys(keyword + Keys.RETURN)
        print('    searched by "{0}"'.format(keyword))
        print('End of search')
    except NoSuchElementException as err:
        print('Cannot find element: {0}'.format(err))
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
        print('    moved to "quiz page"')

        time.sleep(2)
        r = random.randint(1, 4)
        wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/section/article/section/ul/li[{0}]/a'.format(r))))
        elem = driver.find_element(By.XPATH,'/html/body/section/article/section/ul/li[{0}]/a'.format(r))
        elem.click()
        print('    clicked {0} answer in "quize page"'.format(numToOridnal(r)))

        time.sleep(2)
        alert = driver.switch_to.alert
        alert.accept()
        print('    accepted in dialogue')
        time.sleep(2)
        print('End of quiz')
    except NoSuchElementException as err:
        print('Cannot find element: {0}'.format(err))
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
        print('    moved to "pekutan page"')

        time.sleep(2)
        r = random.randint(1, 2)
        wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/section/article/section/ul/li[{0}]/form/input[5]'.format(r))))
        elem = driver.find_element(By.XPATH,'/html/body/section/article/section/ul/li[{0}]/form/input[5]'.format(r))
        elem.click()
        print('    clicked {0} item for first word'.format(numToOridnal(r)))

        driver.get('http://pex.jp/pekutan/words/current')
        #wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="fixed-box"]/ul/li[8]')))
        #elem = driver.find_element(By.XPATH,'//*[@id="fixed-box"]/ul/li[8]')
        #elem.click()

        time.sleep(2)
        r = random.randint(1, 2)
        wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/section/article/section/ul/li[{0}]/form/input[5]'.format(r))))
        elem = driver.find_element(By.XPATH,'/html/body/section/article/section/ul/li[{0}]/form/input[5]'.format(r))
        elem.click()
        print('    clicked {0} item for Second word'.format(numToOridnal(r)))
        print('End of pekutan')
    except NoSuchElementException as err:
        print('Cannot find element: {0}'.format(err))
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
        print('    moved to "seal page"')

        time.sleep(2)
        wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="mekutte_seal"]/a')))
        elem = driver.find_element(By.XPATH,'//*[@id="mekutte_seal"]/a')
        elem.click()

        print('    moved to detail "seal page"')
        time.sleep(2)
        r = random.randint(1, 4)
        wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="serve"]/li[{0}]/form/input[3]'.format(r))))
        elem = driver.find_element(By.XPATH,'//*[@id="serve"]/li[{0}]/form/input[3]'.format(r))
        elem.click()
        print('    clicked {0} seal'.format(numToOridnal(r)))
        print('End of seal')
    except NoSuchElementException as err:
        print('Cannot find element: {0}'.format(err))
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
        print('    moved to "answer page"')

        time.sleep(2)
        r = random.randint(1, 2)
        wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/section/article/section/ul/li[{0}]/form/input[4]'.format(r))))
        elem = driver.find_element(By.XPATH,'/html/body/section/article/section/ul/li[{0}]/form/input[4]'.format(r))
        elem.click()
        print('    clicked {0} answer in "answer page"'.format(numToOridnal(r)))
        print('End of answer')
    except NoSuchElementException as err:
        print('Cannot find element: {0}'.format(err))
    except:
        print('Error in answer')
    return True


def clickChirashi(driver, wait):
    try :
        print('Start of chirashi')
        driver.get('http://pex.jp/chirashi')
        #wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="fixed-box"]/ul/li[8]')))
        #elem = driver.find_element(By.XPATH,'//*[@id="fixed-box"]/ul/li[8]')
        #elem.click()
        print('    moved to "chirashi page"')
        time.sleep(5)

        for i in range(1,2):
            time.sleep(5)
            wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/section/section[2]/ul/li[{0}]/figure/a[2]'.format(i))))
            elem = driver.find_element(By.XPATH,'/html/body/section/section[2]/ul/li[{0}]/figure/a[2]'.format(i))
            elem.click()
            print('    clicked {0} ad in "chirashi page"'.format(numToOridnal(i)))
        print('End of chirashi')
    except NoSuchElementException as err:
        print('Cannot find element: {0}'.format(err))
    except:
        print('Error in chirashi')
    return True


def clickNews(driver, wait):
    try :
        print('Start of news')
        driver.get('http://pex.jp/point_news')
        #wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="fixed-box"]/ul/li[8]')))
        #elem = driver.find_element(By.XPATH,'//*[@id="fixed-box"]/ul/li[8]')
        #elem.click()
        print('    moved to "news page"')

        for i in range(1,7):
            time.sleep(2)
            wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="news-list"]/li[{0}]/figure/a/div'.format(i))))
            elem = driver.find_element(By.XPATH,'//*[@id="news-list"]/li[{0}]/figure/a/div'.format(i))
            elem.click()
            print('    clicked {0} news in "news page"'.format(numToOridnal(i)))

            time.sleep(5)
            wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="submit-cool"]'.format(i))))
            elem = driver.find_element(By.XPATH,'//*[@id="submit-cool"]'.format(i))
            elem.click()
            print('    clicked cool-icon "news page"')

            driver.get('http://pex.jp/point_news')

        print('End of news')
    except NoSuchElementException as err:
        print('Cannot find element: {0}'.format(err))
    except:
        print('Error in news')
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
    wait = WebDriverWait(driver, 8)

    try:

        driver.get('https://pex.jp/login')
        #assert 'ログイン | ポイント交換のPeX' in driver.title

        elem = driver.find_element(By.NAME,'pex_user_login[email]')
        elem.send_keys(obj['Credential'][0]['Email'])

        elem = driver.find_element(By.NAME, 'pex_user_login[password]')
        elem.send_keys(obj['Credential'][0]['Password'] + Keys.RETURN)

        time.sleep(5)

        searchWord(driver, wait, keyword_list[0])
        clickQuiz(driver, wait)
        clickPekutan(driver, wait)
        clickSeal(driver, wait)
        clickAnswer(driver, wait)
        clickChirashi(driver, wait)
        clickNews(driver, wait)

        for i in range(1,len(keyword_list)):
            for j in range(30):
                print('*', end='', flush='ture')
                time.sleep(9+random.randint(1, 4))
            print(" ")

            searchWord(driver, wait, keyword_list[i])
            if(i<3):
                clickPekutan(driver, wait)

    except:
        print('Unexpected error in Main')

    print("End of Script")


if __name__ == '__main__':
    main()
