# coding=utf-8
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import smtplib
from email.mime.text import MIMEText
from datetime import *
import threading
import time


mailto_list = ["297520702@qq.com"]
mail_host = "smtp.163.com"
mail_user = "tc297520702@163.com"
mail_pass = "CHENchunlin0305"


def sendemail(to_list, sub, content):
    me = "Hello<{0}>".format(mail_user)
    msg = MIMEText(content, _subtype='plain', _charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host, '25')
        server.login(mail_user, mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(str(e))
        return False


def searchtickets_vanilla():
    while True:
        price = ""
        vanilla_url = r"https://www.vanilla-air.com/hk/booking/#/flight-select/?tripType=OW&origin=HKG&destination=NRT" \
                      r"&outboundDate=2017-10-01&adults=1&children=0&infants=0&promoCode=&mode=searchResultInter"
        price_xpath = r"/html/body/div[1]/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/div/div[4]" \
                      r"/div/div[2]/dl[2]/dd[2]/div/span/span[2]"

        driver = webdriver.PhantomJS(executable_path=phantomjs_path, desired_capabilities=dcap)
        driver.set_page_load_timeout(300)
        try:
            driver.get(vanilla_url)
            element = WebDriverWait(driver, 300).until(
                EC.presence_of_element_located((By.XPATH, price_xpath))
            )
            price = element.text
        except Exception as e:
            print(e)
        finally:
            driver.quit()

        date_vanilla = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = datetime.now().strftime("%Y%m%d")
        file_path = "D:\SearchTicket\\vanilla\\price_{0}.txt".format(file_name)
        if price is not None:
            with open(file_path, 'a') as f:
                f.write("{0}    {1}\n".format(price, date_vanilla))
            price = int(price.replace(',', '').strip("HKD").strip())
            if price <= 1000:
                sendemail(mailto_list, "票价通知！！！", content="香草航空机票的价格已经低于1000港币，价格是{0}港币".format(price))
                print("香草航空机票的价格已经低于1000港币，价格是{0}港币".format(price))
            else:
                print("现在机票还是太贵了，价格是{0}港币".format(price))
        else:
            print("加载超时，未能显示页面")


def searchtickets_hkexpress():
    while True:
        price = {}
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
            time.sleep(2)
            # 选择大阪机场
            element_from = driver.find_element_by_xpath(r'//*[@id="airportFrom"]/div[4]/a[6]')
            element_from.click()
            # 点击目的地，显示目的地列表
            element_destination = driver.find_element_by_xpath(r'//*[@id="DestinationTo"]')
            element_destination.click()
            # 等待2秒，因为目的地列表为蒙层动画，等待其加载完
            time.sleep(2)
            # 选择香港机场
            element_to = driver.find_element_by_xpath(r'//*[@id="airportTo"]/div[1]/a[1]')
            element_to.click()
            # 输入返程日期
            element_date = driver.find_element_by_xpath(r'//*[@id="DepartureDate"]')
            element_date.send_keys('08/10/2017')
            # 等待2秒
            time.sleep(2)
            # 点击搜寻
            element_submit = driver.find_element_by_xpath(r'//*[@id="search_flight"]/div/div[2]/div[4]/input')
            element_submit.click()
            # 等待2秒
            time.sleep(2)
            # 跳转到另一页面，切换到另一个页面
            driver.switch_to_window(driver.window_handles[0])
        except Exception as e:
            print(e)
        finally:
            pass

        try:
            element_price_one = driver.find_element_by_xpath(
                r'//*[@id="select_departure"]/table/tbody/tr[2]/td[4]/label/span[1]')
            element_price_one_time = driver.find_element_by_xpath(
                r'//*[@id="select_departure"]/table/tbody/tr[2]/td[1]/strong'
            )
            price[element_price_one.text.strip(',').strip('JPY').strip()] = element_price_one_time.text
            print(price)
        except Exception as e:
            print(e)
        finally:
            driver.quit()


if __name__ == '__main__':
    phantomjs_path = r"C:\Users\apkserver\AppData\Local\Programs\Python\Python35\phantomjs.exe"
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.loadImages"] = False
    threads = []
    t1 = threading.Thread(target=searchtickets_vanilla)
    threads.append(t1)
    t2 = threading.Thread(target=searchtickets_hkexpress)
    threads.append(t2)
    for t in threads:
        t.start()
