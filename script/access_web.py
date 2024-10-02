import os, json, time, requests, platform  # pip install PySocks
import conf.chrome_setting as chrome_setting
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime

print(f'{"*" * 6}conf loading...{"*" * 6}')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"BASE_DIR {BASE_DIR} loading...")
Bin_DIR = os.path.join(BASE_DIR, "bin")
Conf_DIR = os.path.join(BASE_DIR, "conf")
Script_DIR = os.path.join(BASE_DIR, "script")
print(f"OS is {platform.system()} ")

if platform.system() == 'Windows':  # company windows path
    chromedriver_DIR = os.path.join(Bin_DIR+'Windows', 'chromedriver.exe')
    taskkill_exe = os.path.join(Bin_DIR, 'taskkill.exe')
    Ping_exe = os.path.join(r'C:\Windows\System32', 'PING.EXE')  
elif platform.system() == "Darwin" :
    chromedriver_DIR = os.path.join(Bin_DIR+'/Mac', 'chromedriver_92') 
    Ping_exe = 'ping'
else :
    chromedriver_DIR = os.path.join(Bin_DIR+'/Linux', 'chromedriver') 
    Ping_exe = 'ping'
print(f"chromedriver_DIR is {chromedriver_DIR} ")

test_json_DIR = os.path.join(Conf_DIR, 'test_index.json')

with open(test_json_DIR, 'r', encoding='utf-8-sig') as json_file:  # 各種變數
    test_index = json.loads(json_file.read())
    urls = test_index['url']['test']


def split_list(A, n=50):
    return [A[i:i + n] for i in range(0, len(A), n)]

def askwebPC(url, timeout=30):
    return test_run(url,timeout,'//div[contains(@class, \"header_menu-container\")]')

def askwebWAP(url, timeout=30):
    return test_run(url,timeout,'//div[contains(@class, \"header_logoContainer_\")]',True)

def test_run(url,timeout,element_locator,is_WAP=False) :
    return_seconds = 0
    set = chrome_setting.driv_option()
    if is_WAP :
        set.add_experimental_option('mobileEmulation', {'deviceName': 'iPhone X'})
    # set.add_argument('--proxy-server=socks5://%s:%s' % ('127.0.0.1', '1080'))
    driver = webdriver.Chrome(chromedriver_DIR, options=set)
    driver.set_page_load_timeout(timeout)  # timeout 155s 240s 4分鐘
    if is_WAP :
        driver.set_window_size(960, 950)
    else :
        driver.set_window_size(1366, 1000)

    driver.start_client()

    if "http" not in url:  # requests 网址要有http://
        web_url = f"http://{url}"
    else:
        web_url = url

    try:
        start_time = datetime.now()        
        driver.get(web_url)                
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, element_locator)))
        end_time = datetime.now()
        return_seconds= (end_time - start_time).seconds

    except Exception as e:
        # print("\033[34;1m ***ERROR*** [%s]  \033[0m" % web_url)
        if driver.find_elements_by_xpath('//div[contains(@class, \"maintenance_maintenance\")]') : 
            return_seconds = 0
        else :
            return_seconds = -1
    finally:
        driver.quit()           
        return return_seconds

