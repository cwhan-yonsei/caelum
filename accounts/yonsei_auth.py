import selenium

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import traceback

def verify(portal_id, portal_pw):
    a = 0
    if portal_id[4] == '1':
        try:
            options = webdriver.ChromeOptions()
            a = 1
            options.add_argument('--headless')
            options.add_argument('window-size=1366x768')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            driver = webdriver.Chrome('/home/cwahn/yonsei/caelum/downloads/chromedriver', options=options)
            wait = WebDriverWait(driver, 20)
            a = 2
            driver.get('http://underwood1.yonsei.ac.kr/haksa/sso/main.jsp')
            #driver.delete_all_cookies()
            a = 3
            wait.until(EC.element_to_be_clickable(
                (By.ID, 'loginId'))).send_keys(portal_id)
            wait.until(EC.element_to_be_clickable(
                (By.ID, 'loginPasswd'))).send_keys(portal_pw)
            wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#container > fieldset > button'))).click()
            a = 4
            wait.until(EC.element_to_be_clickable((By.ID, 'btn_lang'))).click()
            a = 5

            name = ''
            dept_major = ''

            while name == '' or dept_major == '':
                name = driver.find_element_by_id(
                    'wq_uuid_63').get_attribute("textContent")
                dept_major = driver.find_element_by_id(
                    'wq_uuid_77').get_attribute("textContent")
                a = 6
                
            wait.until(EC.element_to_be_clickable((By.ID, 'btn_logout'))).click()    
            a = 7

            driver.quit()
            a = 8
            return True, str(name), str(dept_major)

        except Exception as e:
            try:
                driver.quit()
            finally:
                tb = traceback.format_exc()
                return False, 'this is an exception:' + str(e), str(a) + str(tb)
    else:
        return False, 'not y', 'not y'


#result = verify('2016145118', 'A!S@d3f42559')
#print(result[0], result[1], result[2])