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


def searchtickets_jetstar():
    while True:
        price_jetstar = ""
        jetstar_session_generate_url = r"http://www.jetstar.com/hk/zh/home?origin=KIX&destination=HKG" \
                                       r"&adult=1&children=0&infants=0&flexible=1&departure-date=08-10-2017"
        jetstar_url = r"https://book.jetstar.com/Select.aspx"
        price_xpath = r'//*[@id="main"]/div[6]/div[2]/div[1]/table/tbody/tr[1]/td[4]/div[1]/label'
        button_xpath = r'//*[@id="flightsearch-form"]/div[7]/div/div[2]/div[2]/button'
        driver = webdriver.PhantomJS(executable_path=phantomjs_path, desired_capabilities=dcap)
        driver_getprice = webdriver.PhantomJS(executable_path=phantomjs_path, desired_capabilities=dcap)
        driver_getprice.set_page_load_timeout(200)
        try:
            driver.get(jetstar_session_generate_url)
            button = WebDriverWait(driver, 300).until(
                EC.presence_of_element_located((By.XPATH, button_xpath))
            )
            button.click()
            driver_getprice.get(jetstar_url)
            element = WebDriverWait(driver_getprice, 300).until(
                EC.presence_of_element_located((By.XPATH, price_xpath))
            )
            price_jetstar = element.text
        except Exception as e:
            print(e)
        finally:
            driver.quit()
            driver_getprice.quit()

        date_jetstar = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = datetime.now().strftime("%Y%m%d")
        file_path = "D:\SearchTicket\\jetstar\\price_{0}.txt".format(file_name)
        if price_jetstar is not None:
            with open(file_path, 'a') as f:
                f.write("{0}    {1}\n".format(price_jetstar, date_jetstar))
            print(price_jetstar)
            price_jetstar = int(price_jetstar.replace(',', '').strip("¥").strip())
            if price_jetstar <= 15000:
                sendemail(mailto_list, "票价通知！！！", content="捷星航空机票的价格已经低于15000日元，价格是{0}日元".format(price_jetstar))
                print("香草航空机票的价格已经低于15000日元，价格是{0}日元".format(price_jetstar))
            else:
                print("现在机票还是太贵了，价格是{0}日元".format(price_jetstar))
        else:
            print("加载超时，未能显示页面")


if __name__ == '__main__':
    phantomjs_path = r"C:\Users\apkserver\AppData\Local\Programs\Python\Python35\phantomjs.exe"
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.loadImages"] = False
    threads = []
    t1 = threading.Thread(target=searchtickets_vanilla)
    threads.append(t1)
    t2 = threading.Thread(target=searchtickets_jetstar)
    threads.append(t2)
    for t in threads:
        t.start()
