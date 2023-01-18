import pickle
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
import sqlite3 as sq


# Auto login
# username = driver.find_element(by=By.XPATH, value=('//*[@id="session_key"]'))
# password = driver.find_element(by=By.XPATH, value=('//*[@id="session_password"]'))
# time.sleep(3)
# username.send_keys(my_login)
# password.send_keys(my_password)
# time.sleep(10)
# driver.find_element(by=By.XPATH, value=('//*[@id="main-content"]/section[1]/div/div/form/button')).click()

# Extract cookie to use autologin with cookie
# with open(cookies_path, 'wb') as f:
#     pickle.dump(driver.get_cookies(), f)

options = Options()
# Show or hide browser
options.headless = True
# disable webrdiver-mode:
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=options,
                          )
# import cookie
cookies_path = 'parser/my_cookies.dat'
driver.get('https://www.linkedin.com')
with open(cookies_path, 'rb') as f:
    for cookie in pickle.load(f):
        driver.add_cookie(cookie)


driver.maximize_window()
stop_pages = 50
username_list = []
status_list = []
for n in tqdm(range(1, stop_pages)):
    driver.get("https://www.linkedin.com/search/results/people/?keywords=python&origin=CLUSTER_EXPANSION&page=" + str(n))
    time.sleep(1)
    connect = driver.find_elements(by=By.TAG_NAME, value='button')
    connect_buttons = [button for button in connect if button.text == "Установить контакт"]
    time.sleep(1)
    for button in connect_buttons:
        driver.execute_script("arguments[0].click();", button)
        time.sleep(1)

        # Save var username
        find_username = driver.find_element(by=By.CSS_SELECTOR, value="span[class='flex-1'] strong")
        username_text = find_username.text

        # Find button send now
        send = driver.find_element(by=By.XPATH, value="//button[@aria-label='Отправить сейчас']")
        # Click on button send
        driver.execute_script("arguments[0].click();", send)
        username_list.append(username_text)
        status_list.append('Added successfully')

res = list(zip(username_list, status_list))

# Add to db
if len(res) != 0:
    conn = sq.connect('parserdb.db')
    print('Connected to database successfully.')
    cursor = conn.cursor()
    cursor.executemany("""INSERT INTO parsing (name, status) VALUES (?, ?) """, res)
    print('Records inserted successfully.')
    conn.commit()
    conn.close()

driver.quit()
