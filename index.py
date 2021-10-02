from idlelib import browser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
import requests
import time
import random
from config import login_passport, password_passport, url_yandex_auth, url_yandex_order, ya_token, ya_channel_id

# from fake_useragent import UserAgent
# useragent = UserAgent()

options = webdriver.ChromeOptions()
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    # f"user-agent={useragent.random}"
)

#set headless
#options.add_argument("--headless")

#set proxy
#options.add_argument("--proxy-server=93.183.84.150:8080")

options.add_argument("--disable-blink-features=AutomationControlled")

url = url_yandex_auth
driver = webdriver.Chrome(
    executable_path='./Selenium_Auto_auth/chromedriver',
    options=options
)

driver.get(url)
login = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (
            By.ID, 'passp-field-login'
        )
    )
)
login.send_keys(login_passport)
btnLogin = driver.find_element_by_class_name(
    'Button2_type_submit'
).click()
password_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (
            By.ID, 'passp-field-passwd'
        )
    )
)
password_field.send_keys(password_passport)
driver.find_element_by_class_name(
    'Button2_type_submit'
).click()

time.sleep(10)

#https://uslugi.yandex.ru/order

driver.get(url_yandex_order)
time.sleep(3)

#Время получения сообщения
time_message = driver.find_elements_by_class_name("OrderCard2-CreationInfo")
time_count = 0
time_arr = []
for t in time_message:
    time_out = time_message[time_count].find_element_by_class_name('OrderCard2-Time')
    time_text = time_out.text
    time_text = ''.join([i for i in time_text if i.isdigit()])
    time_arr.append(time_text)
    time_count = time_count + 1
#генератор списка, удаляет пустые строки
time_arr = [x for x in time_arr if x]
#преобразование строчных чисел в списке в числа
for io, item in enumerate(time_arr):
    time_arr[io] = int(item)
print(time_arr)

#Ссылки услуг
elems = driver.find_elements_by_css_selector(".OrderCard2-TitleRow [href]")
links = [elem.get_attribute('href') for elem in elems]
# print(links)

#Заголовки услуг
example = driver.find_elements_by_class_name("OrderCard2-TitleRow")
count = 0
arr = []
for i in example:
    out = example[count].find_element_by_class_name('Text_type_medium')
    arr.append(out.text)
    count = count + 1
# print(arr)

#цикл вывода информации
bot_info = []
bot_count = 0
#счетчик времени
for bot in time_arr:
    #если заявонька упала за последние x минуты допустим
    if time_arr[bot_count] < 55:
        bot_info.append(arr[bot_count] + ' - ' + links[bot_count])
        bot_count = bot_count + 1
print(bot_info)

#отправка данных в телеграм бот
def send_telegram(text: str):
    token = ya_token
    url = "https://api.telegram.org/bot"
    channel_id = ya_channel_id
    url += token
    method = url + "/sendMessage"
    r = requests.post(method, data={
         "chat_id": channel_id,
         "text": bot_info[0]
          })

    if r.status_code != 200:
        raise Exception("post_text error")

if __name__ == '__main__':
  send_telegram("hello world!")