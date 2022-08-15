import requests
from bs4 import BeautifulSoup
import time
import win10toast
from multiprocessing import Process

DOLLAR_RUB = 'https://www.google.com/finance/quote/USD-RUB'
BTC_USD = 'https://www.google.com/finance/quote/BTC-USD'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.50'}


# dollar rate
def get_rate():
    last_result = 0
    while True:
        session = requests.Session()
        session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 OPR/89.0.4447.64 (Edition Yx GX) '}
        cookies = dict(cookies_are = 'working')
        headers = session.headers
        fullpage = requests.get(DOLLAR_RUB, headers=headers, cookies=cookies)

        soup = BeautifulSoup(fullpage.content, 'html.parser')
        kurs = soup.find("div", {"class": "YMlKec", "class": "fxKbKc"})
        result = kurs.text
        result_float = round(float(result), 2)
        message = "Курс доллара к рублю: " + str(result_float)
        print(message)
        if last_result != result_float:
            pyshUSD(result)
        last_result = result_float
        time.sleep(10)

# bts rate
def get_bts():
    last_result = 0
    while True:
        session = requests.Session()
        session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 OPR/89.0.4447.64 (Edition Yx GX) '}
        cookies = dict(cookies_are='working')
        headers = session.headers
        fullpage = requests.get(BTC_USD, headers=headers, cookies=cookies)

        soup = BeautifulSoup(fullpage.content, 'html.parser')
        kurs = soup.find("div", {"class": "YMlKec", "class": "fxKbKc"})
        result = kurs.text.replace(',', '')
        result_float = round(float(result), 2)
        message = "Курс биткойна к доллару: " + str(result_float)
        print(message)
        if last_result != result_float:
            pyshUSD(result)
        last_result = result_float
        time.sleep(10)

# push windows
def pyshUSD(value):
    toaster = win10toast.ToastNotifier()
    toaster.show_toast(value)

###
if __name__ == '__main__':
    p1 = Process(target=get_rate)
    p2 = Process(target=get_bts)

    p1.start()
    p2.start()

    p1.join()
    p2.join()

