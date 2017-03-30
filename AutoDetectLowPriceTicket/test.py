# coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time as sleeptime
from datetime import *


if __name__ == '__main__':
    price = {}
    dcap = dict(DesiredCapabilities.CHROME)
    dcap["phantomjs.page.settings.loadImages"] = False
    chromedrive_path = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=chromedrive_path, desired_capabilities=dcap)
    driver.set_page_load_timeout(15)
    try:
        driver.get('http://www.hkexpress.com/zh-cn')
    except Exception as e:
        print(e)

    try:
        # 选择单程
        element_oneway = driver.find_element_by_xpath(r'//*[@id="single"]')
        element_oneway.click()
        # 点击出发地，显示出发地列表
        element_originfrom = driver.find_element_by_xpath(r'//*[@id="OriginFrom"]')
        element_originfrom.click()
        # 等待2秒，因为出发地列表为蒙层动画，等待其加载完
        sleeptime.sleep(2)
        # 选择大阪机场
        element_from = driver.find_element_by_xpath(r'//*[@id="airportFrom"]/div[4]/a[6]')
        element_from.click()
        # 点击目的地，显示目的地列表
        element_destination = driver.find_element_by_xpath(r'//*[@id="DestinationTo"]')
        element_destination.click()
        # 等待2秒，因为目的地列表为蒙层动画，等待其加载完
        sleeptime.sleep(2)
        # 选择香港机场
        element_to = driver.find_element_by_xpath(r'//*[@id="airportTo"]/div[1]/a[1]')
        element_to.click()
        # 输入返程日期
        element_date = driver.find_element_by_xpath(r'//*[@id="DepartureDate"]')
        element_date.send_keys('08/10/2017')
        # 等待2秒
        sleeptime.sleep(2)
        # 点击搜寻
        element_submit = driver.find_element_by_xpath(r'//*[@id="search_flight"]/div/div[2]/div[4]/input')
        element_submit.click()
    except Exception as e:
        print(e)

    try:
        driver.switch_to.window(driver.current_window_handle)
    except Exception as e:
        print(e)

    sleeptime.sleep(200)

    try:
        element_price_one = WebDriverWait(driver, 200).until(
            EC.presence_of_element_located((By.XPATH, r'//*[@id="select_departure"]/table/tbody/tr[2]/td[4]/label/span[1]'))
        )
        element_price_one_time = driver.find_element_by_xpath(r'//*[@id="select_departure"]/table/tbody/tr[2]/td[1]/strong')
        price[element_price_one_time.text] = element_price_one.text.replace(',', '').strip('JPY').strip()
        element_price_two =driver.find_element_by_xpath(r'//*[@id="select_departure"]/table/tbody/tr[3]/td[4]/label/span[1]')
        element_price_two_time = driver.find_element_by_xpath(r'//*[@id="select_departure"]/table/tbody/tr[3]/td[1]/strong')
        price[element_price_two_time.text] = element_price_two.text.replace(',', '').strip('JPY').strip()
    except Exception as e:
        print(e)
    finally:
        print(price)
        driver.quit()

    result = {}
    flag = False
    for key in price:
        if int(price[key]) < 15000:
            result[key] = price[key]
            flag = True

    date_hkexpress = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = datetime.now().strftime("%Y%m%d")
    file_path = "D:\SearchTicket\\hkexpress\\price_{0}.txt".format(file_name)

    if flag:
        print("有机票的价格已经在15000日元以下，票价为：{0}".format(result))
    else:
        print("机票的价格还是太高了")

