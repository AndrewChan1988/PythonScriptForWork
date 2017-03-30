from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import smtplib
from email.mime.text import MIMEText
from datetime import *

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
    phantomjs_path = r"C:\Users\apkserver\AppData\Local\Programs\Python\Python35\phantomjs.exe"
    vanilla_url = r"https://www.vanilla-air.com/hk/booking/#/flight-select/?tripType=OW&origin=HKG&destination=NRT" \
                  r"&outboundDate=2017-10-01&adults=1&children=0&infants=0&promoCode=&mode=searchResultInter"
    price_xpath = r"/html/body/div[1]/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/div/div[4]" \
                  r"/div/div[2]/dl[2]/dd[2]/div/span/span[2]"
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.loadImages"] = False

    driver = webdriver.PhantomJS(executable_path=phantomjs_path, desired_capabilities=dcap)
    driver.set_page_load_timeout(300)
    try:
        driver.get(vanilla_url)
        element = WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.XPATH, price_xpath))
        )
        return element.text
    except Exception as e:
        print(e)
    finally:
        driver.quit()


if __name__ == '__main__':
    while True:
        price = searchtickets_vanilla()
        date = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = datetime.now().strftime("%Y%m%d")
        file_path = "D:\SearchTicket\\price_{0}.txt".format(file_name)
        if price is not None:
            with open(file_path, 'a') as f:
                f.write("{0}    {1}\n".format(price, date))
            price = int(price.replace(',', '').strip("HKD").strip())
            if price <= 1000:
                sendemail(mailto_list, "票价通知！！！", content="香草航空机票的价格已经低于1000港币，价格是{0}港币".format(price))
                print("香草航空机票的价格已经低于1000港币，价格是{0}港币".format(price))
            else:
                print("现在机票还是太贵了，价格是{0}港币".format(price))
        else:
            print("加载超时，未能显示页面")
